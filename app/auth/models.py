import uuid
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    String,
    TIMESTAMP,
    text,
)


class RevokedTokens(Base):
    __tablename__ = "revoked_tokens"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    jti = Column(UUID(as_uuid=True), nullable=False, unique=True)
    revoked_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
    revoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
