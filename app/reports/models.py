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


class IncidentType(str, Enum):
    VICTIM = "victim"
    WITNESS = "witness"


class IncidentSummary(str, Enum):
    FIRE = "fire"
    ACCIDENT = "accident"
    CRIME = "crime"


class IncidentPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    EVALUATING = "evaluating"


class IncidentStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RESPONDING = "responding"
    CLOSED = "closed"


class Incidents(Base):
    __tablename__ = "incidents"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    reporter_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="cascade",
            name="incidents_users.id_incidents.reporter_id_fk",
        ),
        nullable=False,
    )
    agency_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "agencies.id",
            ondelete="set null",
            name="incidents_agencies.id_incidente.agency_id_fk",
        ),
        nullable=True,
    )
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    incident_type = Column(
        SQLEnum(IncidentType, name="incident_type_enum"), nullable=False
    )
    incident_summary = Column(
        SQLEnum(IncidentSummary, name="incident_summary_enum", nullable=False)
    )
    priority = Column(
        SQLEnum(IncidentPriority, name="incident_priority_enum"),
        default=IncidentPriority.EVALUATING,
    )
    description = Column(String, nullable=True)
    status = Column(
        SQLEnum(IncidentStatus, name="incident_status_enum"),
        default=IncidentStatus.PENDING,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    media = relationship(
        "Media",
        back_populates="incidents",
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
    upload_status = Column(
        String,
        nullable=False,
        default="pending",
    )
    incident_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "incidents.id",
            ondelete="cascade",
            name="media_incidents.id_media.incident_id_fk",
        ),
        nullable=False,
    )
    object_key = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    incident = relationship(
        "Incidents",
        back_populates="media",
    )
