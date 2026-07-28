import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from app.database import Base


class StatusHistory(Base):
    __tablename__ = "status_history"
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
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    changed_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
