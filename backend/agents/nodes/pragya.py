import os
import json
from typing import Dict, Any

try:
    from litellm import completion
except ImportError:
    completion = None

from ..state import AgentState, PragyaPlan


MODEL = os.getenv("LLM_MODEL", "ollama/llama3.2:3b")
OLLAMA_API_BASE = os.getenv(
    "OLLAMA_API_BASE",
    "http://localhost:11434"
)


def _clean_json_response(content: str) -> str:
    """Remove accidental markdown/code fences from the LLM response."""

    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    return content.strip()


def pragya_node(state: AgentState) -> Dict[str, Any]:

    print("[PRAGYA] Reasoning over intent...")

    intent = state.get("intent", "").strip()

    # ---------------------------------------------------------
    # Empty intent protection
    # ---------------------------------------------------------

    if not intent:
        error_message = "PRAGYA Error: Empty intent received."

        fallback_plan = PragyaPlan(
            summary="No valid intent was provided.",
            steps=["Manual review required"],
            tools_needed=[],
            assumptions=["The task intent was empty."]
        )

        return {
            "current_agent": "PRAGYA",
            "plan": fallback_plan.model_dump(),
            "errors": state.get("errors", []) + [error_message]
        }

    # ---------------------------------------------------------
    # IMPORTANT:
    # Do NOT provide model_json_schema() to llama3.2:3b.
    #
    # The previous implementation caused the model to return
    # the schema itself instead of the actual plan.
    # ---------------------------------------------------------

    system_prompt = """
You are PRAGYA, the reasoning and planning agent of BRAHMA COS.

Your job is to create a simple execution plan for the user's task.

Return ONLY ONE JSON OBJECT.

The JSON MUST contain exactly these four fields:

"summary"
A short string explaining the overall plan.

"steps"
An array of strings containing the ordered execution steps.

"tools_needed"
An array of strings containing tools or resources needed.
Use an empty array if no tools are needed.

"assumptions"
An array of strings containing assumptions.
Use an empty array if there are no assumptions.

IMPORTANT:

- Return the ACTUAL PLAN, not a JSON schema.
- Do NOT return "properties".
- Do NOT return "required".
- Do NOT return "type".
- Do NOT return Python dictionaries.
- Do NOT use single quotes.
- Use double quotes for JSON keys.
- Use double quotes for string values.
- Do NOT use Markdown.
- Do NOT use ```json.
- Do NOT explain your answer.
- Do NOT include chain-of-thought.
- Return only valid JSON.

Example of the REQUIRED OUTPUT FORMAT:

{
  "summary": "Create a concise execution plan for the requested task.",
  "steps": [
    "Understand the task requirements",
    "Identify the required information",
    "Prepare the final result"
  ],
  "tools_needed": [],
  "assumptions": [
    "The required information is available"
  ]
}
"""

    try:

        if completion is None:
            raise RuntimeError(
                "LiteLLM is not installed"
            )

        print(f"[PRAGYA] Using model: {MODEL}")

        response = completion(
            model=MODEL,
            api_base=OLLAMA_API_BASE,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": (
                        "Create the plan for this task:\n\n"
                        + intent
                    )
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "LLM returned an empty response"
            )

        content = _clean_json_response(content)

        print(
            f"[PRAGYA] Raw LLM response: {content}"
        )

        # -----------------------------------------------------
        # Parse JSON
        # -----------------------------------------------------

        try:
            parsed = json.loads(content)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"PRAGYA returned invalid JSON: {e}"
            )

        # -----------------------------------------------------
        # Detect model returning the schema instead of plan
        # -----------------------------------------------------

        if (
            isinstance(parsed, dict)
            and "properties" in parsed
            and "summary" not in parsed
        ):
            raise ValueError(
                "PRAGYA returned the JSON schema instead of "
                "an actual PragyaPlan."
            )

        # -----------------------------------------------------
        # Validate actual plan
        # -----------------------------------------------------

        plan_obj = PragyaPlan.model_validate(parsed)

        print(
            "[PRAGYA] Plan validated successfully."
        )

        return {
            "current_agent": "PRAGYA",
            "plan": plan_obj.model_dump()
        }

    except Exception as e:

        error_message = f"PRAGYA Error: {str(e)}"

        print(
            f"[PRAGYA] {error_message}"
        )

        # -----------------------------------------------------
        # Fail closed
        # -----------------------------------------------------

        fallback_plan = PragyaPlan(
            summary="Fallback plan generated due to LLM failure.",
            steps=[
                "Manual review required"
            ],
            tools_needed=[],
            assumptions=[
                "System encountered an error during planning."
            ]
        )

        return {
            "current_agent": "PRAGYA",
            "plan": fallback_plan.model_dump(),
            "errors": state.get("errors", []) + [
                error_message
            ]
        }