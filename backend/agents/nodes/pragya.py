from __future__ import annotations

import json
from typing import Any, Dict

from ..json_utils import parse_json_object
from ..llm import get_model, llm_completion
from ..state import AgentState, PragyaPlan


def pragya_node(state: AgentState) -> Dict[str, Any]:
    print("[PRAGYA] Reasoning over intent...")
    intent = (state.get("intent") or "").strip()

    if not intent:
        message = "PRAGYA Error: Empty intent received."
        fallback = PragyaPlan(
            summary="No valid intent was provided.",
            steps=["Manual review required"],
            tools_needed=[],
            assumptions=["The task intent was empty."],
        )
        return {
            "current_agent": "PRAGYA",
            "plan": fallback.model_dump(),
            "errors": state.get("errors", []) + [message],
        }

    system_prompt = """
You are PRAGYA, the reasoning and planning agent of BRAHMA COS.
Create a concise, practical plan for the user's task.

Return ONLY a valid JSON object with exactly these fields:
{
  "summary": "short overall plan",
  "steps": ["ordered step 1", "ordered step 2"],
  "tools_needed": [],
  "assumptions": []
}

Rules:
- Return the ACTUAL plan, never a JSON schema.
- Never output keys such as properties, required, type, or definitions.
- Use double-quoted JSON strings and arrays.
- No markdown, code fences, commentary, or chain-of-thought.
- Keep steps short and actionable.
""".strip()

    try:
        print(f"[PRAGYA] Using model: {get_model()}")
        response = llm_completion(
            [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Create the plan for this task:\n\n{intent}",
                },
            ],
            json_mode=True,
        )
        content = response.choices[0].message.content
        parsed = parse_json_object(content)

        if "properties" in parsed and "summary" not in parsed:
            raise ValueError("PRAGYA returned the JSON schema instead of an actual plan")

        plan = PragyaPlan.model_validate(parsed)
        return {"current_agent": "PRAGYA", "plan": plan.model_dump()}

    except Exception as exc:
        message = f"PRAGYA Error: {exc}"
        print(f"[PRAGYA] {message}")
        fallback = PragyaPlan(
            summary="Fallback plan generated due to LLM failure.",
            steps=["Manual review required"],
            tools_needed=[],
            assumptions=["System encountered an error during planning."],
        )
        return {
            "current_agent": "PRAGYA",
            "plan": fallback.model_dump(),
            "errors": state.get("errors", []) + [message],
        }
