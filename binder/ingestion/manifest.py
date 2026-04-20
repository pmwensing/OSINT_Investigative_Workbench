from __future__ import annotations

from pathlib import Path


def manifest_path(out_dir: str | Path) -> Path:
    return Path(out_dir) / "SOURCE_MANIFEST.csv"
