from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

from pydantic import BaseModel, Field, field_validator


class PragyaPlan(BaseModel):
    summary: str = Field(min_length=1)
    steps: List[str] = Field(default_factory=list)
    tools_needed: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class MurphyRiskReport(BaseModel):
    risk_level: str = Field(min_length=1)
    failure_modes: List[str] = Field(default_factory=list)
    security_concerns: List[str] = Field(default_factory=list)
    recommendation: str = Field(min_length=1)

    @field_validator("risk_level")
    @classmethod
    def normalize_risk_level(cls, value: str) -> str:
        value = value.strip().upper()
        if value not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise ValueError("risk_level must be LOW, MEDIUM, HIGH, or CRITICAL")
        return value


class PolicyVerdict(BaseModel):
    risk_tier: str = Field(min_length=1)
    approved: bool
    requires_human: bool
    justification: str = Field(min_length=1)

    @field_validator("risk_tier")
    @classmethod
    def normalize_risk_tier(cls, value: str) -> str:
        value = value.strip().upper()
        if value not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise ValueError("risk_tier must be LOW, MEDIUM, HIGH, or CRITICAL")
        return value


class AgentState(TypedDict, total=False):
    task_id: str
    trace_id: str
    intent: str
    current_agent: str
    errors: List[str]
    knowledge: List[Dict[str, Any]]
    plan: Optional[Dict[str, Any]]
    risk_report: Optional[Dict[str, Any]]
    policy_verdict: Optional[Dict[str, Any]]
    execution_result: Optional[Dict[str, Any]]
