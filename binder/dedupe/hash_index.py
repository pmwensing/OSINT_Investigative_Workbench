from __future__ import annotations
from collections import defaultdict

def exact_duplicate_groups(rows: list[dict]) -> tuple[list[dict], dict[str, str]]:
    by_hash = defaultdict(list)
    for row in rows:
        if row.get("sha256"):
            by_hash[row["sha256"]].append(row)

    groups = []
    source_to_group = {}
    group_num = 1
    for digest, members in by_hash.items():
        if len(members) < 2:
            continue
        preferred = sorted(members, key=lambda r: (int(r.get("page_count") or 0), int(r.get("size_bytes") or 0)), reverse=True)[0]
        gid = f"DG-EXACT-{group_num:04d}"
        group_num += 1
        for m in members:
            source_to_group[m["source_id"]] = gid
        groups.append({
            "duplicate_group_id": gid,
            "match_type": "exact",
            "member_source_ids": ",".join(m["source_id"] for m in members),
            "preferred_source_id": preferred["source_id"],
            "reason": f"Same SHA-256: {digest}",
        })
    return groups, source_to_group
