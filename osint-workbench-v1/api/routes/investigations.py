from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import Investigation, User
from api.schemas.investigation import InvestigationCreate, InvestigationOut
from api.deps.auth import get_current_user

router = APIRouter(tags=["investigations"])

@router.post("/investigations", response_model=InvestigationOut)
def create_investigation(
    payload: InvestigationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = Investigation(name=payload.name, description=payload.description, owner_user_id=user.id)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/investigations", response_model=list[InvestigationOut])
def list_investigations(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list(db.scalars(select(Investigation).order_by(Investigation.created_at.desc())))
