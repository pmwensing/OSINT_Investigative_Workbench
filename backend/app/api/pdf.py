from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.pdf_binder_engine import build_binder_markdown

router = APIRouter(prefix="/pdf", tags=["pdf"])

@router.get("/binder")
def binder(investigation_id: str, db: Session = Depends(get_db)):
    return build_binder_markdown(db, investigation_id)
