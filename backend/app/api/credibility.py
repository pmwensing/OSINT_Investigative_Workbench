from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.credibility import CredibilityScore
from app.services.credibility_engine import compute_credibility

router = APIRouter(prefix="/credibility", tags=["credibility"])

@router.post("/run")
def run_credibility(investigation_id: str, db: Session = Depends(get_db)):
    results = compute_credibility(db, investigation_id)
    return {"generated": len(results)}

@router.get("/")
def list_scores(db: Session = Depends(get_db)):
    return db.query(CredibilityScore).all()
