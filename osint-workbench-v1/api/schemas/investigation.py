from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class InvestigationCreate(BaseModel):
    name: str
    description: str | None = None

class InvestigationOut(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
