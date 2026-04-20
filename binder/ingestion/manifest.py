from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterable
from binder.schemas.source_manifest import SourceManifestRow

MANIFEST_HEADERS = [
    "source_id","source_path","basename","extension","mime_type","size_bytes",
    "sha256","page_count","discovered_at","scan_root","ingest_status"
]

def write_manifest(rows: Iterable[SourceManifestRow], out_csv: str | Path) -> Path:
    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_dict())
    return out_path
