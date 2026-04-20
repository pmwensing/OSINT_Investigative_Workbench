from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.session import Base


class Entity(Base):
    __tablename__ = "entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)
    value = Column(String(512), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    claims = relationship("Claim", back_populates="entity", cascade="all, delete")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False, index=True)
    claim_type = Column(String(128), nullable=False)
    value = Column(Text, nullable=False)
    source = Column(Text, nullable=True)
    confidence = Column(String(32), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    entity = relationship("Entity", back_populates="claims")


class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    artifact_type = Column(String(128), nullable=False)
    location = Column(Text, nullable=False)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    target_entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
