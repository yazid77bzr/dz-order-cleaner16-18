import pytest
from dz_order_cleaner import clean_rows

H = ["name", "phone", "wilaya", "product"]


def rows(*r):
    return [dict(zip(H, x)) for x in r]


def test_split_clean_review_duplicates():
    data = rows(
        ("A", "+213 550 12 34 56", "Alger", "x"),
        ("B", "550123456", "الجزاير", "x"),        # duplicate of A
        ("C", "123", "Oran", "x"),                   # bad phone
        ("D", "0661234567", "Atlantis", "x"),        # bad wilaya
        ("E", "0770112233", "Setif", "x"),
    )
    res = clean_rows(data, H)
    assert [r["name"] for r in res.clean] == ["A", "E"]
    assert res.clean[0]["phone"] == "0550123456"
    assert res.clean[0]["wilaya"] == "Alger"
    assert [r["name"] for r in res.duplicates] == ["B"]
    assert res.duplicates[0]["duplicate_of_row"] == 2
    assert [r["name"] for r in res.review] == ["C", "D"]


def test_dedupe_by_phone_and_product():
    data = rows(("A", "0550123456", "Alger", "shirt"),
                ("B", "0550123456", "Alger", "watch"))
    assert len(clean_rows(data, H, dedupe_by=["phone"]).duplicates) == 1
    assert len(clean_rows(data, H, dedupe_by=["phone", "product"]).duplicates) == 0


def test_options():
    data = rows(("A", "0550123456", "Alger", "x"))
    res = clean_rows(data, H, international=True, wilaya_format="ar", add_code=True)
    r = res.clean[0]
    assert (r["phone"], r["wilaya"], r["wilaya_code"]) == ("+213550123456", "الجزائر", "16")


def test_missing_columns():
    with pytest.raises(ValueError):
        clean_rows([{"a": "1"}], ["a"])
