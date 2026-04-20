from __future__ import annotations
from difflib import SequenceMatcher
from pathlib import Path

def _name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def near_duplicate_groups(rows: list[dict], existing_source_to_group: dict[str, str]) -> tuple[list[dict], dict[str, str]]:
    groups = []
    source_to_group = dict(existing_source_to_group)
    group_num = 1

    candidates = [r for r in rows if r["source_id"] not in source_to_group]
    used = set()

    for i, left in enumerate(candidates):
        if left["source_id"] in used:
            continue
        cluster = [left]
        left_name = Path(left["basename"]).stem
        left_pages = int(left.get("page_count") or 0)
        left_size = int(left.get("size_bytes") or 0)

        for right in candidates[i+1:]:
            if right["source_id"] in used:
                continue
            right_name = Path(right["basename"]).stem
            sim = _name_similarity(left_name, right_name)
            right_pages = int(right.get("page_count") or 0)
            right_size = int(right.get("size_bytes") or 0)
            size_ratio = (min(left_size, right_size) / max(left_size, right_size)) if left_size and right_size else 0.0
            page_match = (left_pages == right_pages and left_pages != 0)

            if sim >= 0.82 and (size_ratio >= 0.85 or page_match):
                cluster.append(right)

        if len(cluster) > 1:
            gid = f"DG-NEAR-{group_num:04d}"
            group_num += 1
            preferred = sorted(cluster, key=lambda r: (int(r.get("page_count") or 0), int(r.get("size_bytes") or 0)), reverse=True)[0]
            for m in cluster:
                used.add(m["source_id"])
                source_to_group[m["source_id"]] = gid
            groups.append({
                "duplicate_group_id": gid,
                "match_type": "near",
                "member_source_ids": ",".join(m["source_id"] for m in cluster),
                "preferred_source_id": preferred["source_id"],
                "reason": "Filename/page-count/size similarity heuristic",
            })
    return groups, source_to_group
