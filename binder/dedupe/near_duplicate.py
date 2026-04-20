from __future__ import annotations

import argparse
import csv
from difflib import SequenceMatcher

from binder.schemas.exhibit_index import DuplicateGroupRow


def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def build_near_duplicate_groups(manifest_csv: str, out_csv: str) -> str:
    with open(manifest_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    groups = []
    used = set()

    for i, left in enumerate(rows):
        if i in used:
            continue

        members = [left["source_id"]]
        for j, right in enumerate(rows[i + 1:], start=i + 1):
            if j in used:
                continue

            same_ext = left.get("extension") == right.get("extension")
            size_l = int(left.get("size_bytes", 0) or 0)
            size_r = int(right.get("size_bytes", 0) or 0)
            size_close = abs(size_l - size_r) <= max(1024, int(size_l * 0.1) if size_l else 1024)
            name_close = sim(left.get("basename", ""), right.get("basename", "")) >= 0.85

            if same_ext and size_close and name_close and left.get("sha256") != right.get("sha256"):
                members.append(right["source_id"])
                used.add(j)

        if len(members) > 1:
            groups.append(DuplicateGroupRow(
                duplicate_group_id=f"near-{len(groups) + 1}",
                match_type="near",
                member_source_ids="|".join(members),
                preferred_source_id=members[0],
                reason="filename+size heuristic",
            ).to_dict())

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "duplicate_group_id", "match_type", "member_source_ids", "preferred_source_id", "reason"
        ])
        writer.writeheader()
        writer.writerows(groups)

    return out_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(build_near_duplicate_groups(args.manifest, args.out))


if __name__ == "__main__":
    main()
