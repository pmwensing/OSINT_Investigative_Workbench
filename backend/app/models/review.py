from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.session import Base


class AnalystReview(Base):
    __tablename__ = "analyst_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    object_type = Column(String(64), nullable=False)
    object_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(String(32), nullable=False, default="pending")
    notes = Column(Text, nullable=True)
    reviewer = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = Column(String(64), nullable=False)
    value = Column(String(512), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(String(64), nullable=False)
    severity = Column(String(32), nullable=False, default="medium")
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    source_object_type = Column(String(64), nullable=True)
    source_object_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    is_open = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
