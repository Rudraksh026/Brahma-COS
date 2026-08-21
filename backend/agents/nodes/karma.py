from __future__ import annotations

from typing import Any, Dict

from ..state import AgentState


def karma_node(state: AgentState) -> Dict[str, Any]:
    """Initialize a trace and route the task into the reasoning pipeline."""
    task_id = state.get("task_id", "unknown")
    intent = (state.get("intent") or "").strip()
    print(f"[KARMA] Orchestrator activated for Task: {task_id}")
    print(f"[KARMA] Intent: {intent}")
    return {"current_agent": "KARMA"}
