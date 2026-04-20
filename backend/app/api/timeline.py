from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.timeline import TimelineEvent
from app.services.timeline_engine import build_timeline

router = APIRouter(prefix="/timeline", tags=["timeline"])

@router.post("/build")
def run_timeline(investigation_id: str, db: Session = Depends(get_db)):
    created = build_timeline(db, investigation_id)
    return {"created": len(created)}

@router.get("/")
def get_timeline(db: Session = Depends(get_db)):
    return db.query(TimelineEvent).order_by(TimelineEvent.event_at).all()
