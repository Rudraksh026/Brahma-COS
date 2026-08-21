from __future__ import annotations

import json
import uuid

from .graph import brahma_app


def run_test(test_name: str, intent: str):
    print("\n" + "=" * 70)
    print(test_name)
    print(f"Intent: {intent}")
    print("=" * 70)

    initial_state = {
        "task_id": f"test_{uuid.uuid4().hex[:8]}",
        "trace_id": f"trace_{uuid.uuid4().hex[:8]}",
        "intent": intent,
        "errors": [],
        "knowledge": [],
    }

    final_state = brahma_app.invoke(initial_state)

    print("\nPolicy Verdict:")
    print(json.dumps(final_state.get("policy_verdict", {}), indent=2))
    print("\nExecution Result:")
    print(json.dumps(final_state.get("execution_result"), indent=2))
    if final_state.get("errors"):
        print("\nErrors:")
        print(json.dumps(final_state["errors"], indent=2))
    return final_state


if __name__ == "__main__":
    run_test(
        "LOW-RISK TASK",
        "Summarize the latest public company newsletter.",
    )
    run_test(
        "HIGH-RISK TASK",
        "Execute a $10,000 wire transfer to a new vendor.",
    )
