from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import Target, Investigation, User
from api.schemas.target import TargetCreate, TargetOut
from api.deps.auth import get_current_user

router = APIRouter(tags=["targets"])

@router.post("/investigations/{investigation_id}/targets", response_model=TargetOut)
def create_target(
    investigation_id: UUID,
    payload: TargetCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    inv = db.get(Investigation, investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")
    target = Target(investigation_id=investigation_id, **payload.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return target

@router.get("/investigations/{investigation_id}/targets", response_model=list[TargetOut])
def list_targets(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list(db.scalars(select(Target).where(Target.investigation_id == investigation_id).order_by(Target.created_at.desc())))
