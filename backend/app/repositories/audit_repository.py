from sqlalchemy.orm import Session
from app.models.audit import Audit
from app.models.task import Task

class AuditRepository:
    def create(self, db: Session, task_id: int | None, agent: str, action: str, status: str = "success", event: str = "", details: str = ""):
        audit = Audit(task_id=task_id, agent=agent, action=action, status=status, event=event, details=details)
        db.add(audit); db.commit(); db.refresh(audit); return audit

    def get_all(self, db: Session):
        rows = db.query(Audit).order_by(Audit.created_at.desc()).all()
        return [{
            "id": row.id, "task_id": row.task_id,
            "task": (db.query(Task.title).filter(Task.id == row.task_id).scalar() if row.task_id else "System"),
            "agent": row.agent, "action": row.action, "status": row.status,
            "event": row.event or row.action, "details": row.details or "",
            "timestamp": row.created_at
        } for row in rows]

audit_repository = AuditRepository()
