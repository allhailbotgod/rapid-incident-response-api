from sqlalchemy import TIMESTAMP, Column, Integer, Double, String, Boolean, text
from app.database import Base


class Agency(Base):
    __tablename__ = "agencies"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    agency_name = Column(String, unique=True, nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(Integer, nullable=False)
    org_type = Column(String, nullable=False)
    org_address = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
