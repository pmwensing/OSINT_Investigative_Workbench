def normalize_value(observable_type: str, value: str) -> str:
    v = value.strip()
    if observable_type in {"email", "domain", "hostname"}:
        return v.lower()
    return v
