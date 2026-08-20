import json
from typing import Dict, Any
from litellm import completion
from ..state import AgentState, PragyaPlan

MODEL = "ollama/llama3.2:3b" # Can be configured via env later

def pragya_node(state: AgentState) -> Dict[str, Any]:
    print(f"[PRAGYA] Reasoning over intent...")
    intent = state.get("intent", "")
    
    system_prompt = f"""You are PRAGYA, the core reasoning agent of BRAHMA COS.
Your goal is to formulate a structured plan to address the user's intent.
You MUST respond with valid JSON matching this schema:
{PragyaPlan.model_json_schema()}
Do not include any other text, markdown blocks, or chain-of-thought in your response, ONLY the raw JSON object.
"""
    
    try:
        response = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": intent}
            ]
        )
        content = response.choices[0].message.content
        
        # Strip markdown if present
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        plan_obj = PragyaPlan.model_validate_json(content.strip())
        return {
            "current_agent": "PRAGYA",
            "plan": plan_obj.model_dump()
        }
    except Exception as e:
        print(f"[PRAGYA] Error generating plan: {str(e)}")
        # Safe failure
        fallback_plan = PragyaPlan(
            summary="Fallback plan generated due to LLM failure.",
            steps=["Manual review required"],
            tools_needed=[],
            assumptions=["System encountered an error during planning."]
        )
        return {
            "current_agent": "PRAGYA",
            "plan": fallback_plan.model_dump(),
            "errors": state.get("errors", []) + [f"PRAGYA Error: {str(e)}"]
        }
