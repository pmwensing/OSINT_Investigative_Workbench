from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.pdf_binder_engine import build_binder_markdown, build_binder_html

router = APIRouter(prefix="/pdf", tags=["pdf"])

@router.get("/binder")
def binder(investigation_id: str, db: Session = Depends(get_db)):
    return build_binder_markdown(db, investigation_id)

@router.get("/binder_html")
def binder_html(investigation_id: str, db: Session = Depends(get_db)):
    return build_binder_html(db, investigation_id)
