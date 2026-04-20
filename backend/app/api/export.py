from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.hearing_package_engine import build_hearing_package
from app.services.export_engine import build_export_package

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/")
def export_package(investigation_id: str, db: Session = Depends(get_db)):
    pkg = build_hearing_package(db, investigation_id)
    return build_export_package(pkg)
