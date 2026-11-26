"""dz-order-cleaner: clean Algerian e-commerce order files."""

from .cleaner import CleanResult, clean_rows
from .phone import clean_phone, to_international
from .wilaya import match_wilaya
from .wilayas import WILAYAS, Wilaya

__all__ = [
    "CleanResult", "clean_rows", "clean_phone", "to_international",
    "match_wilaya", "WILAYAS", "Wilaya",
]
__version__ = "0.1.0"
