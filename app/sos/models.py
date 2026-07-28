from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
    text,
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
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    phone = Column(Integer, nullable=False)
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
