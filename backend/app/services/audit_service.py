from sqlalchemy.orm import Session

from app.repositories.audit_repository import audit_repository


class AuditService:

    def create(self, db: Session, task_id: int, agent: str, action: str):
        return audit_repository.create(db, task_id, agent, action)

    def get_all(self, db: Session):
        return audit_repository.get_all(db)


audit_service = AuditService()