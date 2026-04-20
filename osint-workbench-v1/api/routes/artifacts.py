from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import Artifact, User
from api.deps.auth import get_current_user

router = APIRouter(tags=["artifacts"])

@router.get("/investigations/{investigation_id}/artifacts")
def list_artifacts(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = list(db.scalars(select(Artifact).where(Artifact.investigation_id == investigation_id).order_by(Artifact.created_at.desc())))
    return [
        {
            "id": str(a.id),
            "artifact_type": a.artifact_type,
            "bucket": a.bucket,
            "object_key": a.object_key,
            "content_type": a.content_type,
            "created_at": a.created_at.isoformat(),
        }
        for a in rows
    ]
