from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, text
from app.database import Base


class StatusHistory(Base):
    __tablename__ = "status_history"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    incident_id = Column(
        Integer, ForeignKey("reports.id", ondelete="cascade"), nullable=False
    )
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    changed_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
