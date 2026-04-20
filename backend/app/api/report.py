from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.report_engine import build_report

router = APIRouter(prefix="/report", tags=["report"])

@router.get("/")
def get_report(investigation_id: str, db: Session = Depends(get_db)):
    return build_report(db, investigation_id)
