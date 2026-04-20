from __future__ import annotations
import argparse, csv
from pathlib import Path

from binder.classify.classifier import classify_manifest
from binder.dedupe.hash_index import exact_duplicate_groups
from binder.dedupe.near_duplicate import near_duplicate_groups

MASTER_HEADERS = [
    "exhibit_id","title","source_id","source_path","category","subcategory",
    "packet_flags","sha256","duplicate_group_id","canonical_preferred","notes"
]
DUP_HEADERS = [
    "duplicate_group_id","match_type","member_source_ids","preferred_source_id","reason"
]

def build_master_rows(manifest_csv: str | Path) -> tuple[list[dict], list[dict]]:
    classified = classify_manifest(manifest_csv)
    exact_groups, source_to_group = exact_duplicate_groups(classified)
    near_groups, source_to_group = near_duplicate_groups(classified, source_to_group)
    all_groups = exact_groups + near_groups

    preferred_by_group = {g["duplicate_group_id"]: g["preferred_source_id"] for g in all_groups}

    counters = {}
    master_rows = []
    for row in classified:
        category = row["category"]
        counters.setdefault(category, 0)
        counters[category] += 1
        exhibit_id = f"{category}-{counters[category]:03d}"
        group_id = source_to_group.get(row["source_id"], "")
        preferred = preferred_by_group.get(group_id, row["source_id"])
        canonical_preferred = "yes" if preferred == row["source_id"] else "no"
        notes = ""
        if row["category"] == "Z_UNCLASSIFIED":
            notes = "review classification"

        master_rows.append({
            "exhibit_id": exhibit_id,
            "title": row["title"],
            "source_id": row["source_id"],
            "source_path": row["source_path"],
            "category": row["category"],
            "subcategory": row["subcategory"],
            "packet_flags": row["packet_flags"],
            "sha256": row["sha256"],
            "duplicate_group_id": group_id,
            "canonical_preferred": canonical_preferred,
            "notes": notes,
        })
    return master_rows, all_groups

def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    master_rows, duplicate_rows = build_master_rows(args.manifest)
    write_csv(out / "MASTER_EXHIBIT_INDEX.csv", MASTER_HEADERS, master_rows)
    write_csv(out / "DUPLICATE_GROUPS.csv", DUP_HEADERS, duplicate_rows)

    print(f"Wrote {out / 'MASTER_EXHIBIT_INDEX.csv'}")
    print(f"Wrote {out / 'DUPLICATE_GROUPS.csv'}")
    print(f"Master rows: {len(master_rows)}")
    print(f"Duplicate groups: {len(duplicate_rows)}")

if __name__ == "__main__":
    main()
