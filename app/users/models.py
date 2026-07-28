from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Enum as SQLEnum,
    text,
)
from enum import Enum
from app.database import Base


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(SQLEnum(Gender, name="gender_enum"), nullable=False)
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="restrict"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
