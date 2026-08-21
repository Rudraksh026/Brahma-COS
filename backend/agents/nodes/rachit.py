from __future__ import annotations

from typing import Any, Dict

from ..state import AgentState


def rachit_node(state: AgentState) -> Dict[str, Any]:
    """Execute only after MARYADA has explicitly approved the task."""
    verdict = state.get("policy_verdict") or {}
    if verdict.get("approved") is not True or verdict.get("requires_human") is True:
        return {
            "current_agent": "RACHIT",
            "execution_result": {
                "status": "BLOCKED",
                "message": "Execution blocked because MARYADA did not grant automatic approval.",
                "executed_steps": 0,
            },
        }

    plan = state.get("plan") or {}
    steps = plan.get("steps") or []
    return {
        "current_agent": "RACHIT",
        "execution_result": {
            "status": "COMPLETED",
            "message": f"Successfully simulated execution of {len(steps)} steps.",
            "executed_steps": len(steps),
        },
    }
