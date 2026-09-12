import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    TIMESTAMP,
    Enum as SQLEnum,
    text,
)
from enum import Enum

from sqlalchemy.orm import relationship
from app.database import Base


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Users(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(SQLEnum(Gender, name="gender_enum"), nullable=False)
    password = Column(String, nullable=False)
    org_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "agencies.id", ondelete="set null", name="users_agencies.id_users.org_id_fk"
        ),
        nullable=True,
        unique=True,
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "roles.id", ondelete="restrict", name="users_roles.id_users.role_id_fk"
        ),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    role = relationship("Roles")
