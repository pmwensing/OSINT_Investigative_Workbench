from app.worker.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.job import Job
from app.models.entity import Entity, Claim, Artifact


@celery_app.task(name="app.worker.tasks.run_basic_email_scan")
def run_basic_email_scan(job_id: str, email: str, investigation_id: str):
    db = SessionLocal()

    job = db.query(Job).get(job_id)
    if not job:
        return

    try:
        job.status = "running"
        db.commit()

        # SIMULATED INTELLIGENCE OUTPUT
        entity = Entity(
            investigation_id=investigation_id,
            entity_type="email",
            value=email
        )
        db.add(entity)
        db.commit()
        db.refresh(entity)

        claim = Claim(
            entity_id=entity.id,
            claim_type="presence",
            value=f"Email {email} detected in OSINT scan",
            confidence="low"
        )
        db.add(claim)

        artifact = Artifact(
            investigation_id=investigation_id,
            artifact_type="scan_result",
            location="internal://email_scan",
            metadata=f"email={email}"
        )
        db.add(artifact)

        job.status = "completed"
        job.result_summary = f"Entity + claim created for {email}"
        db.commit()

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()

    finally:
        db.close()
