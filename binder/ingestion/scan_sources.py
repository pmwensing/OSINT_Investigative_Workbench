import hashlib, os, csv, uuid, datetime
from pathlib import Path
from binder.schemas.source_manifest import SourceManifestRow

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def run_scan(roots, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "SOURCE_MANIFEST.csv"

    rows = []

    for root in roots:
        for dirpath, _, files in os.walk(root):
            for f in files:
                p = Path(dirpath) / f
                try:
                    row = SourceManifestRow(
                        source_id=str(uuid.uuid4()),
                        source_path=str(p),
                        basename=p.name,
                        extension=p.suffix,
                        mime_type="unknown",
                        size_bytes=p.stat().st_size,
                        sha256=sha256_file(p),
                        page_count=None,
                        discovered_at=str(datetime.datetime.utcnow()),
                        scan_root=root,
                    )
                    rows.append(row)
                except Exception:
                    continue

    with open(manifest_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].to_dict().keys())
        writer.writeheader()
        for r in rows:
            writer.writerow(r.to_dict())

    return manifest_path
