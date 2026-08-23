import uuid
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, Column, Double, String, Boolean, text, Enum as SQLEnum
from app.database import Base


class OrgTypeEnum(str, Enum):
    MEDICAL = "medical"
    FIRE_SERVICE = "fire service"
    LAW = "law enforcement"


class Agency(Base):
    __tablename__ = "agencies"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String, unique=True, nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    org_type = Column(SQLEnum(OrgTypeEnum, name="org_type_enum"), nullable=False)
    org_address = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
