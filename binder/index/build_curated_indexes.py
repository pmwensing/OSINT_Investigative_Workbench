from __future__ import annotations

import argparse
import csv
from pathlib import Path

DISCLOSURE_CATS = {"A_CHRONOLOGY", "B_MAINTENANCE", "C_PEST", "D_FIRE", "E_LOCKOUT", "F_FINANCIAL"}
ADJUDICATOR_CATS = {"A_CHRONOLOGY", "D_FIRE", "E_LOCKOUT", "F_FINANCIAL"}


def build_curated_indexes(master_csv: str, out_dir: str) -> dict:
    with open(master_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    disclosure = [r for r in rows if r.get("category") in DISCLOSURE_CATS]
    adjudicator = [r for r in rows if r.get("category") in ADJUDICATOR_CATS]

    disclosure_path = out / "DISCLOSURE_EXHIBIT_INDEX.csv"
    adjudicator_path = out / "ADJUDICATOR_EXHIBIT_INDEX.csv"

    fieldnames = rows[0].keys() if rows else []

    for path, subset in ((disclosure_path, disclosure), (adjudicator_path, adjudicator)):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(subset)

    return {
        "disclosure": str(disclosure_path),
        "adjudicator": str(adjudicator_path),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(build_curated_indexes(args.master, args.out))


if __name__ == "__main__":
    main()
