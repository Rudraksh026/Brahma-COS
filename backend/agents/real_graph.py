import os
from typing import TypedDict
# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, END
from litellm import completion

# Optional: Add your API key here or in an .env file
# os.environ["OPENAI_API_KEY"] = "sk-..."
# os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

# Default model, change to "gpt-4o" or "claude-3-5-sonnet-20240620" as needed
MODEL = "ollama/llama3.2:3b"

class AgentState(TypedDict):
    task_id: str
    input: str
    plan: str
    risk_report: str
    policy_verdict: str

def pragya_node(state: AgentState):
    print(f"[PRAGYA] Thinking about: {state['input']}")
    
    try:
        response = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are PRAGYA, the reasoning agent of BRAHMA COS. Formulate a structured, step-by-step plan to address the user's input."},
                {"role": "user", "content": state['input']}
            ]
        )
        plan = response.choices[0].message.content
    except Exception as e:
        plan = f"[Error connecting to LLM] Backup Plan: Process {state['input']} manually."
        
    return {"plan": plan}

def murphy_node(state: AgentState):
    print(f"[MURPHY] Simulating risks for the plan...")
    
    try:
        response = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are MURPHY, the risk simulation agent. Red-team the following plan. Identify failure modes, edge cases, and security risks."},
                {"role": "user", "content": state['plan']}
            ]
        )
        risk = response.choices[0].message.content
    except Exception as e:
        risk = "[Error connecting to LLM] Backup Risk Report: Moderate risk assumed."
        
    return {"risk_report": risk}

def maryada_node(state: AgentState):
    print(f"[MARYADA] Applying governance policies...")
    # Simple hardcoded policy check for MVP
    if "buy" in state["input"].lower() or "purchase" in state["input"].lower():
        verdict = "ESCALATED: Financial transactions require Founder approval."
    else:
        verdict = "APPROVED: Plan passes standard policy checks."
    return {"policy_verdict": verdict}

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("pragya", pragya_node)
workflow.add_node("murphy", murphy_node)
workflow.add_node("maryada", maryada_node)

workflow.set_entry_point("pragya")
workflow.add_edge("pragya", "murphy")
workflow.add_edge("murphy", "maryada")
workflow.add_edge("maryada", END)

brahma_app = workflow.compile()

if __name__ == "__main__":
    print("--- Running Real LLM Graph ---")
    initial_state = {"task_id": "1", "input": "Analyze the new FSSAI document for compliance"}
    for output in brahma_app.stream(initial_state):
        pass
    print("\n--- Final Verdict ---")
    print(output)
