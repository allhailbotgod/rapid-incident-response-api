from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from app.database import Base


class MedicProfile(Base):
    __tablename__ = "medic_profile"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False, unique=True
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
