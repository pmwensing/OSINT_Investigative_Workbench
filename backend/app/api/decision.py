from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.decision_engine import build_findings, decision_summary

router = APIRouter(prefix="/decision", tags=["decision"])

@router.get("/findings")
def findings(investigation_id: str, db: Session = Depends(get_db)):
    return build_findings(db, investigation_id)

@router.get("/summary")
def summary(investigation_id: str, db: Session = Depends(get_db)):
    return decision_summary(db, investigation_id)
