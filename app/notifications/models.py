import uuid
from enum import Enum

from sqlalchemy import Column, String, text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum

from app.database import Base


class NotificationChannel(str, Enum):
    PUSH = "push"
    SMS = "sms"
    WHATSAPP = "whatsapp"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    incident_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reports.id", ondelete="cascade"),
        nullable=False,
    )

    channel = Column(
        SQLEnum(
            NotificationChannel,
            name="notification_channel_enum",
        ),
        nullable=False,
    )

    status = Column(
        SQLEnum(
            NotificationStatus,
            name="notification_status_enum",
        ),
        nullable=False,
        default=NotificationStatus.PENDING,
    )

    recipient_email = Column(
        String,
        nullable=True,
    )

    recipient_phone = Column(
        String,
        nullable=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    message = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    sent_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    error = Column(
        String,
        nullable=True,
    )
