import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    String,
    text,
    Enum as SQLEnum,
    ARRAY,
)
from enum import Enum
from app.database import Base


class BloodgroupEnum(str, Enum):
    Ap = "A+"
    An = "A-"
    Bp = "B+"
    Bn = "B-"
    ABp = "AB+"
    ABn = "AB-"
    Op = "O+"
    On = "O-"


class GenotypeEnum(str, Enum):
    AA = "AA"
    AS = "AS"
    SS = "SS"
    CC = "CC"
    AC = "AC"
    SC = "SC"


class MedicProfile(Base):
    __tablename__ = "medic_profile"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
        unique=True,
    )
    blood_group = Column(
        SQLEnum(BloodgroupEnum, name="blood_group_enum"), nullable=True
    )
    genotype = Column(SQLEnum(GenotypeEnum, name="genotype_enum"), nullable=True)
    conditions = Column(ARRAY(String), nullable=True)
    allergies = Column(ARRAY(String), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
