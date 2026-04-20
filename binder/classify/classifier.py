from __future__ import annotations
import csv
from pathlib import Path
from binder.classify.rules import classify_text

def infer_title(basename: str) -> str:
    stem = Path(basename).stem.replace("_", " ").replace("-", " ").strip()
    return " ".join(w.capitalize() for w in stem.split()) or basename

def packet_flags_for(category: str) -> str:
    flags = ["full"]
    if category in {"A_CHRONOLOGY","D_FIRE","E_LOCKOUT","F_FINANCIAL"}:
        flags.append("adjudicator")
    if category != "Z_UNCLASSIFIED":
        flags.append("disclosure")
    return ",".join(flags)

def classify_manifest(manifest_csv: str | Path) -> list[dict]:
    rows = []
    with Path(manifest_csv).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category, subcategory = classify_text(row["basename"], row["source_path"])
            row["category"] = category
            row["subcategory"] = subcategory
            row["title"] = infer_title(row["basename"])
            row["packet_flags"] = packet_flags_for(category)
            rows.append(row)
    return rows
