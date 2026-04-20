CATEGORY_RULES = {
    "A_CHRONOLOGY": ["timeline", "chronology", "sequence", "events", "history"],
    "B_MAINTENANCE": ["maintenance", "repair", "appliance", "heat", "mould", "mold"],
    "C_PEST": ["pest", "bedbug", "roach", "rats", "mice", "infestation"],
    "D_FIRE": ["fire", "smoke", "alarm", "ofm", "esa", "electrical"],
    "E_LOCKOUT": ["lockout", "access", "key", "entry", "denied", "possession"],
    "F_FINANCIAL": ["receipt", "invoice", "hotel", "motel", "rent", "expense", "compensation", "financial"],
}


def classify_text(text: str) -> str:
    lower = text.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(word in lower for word in keywords):
            return category
    return "Z_UNCLASSIFIED"
