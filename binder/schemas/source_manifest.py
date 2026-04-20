from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class SourceManifestRow:
    source_id: str
    source_path: str
    basename: str
    extension: str
    mime_type: str
    size_bytes: int
    sha256: str
    page_count: Optional[int]
    discovered_at: str
    scan_root: str
    ingest_status: str = "ok"

    def to_dict(self) -> dict:
        return asdict(self)
