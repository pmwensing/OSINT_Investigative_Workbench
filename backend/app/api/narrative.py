from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.narrative_engine import build_narrative

router = APIRouter(prefix="/narrative", tags=["narrative"])

@router.get("/")
def narrative(investigation_id: str, db: Session = Depends(get_db)):
    return build_narrative(db, investigation_id)
