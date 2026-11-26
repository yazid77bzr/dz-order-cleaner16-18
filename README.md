# dz-order-cleaner 🇩🇿

[![tests](https://github.com/yazid77bzr/dz-order-cleaner/actions/workflows/tests.yml/badge.svg)](https://github.com/yazid77bzr/dz-order-cleaner/actions)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

**Clean messy Algerian e-commerce order exports in one command — ready for Yalidine, ZR Express and other couriers.**

Customers type their details however they like. This tool takes your raw orders file (CSV or Excel) and:

- 📞 **Fixes phone numbers** — `+213 550 12 34 56`, `550123456`, `00213550123456`, `0550-12-34-56`, Arabic digits `٠٧٧٠…` → `0550123456`
- 🗺️ **Normalises the 58 wilayas** — `الجزاير`, `Alger`, `algiers`, `16 - Alger`, `Wilaya de Béjaïa`, `bejaia`, `BBA`, `برج بوعريرج` → one official name
- 🧹 **Removes duplicate orders** — same customer ordering twice by mistake (removed rows are saved, never deleted)
- 🔎 **Flags what it can't fix** — instead of guessing, unclear rows go to a separate review file

No dependencies for CSV. Optional `openpyxl` for `.xlsx`.

## Install

```bash
pip install git+https://github.com/YOUR_USERNAME/dz-order-cleaner.git
# with Excel support:
pip install "dz-order-cleaner[xlsx] @ git+https://github.com/YOUR_USERNAME/dz-order-cleaner.git"
```

Or run from source: `git clone … && cd dz-order-cleaner && python -m dz_order_cleaner orders.csv`

## Usage

```bash
dz-clean orders.csv
```

Produces three files next to your input:

| File | Content |
|------|---------|
| `orders_clean.csv` | Valid rows, ready to import into your courier's platform |
| `orders_review.csv` | Rows with a bad phone or unknown wilaya, plus an `issues` column |
| `orders_duplicates.csv` | Removed duplicates, with the row number of the original |

### Example

| phone (before) | wilaya (before) | → phone | → wilaya |
|---|---|---|---|
| `+213 550 12 34 56` | `Alger` | `0550123456` | `Alger` |
| `550123456` | `الجزاير` | `0550123456` | `Alger` *(duplicate → removed)* |
| `00213 770 11 22 33` | `Setif` | `0770112233` | `Sétif` |
| `0555 44 33 22` | `Wilaya de Béjaïa` | `0555443322` | `Béjaïa` |
| `12345` | `Tizi Ouzou` | — | *(sent to review: invalid phone)* |

A sample file is in [`examples/messy_orders.csv`](examples/messy_orders.csv).

### Options

| Option | Description |
|---|---|
| `-o, --output-dir` | Output folder (default: next to the input file) |
| `--phone-col NAME` | Phone column (auto-detected: `phone`, `tel`, `téléphone`, `هاتف`, …) |
| `--wilaya-col NAME` | Wilaya column (auto-detected: `wilaya`, `state`, `الولاية`, …) |
| `--dedupe-by KEYS` | What defines a duplicate, comma-separated. Default `phone`. Example: `phone,product` or `phone,wilaya` |
| `--wilaya-format` | `fr` (default), `ar`, or `code` (`16`) |
| `--international` | Write phones as `+213550123456` |
| `--add-code` | Add a `wilaya_code` column |
| `--encoding` | Force input encoding (CSV) |

> ⚠️ **About duplicates:** by default two rows with the same phone are duplicates. If the same customer may legitimately order different products, use `--dedupe-by phone,product`.

## Use as a library

```python
from dz_order_cleaner import clean_phone, match_wilaya

clean_phone("+213 550 12 34 56")   # ('0550123456', '')
match_wilaya("الجزاير").fr          # 'Alger'
```

## How it works

- **Phones:** strips symbols, converts Arabic digits, removes `+213`/`00213`/`(0)`, restores the leading `0`, then validates (mobile `05/06/07` + 8 digits, landline `02/03/04` + 7 digits). If a cell has several numbers (`a / b`), the first valid one is kept.
- **Wilayas:** text normalisation (accents, Arabic letter variants, `ال`, punctuation) → exact lookup in names + common aliases → fuzzy matching. If two wilayas are equally likely, the row is flagged instead of guessed.

## Roadmap

- [ ] Courier-specific export templates (Yalidine, ZR Express, Procolis…)
- [ ] Commune-level matching
- [ ] Simple web UI (drag & drop a file)

## Contributing

Found a spelling the tool misses? Add it to the `aliases` in [`wilayas.py`](dz_order_cleaner/wilayas.py) with a test in `tests/test_wilaya.py` and open a PR. Issues and ideas welcome.

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
