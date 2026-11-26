import pytest
from dz_order_cleaner import WILAYAS, match_wilaya


def test_there_are_58_wilayas():
    assert len(WILAYAS) == 58
    assert [w.code for w in WILAYAS] == list(range(1, 59))


@pytest.mark.parametrize("raw,code", [
    ("Alger", 16), ("الجزائر", 16), ("الجزاير", 16), ("ALGIERS", 16),
    ("Wilaya de Béjaïa", 6), ("bejaia", 6), ("sétif", 19), ("setif", 19),
    ("وهران", 31), ("oran", 31), ("M'sila", 28), ("msila", 28),
    ("برج بوعريرج", 34), ("BBA", 34), ("ولاية باتنة", 5),
    ("16", 16), ("16 - Alger", 16), ("Constantina", 25),
    ("Tizi-Ouzou", 15), ("ain defla", 44), ("Ain Temouchent", 46),
    ("Mostaghanem", 27), ("tebessa", 12), ("جيجل", 18),
])
def test_matches(raw, code):
    assert match_wilaya(raw).code == code


@pytest.mark.parametrize("raw", ["", None, "Atlantis", "ain", "xx", "99"])
def test_no_match(raw):
    assert match_wilaya(raw) is None


def test_every_official_name_matches_itself():
    for w in WILAYAS:
        assert match_wilaya(w.fr).code == w.code
        assert match_wilaya(w.ar).code == w.code
