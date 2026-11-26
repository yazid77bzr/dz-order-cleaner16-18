"""Map free-text wilaya input (Arabic / French / typos / codes) to an official wilaya."""
import re
from difflib import SequenceMatcher
from functools import lru_cache
from typing import Optional

from .text import normalize
from .wilayas import BY_CODE, WILAYAS, Wilaya

FUZZY_CUTOFF = 0.80
_AMBIGUITY_GAP = 0.04
_PREFIX = re.compile(r"^(?:wilaya|willaya|ولايه|ولاية)\s+(?:(?:de|d)\s+)?")
_LEADING_CODE = re.compile(r"^(\d{1,2})\s*(.*)$")


def _build_index():
    index = {}
    for w in WILAYAS:
        for name in (w.fr, w.ar, *w.aliases):
            key = normalize(name)
            index[key] = w
            if key.startswith("ال") and len(key) > 4:   # allow input without "ال"
                index.setdefault(key[2:], w)
    return index


_INDEX = _build_index()


def _fuzzy(key: str) -> Optional[Wilaya]:
    if len(key) < 3:
        return None
    best = {}
    for alias, w in _INDEX.items():
        r = SequenceMatcher(None, key, alias).ratio()
        if r >= FUZZY_CUTOFF and r > best.get(w.code, (0, None))[0]:
            best[w.code] = (r, w)
    ranked = sorted(best.values(), key=lambda x: -x[0])
    if not ranked:
        return None
    if len(ranked) > 1 and ranked[0][0] - ranked[1][0] < _AMBIGUITY_GAP:
        return None  # too close to call: let a human decide
    return ranked[0][1]


@lru_cache(maxsize=8192)
def _match_key(key: str) -> Optional[Wilaya]:
    if not key:
        return None
    key = _PREFIX.sub("", key).strip()
    code = None
    m = _LEADING_CODE.match(key)
    if m:
        code = BY_CODE.get(int(m.group(1)))
        key = m.group(2).strip()
        if not key:
            return code
    if key in _INDEX:
        return _INDEX[key]
    found = _fuzzy(key)
    return found or code


def match_wilaya(raw) -> Optional[Wilaya]:
    """Return the matching Wilaya, or None if it can't be determined safely."""
    if raw is None:
        return None
    return _match_key(normalize(raw))


def format_wilaya(w: Wilaya, fmt: str = "fr") -> str:
    return {"fr": w.fr, "ar": w.ar, "code": w.code_str}[fmt]
