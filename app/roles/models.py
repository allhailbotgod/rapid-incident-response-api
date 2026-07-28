from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.database import Base


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
