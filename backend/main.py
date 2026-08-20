from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="BRAHMA COS Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    user_id: str
    intent: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "BRAHMA COS API is running"}

@app.post("/api/tasks")
def create_task(request: TaskRequest):
    # Mocking task creation and orchestration
    return {
        "status": "pending",
        "task_id": "mock_task_id",
        "message": f"Task '{request.intent}' received and queued for KARMA routing."
    }

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    # Mock task status polling
    return {
        "task_id": task_id,
        "status": "approved",
        "trace": [
            {"agent": "KARMA", "action": "route", "status": "done"},
            {"agent": "PRAGYA", "action": "reasoning", "status": "done"},
            {"agent": "MARYADA", "action": "governance_check", "status": "done"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
