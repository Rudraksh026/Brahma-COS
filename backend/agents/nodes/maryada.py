import json
from typing import Dict, Any
try:
    from litellm import completion
except ImportError:
    completion = None
from ..state import AgentState, PolicyVerdict

MODEL = "ollama/llama3.2:3b"

def maryada_node(state: AgentState) -> Dict[str, Any]:
    print(f"[MARYADA] Applying governance policies...")
    plan_dict = state.get("plan", {})
    risk_dict = state.get("risk_report", {})
    intent = state.get("intent", "")
    errors = state.get("errors", [])
    
    # If there was a failure upstream, fail closed immediately
    if errors:
        print("[MARYADA] Upstream errors detected. Failing closed.")
        verdict = PolicyVerdict(
            risk_tier="HIGH",
            approved=False,
            requires_human=True,
            justification=f"Upstream agent errors detected: {', '.join(errors)}"
        )
        return {
            "current_agent": "MARYADA",
            "policy_verdict": verdict.model_dump()
        }

    system_prompt = f"""You are MARYADA, the governance and policy gate agent.
You receive a user's intent, the proposed plan, and a risk report.
Your job is to apply enterprise policy and generate a Policy Verdict.
High-risk actions (financial, data deletion, legal) must NOT be approved automatically.
You MUST respond with valid JSON matching this schema:
{PolicyVerdict.model_json_schema()}
Do not include any other text, markdown blocks, or chain-of-thought in your response, ONLY the raw JSON object.
"""
    user_prompt = f"Intent: {intent}\n\nProposed Plan:\n{json.dumps(plan_dict)}\n\nRisk Report:\n{json.dumps(risk_dict)}"
    
    try:
        if completion is None:
            raise RuntimeError("LiteLLM is not installed")
        response = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        content = response.choices[0].message.content
        
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        verdict_obj = PolicyVerdict.model_validate_json(content.strip())
        
        # Override to prevent high risk from passing
        if verdict_obj.risk_tier == "HIGH" and verdict_obj.approved:
            verdict_obj.approved = False
            verdict_obj.requires_human = True
            verdict_obj.justification += " (Overridden: HIGH risk tiers cannot be auto-approved)"
            
        return {
            "current_agent": "MARYADA",
            "policy_verdict": verdict_obj.model_dump()
        }
    except Exception as e:
        print(f"[MARYADA] Error evaluating policy: {str(e)}")
        # Fail closed
        fallback_verdict = PolicyVerdict(
            risk_tier="HIGH",
            approved=False,
            requires_human=True,
            justification="Policy evaluation failed due to system error."
        )
        return {
            "current_agent": "MARYADA",
            "policy_verdict": fallback_verdict.model_dump(),
            "errors": state.get("errors", []) + [f"MARYADA Error: {str(e)}"]
        }
