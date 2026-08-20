from typing import Dict, Any
from ..state import AgentState
def rachit_node(state:AgentState)->Dict[str,Any]:
    plan=state.get("plan") or {}; steps=plan.get("steps",[])
    return {"current_agent":"RACHIT","execution_result":{"status":"COMPLETED","message":f"Successfully simulated execution of {len(steps)} steps.","executed_steps":len(steps)}}
