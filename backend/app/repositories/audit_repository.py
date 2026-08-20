from sqlalchemy.orm import Session
from app.models.audit import Audit


class AuditRepository:

    def create(self, db: Session, task_id: int, agent: str, action: str):

        audit = Audit(
            task_id=task_id,
            agent=agent,
            action=action
        )

        db.add(audit)
        db.commit()
        db.refresh(audit)

        return audit

    def get_all(self, db: Session):
        return db.query(Audit).all()


audit_repository = AuditRepository()