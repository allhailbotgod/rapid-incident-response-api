import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, text
from app.database import Base


class Roles(Base):
    __tablename__ = "roles"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
