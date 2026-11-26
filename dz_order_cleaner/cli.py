"""Command line interface: `dz-clean orders.csv`."""
import argparse
import sys
from pathlib import Path

from . import __version__
from .cleaner import clean_rows
from .io import read_table, write_table


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dz-clean",
        description="Clean Algerian e-commerce order files: phones, wilayas, duplicates.")
    p.add_argument("input", help="orders file (.csv or .xlsx)")
    p.add_argument("-o", "--output-dir", help="where to write results (default: next to input)")
    p.add_argument("--phone-col", help="phone column name (auto-detected if omitted)")
    p.add_argument("--wilaya-col", help="wilaya column name (auto-detected if omitted)")
    p.add_argument("--dedupe-by", default="phone",
                   help="comma-separated keys that define a duplicate, e.g. phone,product "
                        "(default: phone)")
    p.add_argument("--wilaya-format", choices=["fr", "ar", "code"], default="fr",
                   help="how to write wilaya names (default: fr)")
    p.add_argument("--international", action="store_true",
                   help="write phones as +213XXXXXXXXX instead of 0XXXXXXXXX")
    p.add_argument("--add-code", action="store_true", help="add a wilaya_code column")
    p.add_argument("--encoding", help="force input encoding (CSV only)")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    src = Path(args.input)
    if not src.exists():
        print(f"error: {src} not found", file=sys.stderr)
        return 2

    headers, rows = read_table(src, args.encoding)
    try:
        res = clean_rows(
            rows, headers, phone_col=args.phone_col, wilaya_col=args.wilaya_col,
            dedupe_by=[s.strip() for s in args.dedupe_by.split(",") if s.strip()],
            wilaya_format=args.wilaya_format, international=args.international,
            add_code=args.add_code)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    out = Path(args.output_dir) if args.output_dir else src.parent
    out.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower() if src.suffix.lower() == ".xlsx" else ".csv"
    paths = {
        "clean": out / f"{src.stem}_clean{ext}",
        "review": out / f"{src.stem}_review{ext}",
        "duplicates": out / f"{src.stem}_duplicates{ext}",
    }
    write_table(paths["clean"], res.headers, res.clean)
    if res.review:
        write_table(paths["review"], res.review_headers, res.review)
    if res.duplicates:
        write_table(paths["duplicates"], res.duplicate_headers, res.duplicates)

    total = len(rows)
    print(f"Processed {total} rows")
    print(f"  ✓ clean:      {len(res.clean):>5}  -> {paths['clean']}")
    if res.review:
        print(f"  ! to review:  {len(res.review):>5}  -> {paths['review']}")
    if res.duplicates:
        print(f"  × duplicates: {len(res.duplicates):>5}  -> {paths['duplicates']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
