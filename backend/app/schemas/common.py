from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class InvestigationCreate(BaseModel):
    name: str
    description: str | None = None


class InvestigationRead(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class TargetCreate(BaseModel):
    investigation_id: UUID
    target_type: str
    value: str
    notes: str | None = None


class TargetRead(BaseModel):
    id: UUID
    investigation_id: UUID
    target_type: str
    value: str
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class EntityCreate(BaseModel):
    investigation_id: UUID
    entity_type: str
    value: str


class EntityRead(BaseModel):
    id: UUID
    investigation_id: UUID
    entity_type: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimCreate(BaseModel):
    entity_id: UUID
    claim_type: str
    value: str
    source: str | None = None
    confidence: str | None = None


class ClaimRead(BaseModel):
    id: UUID
    entity_id: UUID
    claim_type: str
    value: str
    source: str | None = None
    confidence: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ArtifactCreate(BaseModel):
    investigation_id: UUID
    artifact_type: str
    location: str
    metadata: str | None = None


class ArtifactRead(BaseModel):
    id: UUID
    investigation_id: UUID
    artifact_type: str
    location: str
    metadata: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class RelationshipCreate(BaseModel):
    source_entity_id: UUID
    target_entity_id: UUID
    relationship_type: str


class RelationshipRead(BaseModel):
    id: UUID
    source_entity_id: UUID
    target_entity_id: UUID
    relationship_type: str
    created_at: datetime

    class Config:
        from_attributes = True
