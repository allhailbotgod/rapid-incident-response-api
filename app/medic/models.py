import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, text
from sqlalchemy.orm import Relationship
from app.database import Base


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
    blood_group = Column(String, nullable=True)
    genotype = Column(String, nullable=True)
    conditions = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
