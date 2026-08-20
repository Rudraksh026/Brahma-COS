import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from litellm import completion

from ..state import AgentState, PragyaPlan

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")


def pragya_node(state: AgentState) -> Dict[str, Any]:
    print("[PRAGYA] Reasoning over intent...")

    print("MODEL =", MODEL)
    print("API_BASE =", API_BASE)

    intent = state.get("intent", "")
    knowledge = state.get("knowledge", [])

    print("Retrieved Knowledge:", knowledge)

    system_prompt = """
You are PRAGYA, the planning agent of BRAHMA COS.

Create a plan for the given user request.

Return ONLY a valid JSON object in exactly this format:

{
  "summary": "short summary",
  "steps": [
    "step 1",
    "step 2"
  ],
  "tools_needed": [
    "tool 1"
  ],
  "assumptions": [
    "assumption 1"
  ]
}

Do not use markdown.
Do not use ```json.
Do not explain anything.
Return only the JSON object.
"""

    try:

        response = completion(
            model=MODEL,
            api_base=API_BASE,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"""
                Intent:
                {intent}

                Relevant Knowledge:
                {json.dumps(knowledge, indent=2)}
                """,
                    },
                ],
        )

        content = response.choices[0].message.content

        print("========== RAW RESPONSE ==========")
        print(content)
        print("==================================")

        plan_obj = PragyaPlan.model_validate_json(content)

        return {
            "current_agent": "PRAGYA",
            "plan": plan_obj.model_dump(),
        }

    except Exception as e:

        print("[PRAGYA] Error:", str(e))

        fallback = PragyaPlan(
            summary="Fallback plan generated.",
            steps=[
                "Manual review required."
            ],
            tools_needed=[],
            assumptions=[
                "LLM response could not be parsed."
            ]
        )

        return {
            "current_agent": "PRAGYA",
            "plan": fallback.model_dump(),
            "errors": state.get("errors", []) + [str(e)],
        }