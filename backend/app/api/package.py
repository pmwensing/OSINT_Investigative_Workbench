from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.package_zip_engine import build_zip_bundle

router = APIRouter(prefix="/package", tags=["package"])

@router.get("/zip")
def export_zip(investigation_id: str, db: Session = Depends(get_db)):
    return build_zip_bundle(db, investigation_id)
