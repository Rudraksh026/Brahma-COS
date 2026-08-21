from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

from pydantic import BaseModel, Field


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


class PolicyVerdict(BaseModel):
    risk_tier: str = Field(min_length=1)
    approved: bool
    requires_human: bool
    justification: str = Field(min_length=1)


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
