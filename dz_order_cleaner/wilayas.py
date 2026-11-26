"""The 58 Algerian wilayas (administrative division since 2021)."""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Wilaya:
    code: int
    fr: str
    ar: str
    aliases: Tuple[str, ...] = ()

    @property
    def code_str(self) -> str:
        return f"{self.code:02d}"


_RAW = [
    (1, "Adrar", "أدرار", ()),
    (2, "Chlef", "الشلف", ("ech cheliff", "el asnam")),
    (3, "Laghouat", "الأغواط", ("aghouat",)),
    (4, "Oum El Bouaghi", "أم البواقي", ("oum bouaghi", "oeb")),
    (5, "Batna", "باتنة", ()),
    (6, "Béjaïa", "بجاية", ("bgayet", "bougie", "bejaya")),
    (7, "Biskra", "بسكرة", ()),
    (8, "Béchar", "بشار", ()),
    (9, "Blida", "البليدة", ()),
    (10, "Bouira", "البويرة", ()),
    (11, "Tamanrasset", "تمنراست", ("tamanghasset", "tam")),
    (12, "Tébessa", "تبسة", ("tbessa",)),
    (13, "Tlemcen", "تلمسان", ("tilimsen",)),
    (14, "Tiaret", "تيارت", ()),
    (15, "Tizi Ouzou", "تيزي وزو", ("tizi", "tizi wezzu", "تيزيوزو")),
    (16, "Alger", "الجزائر", ("algiers", "algier", "alger centre", "dzair",
                              "el djazair", "الجزائر العاصمة", "الجزاير",
                              "جزائر العاصمة")),
    (17, "Djelfa", "الجلفة", ()),
    (18, "Jijel", "جيجل", ("djidjelli",)),
    (19, "Sétif", "سطيف", ("stif",)),
    (20, "Saïda", "سعيدة", ()),
    (21, "Skikda", "سكيكدة", ()),
    (22, "Sidi Bel Abbès", "سيدي بلعباس", ("sba", "sidi belabbes", "سيدي بل عباس")),
    (23, "Annaba", "عنابة", ("bone",)),
    (24, "Guelma", "قالمة", ()),
    (25, "Constantine", "قسنطينة", ("qacentina", "constantina")),
    (26, "Médéa", "المدية", ("media",)),
    (27, "Mostaganem", "مستغانم", ("mosta",)),
    (28, "M'Sila", "المسيلة", ("msila",)),
    (29, "Mascara", "معسكر", ()),
    (30, "Ouargla", "ورقلة", ("wargla",)),
    (31, "Oran", "وهران", ("wahran",)),
    (32, "El Bayadh", "البيض", ("bayadh",)),
    (33, "Illizi", "إليزي", ("ilizi",)),
    (34, "Bordj Bou Arréridj", "برج بوعريريج", ("bba", "bordj bou arreridj",
                                                  "bordj", "برج بو عريريج", "برج")),
    (35, "Boumerdès", "بومرداس", ("boumerdes",)),
    (36, "El Tarf", "الطارف", ("tarf",)),
    (37, "Tindouf", "تندوف", ()),
    (38, "Tissemsilt", "تيسمسيلت", ()),
    (39, "El Oued", "الوادي", ("oued souf", "eloued")),
    (40, "Khenchela", "خنشلة", ()),
    (41, "Souk Ahras", "سوق أهراس", ()),
    (42, "Tipaza", "تيبازة", ("tipasa",)),
    (43, "Mila", "ميلة", ()),
    (44, "Aïn Defla", "عين الدفلى", ("ain dafla",)),
    (45, "Naâma", "النعامة", ("naama",)),
    (46, "Aïn Témouchent", "عين تموشنت", ("ain tmouchent", "عين تيموشنت")),
    (47, "Ghardaïa", "غرداية", ("gherdaia",)),
    (48, "Relizane", "غليزان", ("ghilizane",)),
    (49, "El M'Ghair", "المغير", ("el meghair", "elmghair")),
    (50, "El Menia", "المنيعة", ("el meniaa", "elmenia")),
    (51, "Ouled Djellal", "أولاد جلال", ()),
    (52, "Bordj Badji Mokhtar", "برج باجي مختار", ("bbm",)),
    (53, "Béni Abbès", "بني عباس", ()),
    (54, "Timimoun", "تيميمون", ()),
    (55, "Touggourt", "تقرت", ("tougourt",)),
    (56, "Djanet", "جانت", ()),
    (57, "In Salah", "عين صالح", ("ain salah",)),
    (58, "In Guezzam", "عين قزام", ("ain guezzam",)),
]

WILAYAS = tuple(Wilaya(*row) for row in _RAW)
BY_CODE = {w.code: w for w in WILAYAS}
assert len(WILAYAS) == 58
