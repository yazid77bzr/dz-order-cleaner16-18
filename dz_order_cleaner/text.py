"""Text normalisation helpers (Arabic + French/Latin)."""
import re
import unicodedata

# Arabic-Indic and Persian digits -> ASCII digits
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_TASHKEEL = re.compile(r"[\u064B-\u065F\u0670\u0640]")  # diacritics + tatweel
_AR_MAP = str.maketrans(
    {"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"}
)


def normalize(text) -> str:
    """Lowercase, strip accents/diacritics, unify Arabic letter variants,
    drop punctuation and collapse whitespace."""
    s = str(text).translate(AR_DIGITS)
    s = _TASHKEEL.sub("", s)
    s = s.translate(_AR_MAP)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"['’`´]", "", s)          # m'sila -> msila
    s = re.sub(r"[\W_]+", " ", s)          # punctuation -> space
    return re.sub(r"\s+", " ", s).strip()
