import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from litellm import completion

from ..state import AgentState, MurphyRiskReport

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")


def murphy_node(state: AgentState) -> Dict[str, Any]:
    print("[MURPHY] Analyzing risk...")

    print("MODEL =", MODEL)
    print("API_BASE =", API_BASE)

    intent = state.get("intent", "")
    plan = state.get("plan", {})

    system_prompt = """
You are MURPHY, the risk analysis agent of BRAHMA COS.

Analyze the given plan and identify risks.

Return ONLY a valid JSON object in exactly this format:

{
  "risk_level": "LOW",
  "failure_modes": [
    "failure 1"
  ],
  "security_concerns": [
    "concern 1"
  ],
  "recommendation": "your recommendation"
}

Do not write markdown.
Do not explain anything.
Return only the JSON object.
"""

    user_prompt = f"""
Intent:
{intent}

Plan:
{json.dumps(plan, indent=2)}
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
                    "content": user_prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        print("========== RAW RESPONSE ==========")
        print(content)
        print("==================================")

        risk_obj = MurphyRiskReport.model_validate_json(content)

        return {
            "current_agent": "MURPHY",
            "risk_report": risk_obj.model_dump(),
        }

    except Exception as e:

        print("[MURPHY] Error:", str(e))

        fallback = MurphyRiskReport(
            risk_level="HIGH",
            failure_modes=[
                "LLM response parsing failed."
            ],
            security_concerns=[
                "Unable to complete automated risk analysis."
            ],
            recommendation="Manual review required."
        )

        return {
            "current_agent": "MURPHY",
            "risk_report": fallback.model_dump(),
            "errors": state.get("errors", []) + [str(e)],
        }