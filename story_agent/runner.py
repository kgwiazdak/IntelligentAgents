"""Utilities to execute the storytelling agent workflow."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .state import AgentState


def run_agent(app: Any, inputs: Dict[str, Any]) -> AgentState:
    """Stream the workflow and return the final state."""
    final_state: AgentState | None = None
    for step in app.stream(inputs):
        state_key = next(iter(step.keys()))
        final_state = step[state_key]
        print(f"\nCompleted step: '{state_key}'")
    if final_state is None:
        raise RuntimeError("Agent run produced no state.")
    return final_state


def get_initial_results(app: Any, inputs: Dict[str, Any]) -> Tuple[str, List[str]]:
    """Return the initial story and the inconsistencies found on first pass."""
    initial_stream = app.stream(inputs)
    initial_story = next(initial_stream)["generate_story"]["story"]
    _ = next(initial_stream)  # extract_entities result is not used directly
    check_state = next(initial_stream)["check_consistency"]
    return initial_story, check_state["inconsistencies"]
