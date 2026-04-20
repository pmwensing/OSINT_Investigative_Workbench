from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.job import Job
from app.worker.tasks import run_basic_email_scan

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/email_scan")
def trigger_email_scan(investigation_id: str, email: str, db: Session = Depends(get_db)):
    job = Job(
        investigation_id=investigation_id,
        connector="email_basic",
        status="queued"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    run_basic_email_scan.delay(str(job.id), email, investigation_id)

    return {"job_id": str(job.id), "status": "queued"}
