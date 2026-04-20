from __future__ import annotations

CATEGORY_RULES = [
    ("A_CHRONOLOGY", ["timeline", "chronology", "chronological"]),
    ("B_MAINTENANCE", ["maintenance", "repair", "heat", "appliance", "mould", "mold"]),
    ("C_PEST", ["pest", "bedbug", "bed bug", "roach", "rat", "mouse", "mice"]),
    ("D_FIRE", ["fire", "smoke", "alarm", "esa", "electrical", "inspection"]),
    ("E_LOCKOUT", ["lockout", "access", "entry", "key", "door", "possession"]),
    ("F_FINANCIAL", ["expense", "receipt", "hotel", "motel", "rent", "financial", "compensation"]),
]

def classify_text(*parts: str) -> tuple[str, str]:
    haystack = " ".join(p for p in parts if p).lower()
    for category, keywords in CATEGORY_RULES:
        for kw in keywords:
            if kw in haystack:
                return category, kw
    return "Z_UNCLASSIFIED", ""
