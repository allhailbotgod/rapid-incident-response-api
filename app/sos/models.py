import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    String,
    Enum as SQLEnum,
    text,
    UniqueConstraint,
)
from enum import Enum
from app.database import Base


class SOS_Relation(str, Enum):
    FATHER = "father"
    MOTHER = "mother"
    UNCLE = "uncle"
    AUNT = "aunt"
    BROTHER = "brother"
    SISTER = "sister"
    FRIEND = "friend"
    SPOUSE = "spouse"


class SOS(Base):
    __tablename__ = "sos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    relationship = Column(SQLEnum(SOS_Relation, name="sos_relation"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    __table_args__ = (
        UniqueConstraint("owner_id", "phone", name="uq_sos_owner_phone"),
        UniqueConstraint("owner_id", "email", name="uq_sos_owner_email"),
    )
