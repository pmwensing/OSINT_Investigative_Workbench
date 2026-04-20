from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.hearing_package_engine import build_hearing_package

router = APIRouter(prefix="/hearing", tags=["hearing"])

@router.get("/")
def hearing_package(investigation_id: str, db: Session = Depends(get_db)):
    return build_hearing_package(db, investigation_id)
