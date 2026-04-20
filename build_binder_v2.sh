#!/usr/bin/env bash
set -e

mkdir -p binder/{ingestion,classify,dedupe,index,schemas}
mkdir -p api/routes
mkdir -p worker/tasks
mkdir -p alembic/versions

# -------------------------
# SOURCE MANIFEST SCHEMA
# -------------------------
cat <<'PY' > binder/schemas/source_manifest.py
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

    def to_dict(self):
        return asdict(self)
PY

# -------------------------
# EXHIBIT INDEX SCHEMA
# -------------------------
cat <<'PY' > binder/schemas/exhibit_index.py
from dataclasses import dataclass, asdict

@dataclass
class ExhibitIndexRow:
    exhibit_id: str
    title: str
    source_path: str
    category: str
    sha256: str

    def to_dict(self):
        return asdict(self)
PY

# -------------------------
# SCAN SOURCES
# -------------------------
cat <<'PY' > binder/ingestion/scan_sources.py
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
PY

# -------------------------
# HASH DEDUPE
# -------------------------
cat <<'PY' > binder/dedupe/hash_index.py
import csv
from collections import defaultdict

def build_hash_index(manifest_csv):
    groups = defaultdict(list)

    with open(manifest_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            groups[row["sha256"]].append(row)

    return groups
PY

# -------------------------
# MASTER INDEX
# -------------------------
cat <<'PY' > binder/index/build_master_index.py
import csv, uuid

def build_master_index(manifest_csv, out_dir):
    out_file = f"{out_dir}/MASTER_EXHIBIT_INDEX.csv"

    with open(manifest_csv) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(out_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "exhibit_id","title","source_path","category","sha256"
        ])
        writer.writeheader()

        for r in rows:
            writer.writerow({
                "exhibit_id": str(uuid.uuid4()),
                "title": r["basename"],
                "source_path": r["source_path"],
                "category": "Z_UNCLASSIFIED",
                "sha256": r["sha256"]
            })

    return out_file
PY

# -------------------------
# FASTAPI ROUTE
# -------------------------
cat <<'PY' > api/routes/binder.py
from fastapi import APIRouter

router = APIRouter(tags=["binder"])

@router.get("/binder/health")
def binder_health():
    return {"status": "ok"}
PY

# -------------------------
# CELERY TASK
# -------------------------
cat <<'PY' > worker/tasks/binder_tasks.py
from worker.celery_app import celery_app

@celery_app.task(name="binder.test")
def binder_test():
    return "binder working"
PY

# -------------------------
# ALEMBIC PATCH
# -------------------------
cat <<'PY' > alembic/versions/0002_jobs_target_nullable.py
def upgrade():
    pass

def downgrade():
    pass
PY

echo "Binder v2.0 scaffold built."
