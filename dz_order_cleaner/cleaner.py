"""Core pipeline: fix phones, normalise wilayas, split out duplicates."""
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence

from .phone import clean_phone, to_international
from .text import normalize
from .wilaya import format_wilaya, match_wilaya

PHONE_HEADERS = {"phone", "telephone", "tel", "mobile", "gsm", "numero", "num", "contact",
                 "phone number", "numero de telephone", "هاتف", "رقم الهاتف", "الهاتف", "رقم"}
WILAYA_HEADERS = {"wilaya", "state", "province", "region", "ville", "city",
                  "ولاية", "الولاية", "ولايه"}


def detect_column(headers: Sequence[str], candidates: Iterable[str]) -> Optional[str]:
    wanted = {normalize(c) for c in candidates}
    for h in headers:
        if normalize(h) in wanted:
            return h
    return None


@dataclass
class CleanResult:
    headers: List[str]
    clean: List[Dict] = field(default_factory=list)
    review: List[Dict] = field(default_factory=list)       # rows needing a human look
    duplicates: List[Dict] = field(default_factory=list)   # removed duplicate rows
    review_headers: List[str] = field(default_factory=list)
    duplicate_headers: List[str] = field(default_factory=list)

    @property
    def stats(self) -> Dict[str, int]:
        return {"clean": len(self.clean), "needs_review": len(self.review),
                "duplicates_removed": len(self.duplicates)}


def clean_rows(
    rows: List[Dict],
    headers: Sequence[str],
    phone_col: Optional[str] = None,
    wilaya_col: Optional[str] = None,
    dedupe_by: Sequence[str] = ("phone",),
    wilaya_format: str = "fr",
    international: bool = False,
    add_code: bool = False,
) -> CleanResult:
    """Clean `rows` (list of dicts). Raises ValueError if columns can't be found."""
    phone_col = phone_col or detect_column(headers, PHONE_HEADERS)
    wilaya_col = wilaya_col or detect_column(headers, WILAYA_HEADERS)
    if not phone_col:
        raise ValueError("Could not detect the phone column; pass phone_col=...")
    if not wilaya_col:
        raise ValueError("Could not detect the wilaya column; pass wilaya_col=...")

    out_headers = list(headers) + (["wilaya_code"] if add_code else [])
    result = CleanResult(headers=out_headers)
    result.review_headers = out_headers + ["source_row", "issues"]
    result.duplicate_headers = out_headers + ["source_row", "duplicate_of_row"]

    custom_cols = {}
    for name in dedupe_by:
        if name not in ("phone", "wilaya"):
            col = detect_column(headers, [name])
            if not col:
                raise ValueError(f"Dedupe column {name!r} not found in headers")
            custom_cols[name] = col

    seen: Dict[tuple, int] = {}
    for i, original in enumerate(rows, start=2):  # row 1 is the header line
        row = dict(original)
        issues = []

        number, reason = clean_phone(row.get(phone_col))
        if number:
            row[phone_col] = to_international(number) if international else number
        else:
            issues.append(reason)

        w = match_wilaya(row.get(wilaya_col))
        if w:
            row[wilaya_col] = format_wilaya(w, wilaya_format)
        else:
            issues.append(f"unrecognised wilaya: {row.get(wilaya_col)!r}")
        if add_code:
            row["wilaya_code"] = w.code_str if w else ""

        if number:  # only dedupe rows whose phone we trust
            key = tuple(
                number if n == "phone"
                else (w.code if w else None) if n == "wilaya"
                else normalize(row.get(custom_cols[n], ""))
                for n in dedupe_by
            )
            if key in seen:
                row.update(source_row=i, duplicate_of_row=seen[key])
                result.duplicates.append(row)
                continue
            seen[key] = i

        if issues:
            row.update(source_row=i, issues="; ".join(issues))
            result.review.append(row)
        else:
            result.clean.append(row)
    return result
