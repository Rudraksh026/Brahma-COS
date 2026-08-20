from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any

class TaskCreate(BaseModel):
    title: str
    prompt: str

class TaskResponse(BaseModel):
    id: int
    title: str
    prompt: str
    status: str
    risk_level: str
    current_agent: str | None = None
    plan: dict[str, Any] | None = None
    risk_report: dict[str, Any] | None = None
    policy_verdict: dict[str, Any] | None = None
    execution_result: dict[str, Any] | None = None
    errors: list[str] | None = None
    trace: list[dict[str, Any]] | None = None
    created_at: datetime
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
