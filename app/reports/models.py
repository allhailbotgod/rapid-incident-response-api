from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    text,
    Enum as SQLEnum,
    Double,
)
from enum import Enum
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
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    reporter_id = Column(
        Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False
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


class Media(Base):
    __tablename__ = "incident_media"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    incident_id = Column(
        Integer, ForeignKey("reports.id", ondelete="cascade"), nullable=False
    )
    url = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
