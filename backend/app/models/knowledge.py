from sqlalchemy import Column, Integer, String, Text, JSON
from app.db.database import Base, is_sqlite
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = None

class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSON if is_sqlite or Vector is None else Vector(768), nullable=True)
