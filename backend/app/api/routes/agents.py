from fastapi import APIRouter

from app.db.database import SessionLocal
from app.models.task import Task

router = APIRouter(prefix="/agents", tags=["Agents"])
AGENTS = [
    ("KARMA", "Task orchestration"), ("KOSH", "Knowledge retrieval"), ("SMRITI", "Memory management"),
    ("PRAGYA", "Reasoning and planning"), ("MURPHY", "Risk analysis"), ("MARYADA", "Governance and policy"),
    ("RACHIT", "Approved execution"), ("NIYANTRA", "Audit and traceability"), ("LISA", "Feedback and learning")
]

@router.get("/")
def get_agents():
    db=SessionLocal()
    try:
        latest=db.query(Task).order_by(Task.updated_at.desc()).limit(20).all()
        ollama_ok=True
        try:
            import ollama
            ollama.list()
        except Exception: ollama_ok=False
        result=[]
        for name,role in AGENTS:
            related=next((t for t in latest if t.current_agent == name), None)
            status="active" if related and related.status in ("RUNNING","BLOCKED") else ("failed" if related and related.status=="FAILED" else "idle")
            if name in {"PRAGYA","MURPHY","MARYADA"} and not ollama_ok: status="failed"
            result.append({"name":name,"role":role,"status":status,"current_task":related.title if related else None,"last_activity":related.updated_at if related else None,"health":"healthy" if (ollama_ok or name not in {"PRAGYA","MURPHY","MARYADA"}) else "degraded"})
        return result
    finally: db.close()
