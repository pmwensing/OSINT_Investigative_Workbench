from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.contradiction import Contradiction
from app.services.contradiction_engine import detect_simple_contradictions

router = APIRouter(prefix="/contradictions", tags=["contradictions"])

@router.post("/run")
def run_detection(investigation_id: str, db: Session = Depends(get_db)):
    created = detect_simple_contradictions(db, investigation_id)
    return {"created": len(created)}

@router.get("/")
def list_contradictions(db: Session = Depends(get_db)):
    return db.query(Contradiction).all()
