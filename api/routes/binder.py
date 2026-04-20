from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import Investigation, Job, Artifact, User
from api.deps.auth import get_current_user
from worker.celery_app import celery_app

router = APIRouter(tags=["binder"])


def queue_binder_job(db: Session, investigation_id: UUID, connector: str) -> Job:
    job = Job(
        investigation_id=investigation_id,
        target_id=None,
        connector=connector,
        status="queued",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.post("/investigations/{investigation_id}/binder/scan")
def binder_scan(
    investigation_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = db.get(Investigation, investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    roots = payload.get("roots", [])
    if not roots:
        raise HTTPException(status_code=400, detail="roots required")

    job = queue_binder_job(db, investigation_id, "binder_scan")
    celery_app.send_task("worker.tasks.binder_tasks.run_binder_scan", args=[str(job.id), roots])
    return {"job_id": str(job.id), "status": "queued"}


@router.post("/investigations/{investigation_id}/binder/classify")
def binder_classify(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = db.get(Investigation, investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    job = queue_binder_job(db, investigation_id, "binder_classify")
    celery_app.send_task("worker.tasks.binder_tasks.run_binder_classify", args=[str(job.id)])
    return {"job_id": str(job.id), "status": "queued"}


@router.post("/investigations/{investigation_id}/binder/dedupe")
def binder_dedupe(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = db.get(Investigation, investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    job = queue_binder_job(db, investigation_id, "binder_dedupe")
    celery_app.send_task("worker.tasks.binder_tasks.run_binder_dedupe", args=[str(job.id)])
    return {"job_id": str(job.id), "status": "queued"}


@router.post("/investigations/{investigation_id}/binder/build-indexes")
def binder_build_indexes(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = db.get(Investigation, investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    job = queue_binder_job(db, investigation_id, "binder_build_indexes")
    celery_app.send_task("worker.tasks.binder_tasks.run_binder_build_indexes", args=[str(job.id)])
    return {"job_id": str(job.id), "status": "queued"}


@router.get("/investigations/{investigation_id}/binder/artifacts")
def binder_artifacts(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = list(db.scalars(
        select(Artifact)
        .where(Artifact.investigation_id == investigation_id)
        .where(Artifact.artifact_type.like("binder_%"))
        .order_by(Artifact.created_at.desc())
    ))
    return [
        {
            "id": str(a.id),
            "artifact_type": a.artifact_type,
            "bucket": a.bucket,
            "object_key": a.object_key,
            "content_type": a.content_type,
            "created_at": a.created_at.isoformat(),
        }
        for a in rows
    ]
