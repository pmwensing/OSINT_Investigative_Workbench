from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class TargetCreate(BaseModel):
    target_type: str
    value: str
    display_name: str | None = None
    notes: str | None = None

class TargetOut(BaseModel):
    id: UUID
    investigation_id: UUID
    target_type: str
    value: str
    display_name: str | None = None
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
