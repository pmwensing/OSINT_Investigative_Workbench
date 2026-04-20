from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.review import AnalystReview, Alert
from app.services.alert_engine import create_alert

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/mark")
def mark_review(object_type: str, object_id: str, status: str, db: Session = Depends(get_db)):
    review = AnalystReview(object_type=object_type, object_id=object_id, status=status)
    db.add(review)
    db.commit()
    return {"status": "ok"}

@router.post("/alert")
def create_new_alert(investigation_id: str, title: str, db: Session = Depends(get_db)):
    alert = create_alert(db, investigation_id, "manual", title)
    return {"id": str(alert.id)}

@router.get("/alerts")
def list_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).all()
