import json
from typing import Dict, Any
from litellm import completion
from ..state import AgentState, MurphyRiskReport

MODEL = "ollama/llama3.2:3b"

def murphy_node(state: AgentState) -> Dict[str, Any]:
    print(f"[MURPHY] Analyzing risk...")
    plan_dict = state.get("plan", {})
    intent = state.get("intent", "")
    
    system_prompt = f"""You are MURPHY, the adversarial risk simulation agent.
Your job is to red-team the provided plan and intent. Identify failure modes, edge cases, and security risks.
You MUST respond with valid JSON matching this schema:
{MurphyRiskReport.model_json_schema()}
Do not include any other text, markdown blocks, or chain-of-thought in your response, ONLY the raw JSON object.
"""
    user_prompt = f"Intent: {intent}\n\nProposed Plan:\n{json.dumps(plan_dict, indent=2)}"
    
    try:
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
            
        risk_obj = MurphyRiskReport.model_validate_json(content.strip())
        return {
            "current_agent": "MURPHY",
            "risk_report": risk_obj.model_dump()
        }
    except Exception as e:
        print(f"[MURPHY] Error simulating risk: {str(e)}")
        # Safe failure: Assume high risk if we can't analyze
        fallback_risk = MurphyRiskReport(
            risk_level="HIGH",
            failure_modes=["Unknown - LLM Risk Analysis Failed"],
            security_concerns=["Cannot guarantee safety due to analysis failure"],
            recommendation="Block execution and review manually."
        )
        return {
            "current_agent": "MURPHY",
            "risk_report": fallback_risk.model_dump(),
            "errors": state.get("errors", []) + [f"MURPHY Error: {str(e)}"]
        }
