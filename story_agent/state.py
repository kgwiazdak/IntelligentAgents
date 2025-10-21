"""State definitions for the storytelling agent."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class AgentState(TypedDict):
    """The data passed between nodes in the LangGraph workflow."""

    story_prompt: str
    story: str
    entities: Dict[str, Any]
    inconsistencies: List[str]
    revision_history: List[str]
