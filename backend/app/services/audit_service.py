from sqlalchemy.orm import Session
from app.repositories.audit_repository import audit_repository

class AuditService:
    def create(self, db: Session, task_id: int | None, agent: str, action: str, status: str = "success", event: str = "", details: str = ""):
        return audit_repository.create(db, task_id, agent, action, status, event, details)
    def get_all(self, db: Session): return audit_repository.get_all(db)

audit_service = AuditService()
