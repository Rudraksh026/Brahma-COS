from fastapi import APIRouter
router=APIRouter(prefix="/chat",tags=["Chat"])
@router.get("/health")
def chat_health(): return {"status":"ok"}
