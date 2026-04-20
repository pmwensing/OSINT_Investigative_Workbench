from __future__ import annotations

import argparse
import csv
import uuid
from pathlib import Path


def build_master_index(manifest_csv: str, out_dir: str) -> str:
    out_file = Path(out_dir) / "MASTER_EXHIBIT_INDEX.csv"

    with open(manifest_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "exhibit_id", "title", "source_id", "source_path", "category", "sha256"
        ])
        writer.writeheader()

        for r in rows:
            writer.writerow({
                "exhibit_id": str(uuid.uuid4()),
                "title": r.get("basename", ""),
                "source_id": r.get("source_id", ""),
                "source_path": r.get("source_path", ""),
                "category": r.get("category", "Z_UNCLASSIFIED"),
                "sha256": r.get("sha256", ""),
            })

    return str(out_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(build_master_index(args.manifest, args.out))


if __name__ == "__main__":
    main()
