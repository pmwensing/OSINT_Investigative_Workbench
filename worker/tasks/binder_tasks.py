from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
import tempfile

from api.core.config import settings
from api.db.models import Artifact, Job
from api.db.session import SessionLocal
from binder.classify.classifier import classify_manifest
from binder.dedupe.hash_index import write_exact_duplicate_groups
from binder.dedupe.near_duplicate import build_near_duplicate_groups
from binder.index.build_curated_indexes import build_curated_indexes
from binder.index.build_master_index import build_master_index
from binder.ingestion.scan_sources import run_scan
from shared.storage import get_minio_client, put_json_bytes
from worker.celery_app import celery_app


def _upload_file_and_register(db, job, path: Path, artifact_type: str):
    client = get_minio_client()
    raw = path.read_bytes()
    key = f"investigation/{job.investigation_id}/binder/{path.name}"
    put_json_bytes(client, settings.minio_bucket_artifacts, key, raw, content_type="text/csv")
    db.add(Artifact(
        investigation_id=job.investigation_id,
        job_id=job.id,
        artifact_type=artifact_type,
        bucket=settings.minio_bucket_artifacts,
        object_key=key,
        content_type="text/csv",
    ))


def _start_job(db, job: Job):
    job.status = "running"
    job.started_at = datetime.now(timezone.utc)
    db.commit()


def _finish_job(db, job: Job):
    job.status = "completed"
    job.finished_at = datetime.now(timezone.utc)
    db.commit()


def _fail_job(db, job_id: str, error: Exception):
    job = db.get(Job, UUID(job_id))
    if job:
        job.status = "failed"
        job.error_message = str(error)
        job.finished_at = datetime.now(timezone.utc)
        db.commit()


def _latest_binder_artifact_path_name(db, investigation_id, artifact_type: str) -> str | None:
    rows = [
        a for a in db.query(Artifact)
        .filter(Artifact.investigation_id == investigation_id)
        .filter(Artifact.artifact_type == artifact_type)
        .order_by(Artifact.created_at.desc())
        .all()
    ]
    if not rows:
        return None
    return Path(rows[0].object_key).name


@celery_app.task(name="worker.tasks.binder_tasks.run_binder_scan")
def run_binder_scan(job_id: str, roots: list[str]) -> dict:
    db = SessionLocal()
    try:
        job = db.get(Job, UUID(job_id))
        _start_job(db, job)

        workdir = Path(tempfile.mkdtemp(prefix="binder_scan_"))
        manifest = run_scan(roots=roots, out_dir=workdir)
        _upload_file_and_register(db, job, manifest, "binder_source_manifest")

        _finish_job(db, job)
        return {"status": "completed", "job_id": job_id}
    except Exception as exc:
        db.rollback()
        _fail_job(db, job_id, exc)
        raise
    finally:
        db.close()


@celery_app.task(name="worker.tasks.binder_tasks.run_binder_classify")
def run_binder_classify(job_id: str) -> dict:
    db = SessionLocal()
    try:
        job = db.get(Job, UUID(job_id))
        _start_job(db, job)

        manifest_name = _latest_binder_artifact_path_name(db, job.investigation_id, "binder_source_manifest")
        if not manifest_name:
            raise RuntimeError("No binder_source_manifest artifact found")

        # starter-safe local staging assumption
        workdir = Path(tempfile.mkdtemp(prefix="binder_classify_"))
        local_manifest = workdir / "SOURCE_MANIFEST.csv"
        raise RuntimeError("Classification requires local staging of SOURCE_MANIFEST.csv from artifact store")

    except Exception as exc:
        db.rollback()
        _fail_job(db, job_id, exc)
        raise
    finally:
        db.close()


@celery_app.task(name="worker.tasks.binder_tasks.run_binder_dedupe")
def run_binder_dedupe(job_id: str) -> dict:
    db = SessionLocal()
    try:
        job = db.get(Job, UUID(job_id))
        _start_job(db, job)
        raise RuntimeError("Dedupe wiring requires local staging of classified manifest from artifact store")
    except Exception as exc:
        db.rollback()
        _fail_job(db, job_id, exc)
        raise
    finally:
        db.close()


@celery_app.task(name="worker.tasks.binder_tasks.run_binder_build_indexes")
def run_binder_build_indexes(job_id: str) -> dict:
    db = SessionLocal()
    try:
        job = db.get(Job, UUID(job_id))
        _start_job(db, job)
        raise RuntimeError("Index build wiring requires local staging of classified manifest from artifact store")
    except Exception as exc:
        db.rollback()
        _fail_job(db, job_id, exc)
        raise
    finally:
        db.close()
