from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import TimelineEvent, Contradiction, User
from api.deps.auth import get_current_user

router = APIRouter(tags=["timeline"])

@router.get("/investigations/{investigation_id}/timeline")
def get_timeline(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    events = list(db.scalars(select(TimelineEvent).where(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_time.asc())))
    contradictions = list(db.scalars(select(Contradiction).where(Contradiction.investigation_id == investigation_id)))
    return {
        "events": [
            {
                "id": str(e.id),
                "event_time": e.event_time.isoformat(),
                "title": e.title,
                "description": e.description,
                "event_type": e.event_type,
            }
            for e in events
        ],
        "contradictions": [
            {"id": str(c.id), "left_claim_id": str(c.left_claim_id), "right_claim_id": str(c.right_claim_id), "reason": c.reason, "score": c.score}
            for c in contradictions
        ],
    }
