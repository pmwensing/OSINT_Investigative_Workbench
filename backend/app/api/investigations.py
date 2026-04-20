from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.investigation import Investigation

router = APIRouter(prefix="/investigations", tags=["investigations"])

@router.post("/")
def create_investigation(name: str, description: str = "", db: Session = Depends(get_db)):
    inv = Investigation(name=name, description=description)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/")
def list_investigations(db: Session = Depends(get_db)):
    return db.query(Investigation).all()
