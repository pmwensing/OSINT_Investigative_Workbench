from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.quick_sheet_engine import build_quick_sheet

router = APIRouter(prefix="/quick_sheet", tags=["quick_sheet"])

@router.get("/")
def quick_sheet(investigation_id: str, db: Session = Depends(get_db)):
    return build_quick_sheet(db, investigation_id)
