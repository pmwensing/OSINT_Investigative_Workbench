from datetime import datetime
from app.models.entity import Claim
from app.models.timeline import TimelineEvent


def build_timeline(db, investigation_id):
    claims = db.query(Claim).all()
    created = []

    for c in claims:
        # naive timestamp (use created_at for now)
        event_time = c.created_at or datetime.utcnow()

        event = TimelineEvent(
            investigation_id=investigation_id,
            source_type="claim",
            source_id=c.id,
            event_type=c.claim_type,
            title=f"Claim: {c.claim_type}",
            description=c.value,
            event_at=event_time
        )
        db.add(event)
        created.append(event)

    db.commit()
    return created
