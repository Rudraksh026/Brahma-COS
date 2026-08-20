from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Audit(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer)

    agent = Column(String)

    action = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())