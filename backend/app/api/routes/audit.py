from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.audit_service import audit_service

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    return audit_service.get_all(db)
