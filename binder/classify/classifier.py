from __future__ import annotations

import argparse
import csv
from pathlib import Path

from binder.classify.rules import classify_text


def classify_manifest(manifest_csv: str, out_csv: str) -> str:
    with open(manifest_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        Path(out_csv).write_text("", encoding="utf-8")
        return out_csv

    for row in rows:
        basis = " ".join([
            row.get("basename", ""),
            row.get("source_path", ""),
        ])
        row["category"] = classify_text(basis)

    fieldnames = list(rows[0].keys())
    if "category" not in fieldnames:
        fieldnames.append("category")

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return out_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(classify_manifest(args.manifest, args.out))


if __name__ == "__main__":
    main()
