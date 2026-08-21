from __future__ import annotations

from typing import Literal

from langgraph.graph import END, StateGraph

from .nodes.karma import karma_node
from .nodes.maryada import maryada_node
from .nodes.murphy import murphy_node
from .nodes.pragya import pragya_node
from .nodes.rachit import rachit_node
from .state import AgentState


def route_after_maryada(state: AgentState) -> Literal["rachit", "__end__"]:
    verdict = state.get("policy_verdict") or {}
    if verdict.get("approved") is True and verdict.get("requires_human") is not True:
        return "rachit"
    return "__end__"


workflow = StateGraph(AgentState)
workflow.add_node("karma", karma_node)
workflow.add_node("pragya", pragya_node)
workflow.add_node("murphy", murphy_node)
workflow.add_node("maryada", maryada_node)
workflow.add_node("rachit", rachit_node)

workflow.set_entry_point("karma")
workflow.add_edge("karma", "pragya")
workflow.add_edge("pragya", "murphy")
workflow.add_edge("murphy", "maryada")
workflow.add_conditional_edges(
    "maryada",
    route_after_maryada,
    {"rachit": "rachit", "__end__": END},
)
workflow.add_edge("rachit", END)

brahma_app = workflow.compile()
