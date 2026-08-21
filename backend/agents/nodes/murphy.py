from __future__ import annotations

import json
from typing import Any, Dict

from ..json_utils import parse_json_object, reject_schema_object
from ..llm import get_model, llm_completion
from ..state import AgentState, MurphyRiskReport


def murphy_node(state: AgentState) -> Dict[str, Any]:
    print("[MURPHY] Analyzing risk...")
    plan_dict = state.get("plan") or {}
    intent = (state.get("intent") or "").strip()

    system_prompt = """
You are MURPHY, the adversarial risk simulation agent of BRAHMA COS.

Red-team the user's intent and proposed plan. Identify failure modes,
security/privacy concerns, and the safest recommendation.

IMPORTANT OUTPUT RULES:
1. Return ONLY one JSON OBJECT.
2. Return the DATA itself, NOT a JSON schema.
3. Do NOT return properties, required, type, $defs, or definitions.
4. Use double quotes for JSON.
5. No markdown, commentary, or chain-of-thought.

The JSON object MUST have exactly:
{
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "failure_modes": ["failure mode"],
  "security_concerns": ["security concern"],
  "recommendation": "safest recommendation"
}
""".strip()

    user_prompt = (
        f"Intent: {intent}\n\n"
        f"Proposed Plan:\n{json.dumps(plan_dict, indent=2)}"
    )

    try:
        print(f"[MURPHY] Using model: {get_model()}")
        response = llm_completion(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            json_mode=True,
        )
        content = response.choices[0].message.content or ""
        parsed = parse_json_object(content)
        reject_schema_object(parsed, "MURPHY")

        risk = MurphyRiskReport.model_validate(parsed)
        return {"current_agent": "MURPHY", "risk_report": risk.model_dump()}

    except Exception as exc:
        message = f"MURPHY Error: {exc}"
        print(f"[MURPHY] {message}")
        fallback = MurphyRiskReport(
            risk_level="HIGH",
            failure_modes=["Risk analysis could not be completed."],
            security_concerns=[
                "Safety cannot be guaranteed because risk analysis failed."
            ],
            recommendation="Block execution and review manually.",
        )
        return {
            "current_agent": "MURPHY",
            "risk_report": fallback.model_dump(),
            "errors": state.get("errors", []) + [message],
        }
