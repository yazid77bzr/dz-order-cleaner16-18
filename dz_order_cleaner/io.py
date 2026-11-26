"""Read/write CSV and (optionally) XLSX files."""
import csv
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ENCODINGS = ("utf-8-sig", "cp1252", "latin-1")


def _read_csv(path: Path, encoding: Optional[str]) -> Tuple[List[str], List[Dict]]:
    raw = path.read_bytes()
    text = None
    for enc in ([encoding] if encoding else ENCODINGS):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise ValueError("Could not decode file; try --encoding")
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(text.splitlines(), dialect=dialect)
    headers = [h.strip() for h in (reader.fieldnames or [])]
    reader.fieldnames = headers
    return headers, [{k: (v or "") for k, v in r.items() if k is not None} for r in reader]


def _cell(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


def _read_xlsx(path: Path) -> Tuple[List[str], List[Dict]]:
    try:
        from openpyxl import load_workbook
    except ImportError as e:
        raise SystemExit("XLSX support needs openpyxl:  pip install 'dz-order-cleaner[xlsx]'") from e
    ws = load_workbook(path, read_only=True, data_only=True).active
    data = list(ws.iter_rows(values_only=True))
    if not data:
        return [], []
    headers = [_cell(h).strip() for h in data[0]]
    rows = [dict(zip(headers, map(_cell, r))) for r in data[1:] if any(c is not None for c in r)]
    return headers, rows


def read_table(path, encoding: Optional[str] = None) -> Tuple[List[str], List[Dict]]:
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        return _read_xlsx(path)
    return _read_csv(path, encoding)


def write_table(path, headers: Sequence[str], rows: List[Dict]) -> None:
    path = Path(path)
    if path.suffix.lower() == ".xlsx":
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(list(headers))
        for r in rows:
            ws.append([r.get(h, "") for h in headers])
        # keep phones as text so Excel doesn't drop the leading zero
        for col in ws.iter_cols(min_row=2):
            for c in col:
                if isinstance(c.value, str):
                    c.number_format = "@"
        wb.save(path)
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:  # BOM: Excel reads Arabic correctly
        w = csv.DictWriter(f, fieldnames=list(headers), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
