"""Workflow construction for the storytelling agent."""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from .nodes import (
    check_consistency_node,
    extract_entities_node,
    generate_story_node,
    rewrite_story_node,
)
from .state import AgentState


def should_continue(state: AgentState) -> str:
    """Decide the next step after a consistency check."""
    print("\n--- Edge: should_continue ---")
    if state["inconsistencies"]:
        print("Decision: Inconsistencies found. Routing to rewrite_story.")
        return "rewrite_story"
    print("Decision: No inconsistencies. Routing to END.")
    return END


def create_app(checker: Any):
    """Construct and compile the LangGraph workflow for the agent."""
    workflow = StateGraph(AgentState)

    workflow.add_node("generate_story", generate_story_node)
    workflow.add_node("extract_entities", extract_entities_node)
    workflow.add_node("check_consistency", lambda state: check_consistency_node(state, checker))
    workflow.add_node("rewrite_story", rewrite_story_node)

    workflow.set_entry_point("generate_story")
    workflow.add_edge("generate_story", "extract_entities")
    workflow.add_edge("extract_entities", "check_consistency")
    workflow.add_conditional_edges("check_consistency", should_continue)
    workflow.add_edge("rewrite_story", "extract_entities")

    return workflow.compile()
