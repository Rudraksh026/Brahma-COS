from __future__ import annotations

from typing import Any, Dict

from ..json_utils import parse_json_object, reject_schema_object
from ..llm import get_model, llm_completion
from ..state import AgentState, PragyaPlan


def _fallback(state: AgentState, message: str) -> Dict[str, Any]:
    fallback = PragyaPlan(
        summary="Fallback plan generated because automated planning failed.",
        steps=["Manual review required"],
        tools_needed=[],
        assumptions=["The planning model did not return a valid structured response."],
    )
    return {
        "current_agent": "PRAGYA",
        "plan": fallback.model_dump(),
        "errors": state.get("errors", []) + [message],
    }


def pragya_node(state: AgentState) -> Dict[str, Any]:
    print("[PRAGYA] Reasoning over intent...")
    intent = (state.get("intent") or "").strip()

    if not intent:
        return _fallback(state, "PRAGYA Error: Empty intent received.")

    system_prompt = """
You are PRAGYA, the reasoning and planning agent of BRAHMA COS.

Your task is to create a practical plan for the user's intent.

IMPORTANT OUTPUT RULES:
1. Return ONLY one JSON OBJECT.
2. Return the DATA itself, NOT a JSON schema.
3. Do NOT return keys named properties, required, type, $defs, or definitions.
4. Use double quotes for every JSON key and string.
5. Do not use markdown or code fences.
6. Do not explain your answer outside the JSON object.

The JSON object MUST have exactly this shape:
{
  "summary": "short overall plan",
  "steps": ["ordered actionable step"],
  "tools_needed": ["tool names, or an empty array"],
  "assumptions": ["assumptions, or an empty array"]
}
""".strip()

    user_prompt = f"Create the plan for this task:\n\n{intent}"

    try:
        print(f"[PRAGYA] Using model: {get_model()}")
        response = llm_completion(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            json_mode=True,
        )
        content = response.choices[0].message.content or ""
        parsed = parse_json_object(content)
        reject_schema_object(parsed, "PRAGYA")

        plan = PragyaPlan.model_validate(parsed)
        return {"current_agent": "PRAGYA", "plan": plan.model_dump()}

    except Exception as exc:
        message = f"PRAGYA Error: {exc}"
        print(f"[PRAGYA] {message}")
        return _fallback(state, message)
