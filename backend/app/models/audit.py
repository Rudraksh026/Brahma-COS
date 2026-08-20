from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base

class Audit(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=True)
    agent = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    status = Column(String(30), default="success")
    event = Column(String(255), default="")
    details = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
