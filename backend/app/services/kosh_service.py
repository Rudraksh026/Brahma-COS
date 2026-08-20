from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.knowledge_repository import semantic_search

class KoshService:
    def retrieve(self, query: str, top_k: int = 5):
        db: Session = SessionLocal()
        try: return semantic_search(db, query, top_k)
        finally: db.close()

kosh = KoshService()
