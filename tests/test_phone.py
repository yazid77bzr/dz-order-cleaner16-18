import pytest
from dz_order_cleaner import clean_phone, to_international


@pytest.mark.parametrize("raw,expected", [
    ("0550123456", "0550123456"),
    ("550123456", "0550123456"),
    ("+213550123456", "0550123456"),
    ("+213 550 12 34 56", "0550123456"),
    ("+213 (0) 550 12 34 56", "0550123456"),
    ("00213550123456", "0550123456"),
    ("0550-12-34-56", "0550123456"),
    ("٠٧٧٠١١٢٢٣٣", "0770112233"),
    ("0550123456 / 0661234567", "0550123456"),
    ("021123456", "021123456"),          # landline
    (550123456.0, "0550123456"),          # Excel float
])
def test_valid(raw, expected):
    assert clean_phone(raw)[0] == expected


@pytest.mark.parametrize("raw", ["", None, "12345", "0850123456", "abc", "05501234"])
def test_invalid(raw):
    number, reason = clean_phone(raw)
    assert number is None and reason


def test_international():
    assert to_international("0550123456") == "+213550123456"
