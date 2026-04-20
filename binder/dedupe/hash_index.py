from __future__ import annotations

import argparse
import csv
from collections import defaultdict

from binder.schemas.exhibit_index import DuplicateGroupRow


def build_hash_index(manifest_csv: str) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    with open(manifest_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            groups[row["sha256"]].append(row)
    return groups


def write_exact_duplicate_groups(manifest_csv: str, out_csv: str) -> str:
    groups = build_hash_index(manifest_csv)
    rows = []
    counter = 1

    for sha, members in groups.items():
        if len(members) < 2:
            continue
        rows.append(DuplicateGroupRow(
            duplicate_group_id=f"exact-{counter}",
            match_type="exact",
            member_source_ids="|".join(m["source_id"] for m in members),
            preferred_source_id=members[0]["source_id"],
            reason=f"sha256:{sha}",
        ).to_dict())
        counter += 1

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "duplicate_group_id", "match_type", "member_source_ids", "preferred_source_id", "reason"
        ])
        writer.writeheader()
        writer.writerows(rows)

    return out_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(write_exact_duplicate_groups(args.manifest, args.out))


if __name__ == "__main__":
    main()
