from __future__ import annotations
import argparse, hashlib, mimetypes, os, uuid
from datetime import datetime, timezone
from pathlib import Path
from binder.schemas.source_manifest import SourceManifestRow
from binder.ingestion.manifest import write_manifest

ALLOWED_EXTS = {
    ".pdf",".png",".jpg",".jpeg",".webp",".txt",".csv",".json",".eml",".msg",".mp4",".mov",".avi"
}

def sha256_file(path: Path, chunk_size: int = 1024*1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def guess_page_count(path: Path) -> int:
    if path.suffix.lower() != ".pdf":
        return 0
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except Exception:
        return 0

def scan_root(root: Path):
    discovered_at = datetime.now(timezone.utc).isoformat()
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            p = Path(dirpath) / filename
            ext = p.suffix.lower()
            if ext not in ALLOWED_EXTS:
                continue
            mime_type = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
            try:
                size_bytes = p.stat().st_size
                digest = sha256_file(p)
                page_count = guess_page_count(p)
                yield SourceManifestRow(
                    source_id=str(uuid.uuid4()),
                    source_path=str(p.resolve()),
                    basename=p.name,
                    extension=ext,
                    mime_type=mime_type,
                    size_bytes=size_bytes,
                    sha256=digest,
                    page_count=page_count,
                    discovered_at=discovered_at,
                    scan_root=str(root.resolve()),
                    ingest_status="ok",
                )
            except Exception:
                yield SourceManifestRow(
                    source_id=str(uuid.uuid4()),
                    source_path=str(p.resolve()),
                    basename=p.name,
                    extension=ext,
                    mime_type=mime_type,
                    size_bytes=0,
                    sha256="",
                    page_count=0,
                    discovered_at=discovered_at,
                    scan_root=str(root.resolve()),
                    ingest_status="error",
                )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    rows = list(scan_root(root))
    manifest_path = write_manifest(rows, out / "SOURCE_MANIFEST.csv")
    print(f"Wrote manifest: {manifest_path}")
    print(f"Rows: {len(rows)}")

if __name__ == "__main__":
    main()
