from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import mimetypes
import os
import uuid
from pathlib import Path

from binder.schemas.source_manifest import SourceManifestRow


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def detect_page_count(path: Path):
    # starter-safe: no PDF parsing dependency required
    if path.suffix.lower() == ".pdf":
        return None
    return None


def build_row(path: Path, scan_root: str) -> SourceManifestRow:
    mime_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return SourceManifestRow(
        source_id=str(uuid.uuid4()),
        source_path=str(path),
        basename=path.name,
        extension=path.suffix.lower(),
        mime_type=mime_type,
        size_bytes=path.stat().st_size,
        sha256=sha256_file(path),
        page_count=detect_page_count(path),
        discovered_at=dt.datetime.utcnow().isoformat(),
        scan_root=scan_root,
        ingest_status="ok",
    )


def run_scan(roots: list[str], out_dir: str | Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "SOURCE_MANIFEST.csv"

    rows: list[SourceManifestRow] = []

    for root in roots:
        root_path = Path(root)
        if not root_path.exists():
            continue
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                path = Path(dirpath) / filename
                try:
                    rows.append(build_row(path, str(root_path)))
                except Exception:
                    continue

    fieldnames = list(SourceManifestRow.__dataclass_fields__.keys())
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_dict())

    return manifest_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", action="append", required=True, dest="roots")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    manifest = run_scan(args.roots, args.out)
    print(manifest)


if __name__ == "__main__":
    main()
