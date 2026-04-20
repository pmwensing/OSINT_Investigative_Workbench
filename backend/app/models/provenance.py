from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.session import Base


class ProvenanceRecord(Base):
    __tablename__ = "provenance_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    artifact_id = Column(UUID(as_uuid=True), ForeignKey("artifacts.id", ondelete="CASCADE"), nullable=True, index=True)
    derived_from_id = Column(UUID(as_uuid=True), ForeignKey("provenance_records.id", ondelete="SET NULL"), nullable=True, index=True)
    record_type = Column(String(64), nullable=False)
    locator = Column(Text, nullable=True)
    content_hash = Column(String(128), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ClaimCitation(Base):
    __tablename__ = "claim_citations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False, index=True)
    artifact_id = Column(UUID(as_uuid=True), ForeignKey("artifacts.id", ondelete="CASCADE"), nullable=True, index=True)
    provenance_id = Column(UUID(as_uuid=True), ForeignKey("provenance_records.id", ondelete="SET NULL"), nullable=True, index=True)
    locator = Column(Text, nullable=True)
    excerpt = Column(Text, nullable=True)
    justification = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
