from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    target_id: UUID
    connectors: list[str] = Field(default_factory=list)

class JobOut(BaseModel):
    id: UUID
    investigation_id: UUID
    target_id: UUID
    connector: str
    status: str
    error_message: str | None = None
    queued_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None

    class Config:
        from_attributes = True
