from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.risk_engine import compute_risk

router = APIRouter(prefix="/risk", tags=["risk"])

@router.post("/run")
def run_risk(investigation_id: str, db: Session = Depends(get_db)):
    return compute_risk(db, investigation_id)
