from typing import Dict, Any
from ..state import AgentState

def karma_node(state: AgentState) -> Dict[str, Any]:
    """
    KARMA Orchestrator:
    Parses intent and initializes the workflow. For the MVP, it routes everything 
    to PRAGYA for reasoning, but sets up the tracing and context.
    """
    print(f"[KARMA] Orchestrator activated for Task: {state.get('task_id')}")
    print(f"[KARMA] Analyzing Intent: {state.get('intent')}")
    
    # In a full version, KARMA would decide if it needs RAG (KOSH) first.
    # For MVP, we route straight to PRAGYA.
    return {"current_agent": "KARMA"}
