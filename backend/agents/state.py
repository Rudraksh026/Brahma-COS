from typing import TypedDict, Optional, List, Dict, Any
from pydantic import BaseModel, Field
class PragyaPlan(BaseModel):
    summary:str; steps:List[str]; tools_needed:List[str]; assumptions:List[str]
class MurphyRiskReport(BaseModel):
    risk_level:str; failure_modes:List[str]; security_concerns:List[str]; recommendation:str
class PolicyVerdict(BaseModel):
    risk_tier:str; approved:bool; requires_human:bool; justification:str
class AgentState(TypedDict):
    task_id:str; trace_id:str; intent:str; current_agent:str; errors:List[str]
    knowledge:List[Dict[str,Any]]
    plan:Optional[Dict[str,Any]]; risk_report:Optional[Dict[str,Any]]; policy_verdict:Optional[Dict[str,Any]]; execution_result:Optional[Dict[str,Any]]
