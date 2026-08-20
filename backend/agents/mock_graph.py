from typing import TypedDict
# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, END

# Define the state schema
class AgentState(TypedDict):
    task_id: str
    input: str
    plan: str
    risk_report: str
    policy_verdict: str

# Mock PRAGYA (Reasoning)
def pragya_node(state: AgentState):
    print(f"[PRAGYA] Received input: {state['input']}")
    return {"plan": f"Generated plan for: {state['input']}"}

# Mock MURPHY (Risk)
def murphy_node(state: AgentState):
    print(f"[MURPHY] Analyzing plan: {state['plan']}")
    return {"risk_report": "Low risk. Minor edge cases identified."}

# Mock MARYADA (Governance)
def maryada_node(state: AgentState):
    print(f"[MARYADA] Checking risk report: {state['risk_report']}")
    if "buy" in state["input"].lower():
        verdict = "Escalated: Purchasing action requires Founder approval."
    else:
        verdict = "Approved: No policy violations."
    return {"policy_verdict": verdict}

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("pragya", pragya_node)
workflow.add_node("murphy", murphy_node)
workflow.add_node("maryada", maryada_node)

# Set edges
workflow.set_entry_point("pragya")
workflow.add_edge("pragya", "murphy")
workflow.add_edge("murphy", "maryada")
workflow.add_edge("maryada", END)

# Compile
brahma_mock_app = workflow.compile()

if __name__ == "__main__":
    print("--- Testing Mock Graph ---")
    initial_state = {"task_id": "1", "input": "Analyze the new FSSAI document"}
    for output in brahma_mock_app.stream(initial_state):
        pass
    print("Final State:", output)
