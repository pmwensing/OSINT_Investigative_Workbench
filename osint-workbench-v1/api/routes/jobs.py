from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import Job, Investigation, Target, User
from api.schemas.job import JobCreate, JobOut
from api.deps.auth import get_current_user
from worker.celery_app import celery_app

router = APIRouter(tags=["jobs"])

@router.post("/investigations/{investigation_id}/jobs", response_model=list[JobOut])
def create_jobs(
    investigation_id: UUID,
    payload: JobCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = db.get(Investigation, investigation_id)
    target = db.get(Target, payload.target_id)
    if not inv or not target or target.investigation_id != investigation_id:
        raise HTTPException(status_code=404, detail="Invalid investigation or target")
    if not payload.connectors:
        raise HTTPException(status_code=400, detail="At least one connector is required")

    created = []
    for connector in payload.connectors:
        job = Job(
            investigation_id=investigation_id,
            target_id=payload.target_id,
            connector=connector,
            status="queued",
            queued_at=datetime.now(timezone.utc),
        )
        db.add(job)
        db.flush()
        created.append(job)
    db.commit()
    for job in created:
        celery_app.send_task("worker.tasks.run_job", args=[str(job.id)])
    for job in created:
        db.refresh(job)
    return created

@router.get("/investigations/{investigation_id}/jobs", response_model=list[JobOut])
def list_jobs(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list(db.scalars(select(Job).where(Job.investigation_id == investigation_id).order_by(Job.queued_at.desc())))
