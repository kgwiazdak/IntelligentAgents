"""LangGraph node implementations for the storytelling agent."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from .llm import (
    mock_llm_extract_entities,
    mock_llm_generate_story,
    mock_llm_rewrite_story,
)
from .state import AgentState

if TYPE_CHECKING:  # pragma: no cover - imported for type hints only
    from .ontology import OntologyChecker


def generate_story_node(state: AgentState) -> AgentState:
    """Node to generate the initial story based on the user's prompt."""
    print("\n--- Node: generate_story ---")
    prompt = state["story_prompt"]
    story = mock_llm_generate_story(prompt)
    return {**state, "story": story}


def extract_entities_node(state: AgentState) -> AgentState:
    """Node to extract entities from the current story."""
    print("\n--- Node: extract_entities ---")
    story = state["story"]
    entities = mock_llm_extract_entities(story)
    return {**state, "entities": entities}


def check_consistency_node(state: AgentState, checker: "OntologyChecker") -> AgentState:
    """Node to check for ontology inconsistencies."""
    print("\n--- Node: check_consistency ---")
    entities = state["entities"]

    found_inconsistencies: List[str] = []

    for person in entities.get("persons", []):
        if any(
            event["type"] == "marriage" and person["name"] in event["participants"]
            for event in entities.get("events", [])
        ):
            result = checker.check_marriage_age(person["name"], person["age"])
            if result:
                found_inconsistencies.append(result)

        for event in entities.get("events", []):
            if event["type"] == "eat" and event["person"] == person["name"]:
                result = checker.check_allergy(person["name"], person["allergies"], event["food"])
                if result:
                    found_inconsistencies.append(result)

    for location in entities.get("locations", []):
        result = checker.check_city_terrain(location["name"], location["observed_terrain"])
        if result:
            found_inconsistencies.append(result)

    print("\nConsistency Check Complete.")
    if found_inconsistencies:
        print("Inconsistencies Found:")
        for issue in found_inconsistencies:
            print(f"- {issue}")
    else:
        print("No inconsistencies found.")

    return {**state, "inconsistencies": found_inconsistencies}


def rewrite_story_node(state: AgentState) -> AgentState:
    """Node to rewrite the story to fix inconsistencies."""
    print("\n--- Node: rewrite_story ---")
    story = state["story"]
    inconsistencies = state["inconsistencies"]

    new_story = mock_llm_rewrite_story(story, inconsistencies)

    history = state.get("revision_history", [])
    history.append(new_story)

    return {**state, "story": new_story, "revision_history": history}
