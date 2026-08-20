import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from litellm import completion

from ..state import AgentState, PolicyVerdict

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")


def maryada_node(state: AgentState) -> Dict[str, Any]:

    print("[MARYADA] Applying governance policies...")

    print("MODEL =", MODEL)
    print("API_BASE =", API_BASE)

    intent = state.get("intent", "")
    plan = state.get("plan", {})
    risk = state.get("risk_report", {})
    errors = state.get("errors", [])

    # Fail closed if previous agent failed
    if errors:
        print("[MARYADA] Upstream errors detected.")

        verdict = PolicyVerdict(
            risk_tier="HIGH",
            approved=False,
            requires_human=True,
            justification="Errors detected in previous agents."
        )

        return {
            "current_agent": "MARYADA",
            "policy_verdict": verdict.model_dump()
        }

    system_prompt = """
You are MARYADA, the governance and policy agent of BRAHMA COS.

Review the intent, plan and risk report.

Return ONLY a valid JSON object in exactly this format:

{
  "risk_tier":"LOW",
  "approved":true,
  "requires_human":false,
  "justification":"Reason"
}

Do not write markdown.
Do not explain anything.
Return only JSON.
"""

    user_prompt = f"""
Intent:
{intent}

Plan:
{json.dumps(plan, indent=2)}

Risk Report:
{json.dumps(risk, indent=2)}
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

        verdict = PolicyVerdict.model_validate_json(content)

        # Never auto approve HIGH risk
        if verdict.risk_tier.upper() == "HIGH":
            verdict.approved = False
            verdict.requires_human = True

        return {
            "current_agent": "MARYADA",
            "policy_verdict": verdict.model_dump(),
        }

    except Exception as e:

        print("[MARYADA] Error:", str(e))

        fallback = PolicyVerdict(
            risk_tier="HIGH",
            approved=False,
            requires_human=True,
            justification="Policy evaluation failed."
        )

        return {
            "current_agent": "MARYADA",
            "policy_verdict": fallback.model_dump(),
            "errors": state.get("errors", []) + [str(e)],
        }