from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.session import Base


class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    claim_a_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False, index=True)
    claim_b_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False, index=True)
    rule = Column(String(128), nullable=False)
    summary = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default="medium")
    status = Column(String(32), nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
