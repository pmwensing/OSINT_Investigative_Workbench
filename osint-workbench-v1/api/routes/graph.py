from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.db.session import get_db
from api.db.models import Entity, Relationship, User
from api.deps.auth import get_current_user

router = APIRouter(tags=["graph"])

@router.get("/investigations/{investigation_id}/graph")
def get_graph(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entities = list(db.scalars(select(Entity).where(Entity.investigation_id == investigation_id)))
    relationships = list(db.scalars(select(Relationship).where(Relationship.investigation_id == investigation_id)))
    return {
        "nodes": [
            {"id": str(e.id), "label": e.name, "type": e.entity_type, "confidence": e.confidence}
            for e in entities
        ],
        "edges": [
            {
                "id": str(r.id),
                "source": str(r.source_entity_id),
                "target": str(r.target_entity_id),
                "label": r.relationship_type,
                "confidence": r.confidence,
            }
            for r in relationships
        ],
    }
