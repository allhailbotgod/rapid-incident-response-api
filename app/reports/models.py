import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    TIMESTAMP,
    text,
    Enum as SQLEnum,
    Double,
)
from enum import Enum

from sqlalchemy.orm import relationship
from app.database import Base


class ReportType(str, Enum):
    VICTIM = "victim"
    WITNESS = "witness"


class ReportPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    EVALUATING = "evaluating"


class ReportStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RESPONDING = "responding"
    CLOSED = "closed"


class Reports(Base):
    __tablename__ = "reports"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    reporter_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    report_type = Column(SQLEnum(ReportType, name="report_type_enum"), nullable=False)
    priority = Column(
        SQLEnum(ReportPriority, name="report_priority_enum"),
        default=ReportPriority.EVALUATING,
    )
    description = Column(String, nullable=True)
    status = Column(
        SQLEnum(ReportStatus, name="report_status_enum"),
        default=ReportStatus.PENDING,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    media = relationship(
        "Media",
        back_populates="report",
        cascade="all, delete-orphan",
    )


class Media(Base):
    __tablename__ = "incident_media"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    incident_id = Column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="cascade"), nullable=False
    )
    object_key = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    report = relationship(
        "Reports",
        back_populates="media",
    )
