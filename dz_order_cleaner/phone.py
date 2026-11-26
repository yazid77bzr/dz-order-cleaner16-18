"""Algerian phone number cleaning."""
import re
from typing import Optional, Tuple

from .text import AR_DIGITS

MOBILE = re.compile(r"^0[567]\d{8}$")      # 05/06/07 + 8 digits
LANDLINE = re.compile(r"^0[234]\d{7}$")    # 02x/03x/04x + 6 digits
_SPLIT = re.compile(r"[/,;|\n]|\s[-–]\s|\s+(?:و|ou|or)\s+")


def _clean_one(raw: str) -> Optional[str]:
    s = raw.translate(AR_DIGITS)
    s = re.sub(r"\(\s*0\s*\)", "", s)        # +213 (0) 550 ...
    d = re.sub(r"\D", "", s)
    if d.startswith("00213"):
        d = d[5:]
    elif d.startswith("0213") and len(d) in (12, 13):
        d = d[4:]
    elif d.startswith("213") and len(d) in (11, 12):
        d = d[3:]
    if d and not d.startswith("0"):
        d = "0" + d
    return d if (MOBILE.match(d) or LANDLINE.match(d)) else None


def clean_phone(raw) -> Tuple[Optional[str], str]:
    """Return (local_number, reason). local_number looks like '0550123456',
    or None with a human-readable reason when it can't be fixed."""
    if isinstance(raw, float) and raw.is_integer():   # Excel stores 550123456 as 550123456.0
        raw = int(raw)
    if raw is None or str(raw).strip() == "":
        return None, "missing phone"
    for part in _SPLIT.split(str(raw)):
        if part.strip():
            number = _clean_one(part)
            if number:
                return number, ""
    return None, f"invalid phone: {raw!r}"


def to_international(local: str) -> str:
    """0550123456 -> +213550123456"""
    return "+213" + local[1:]
