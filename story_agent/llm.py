"""Mock LLM interactions used by the storytelling agent."""

from __future__ import annotations

from typing import Any, Dict, List


def mock_llm_generate_story(prompt: str) -> str:
    """Simulate an LLM generating an initial, inconsistent story."""
    print("\n>>> Calling Mock LLM to GENERATE story...")
    return (
        "In the heart of New York City, Jane, sixteen, married her sweetheart Sam. "
        "It was a beautiful ceremony on a hill overlooking the city's majestic mountains. "
        "To celebrate, they enjoyed a large loaf of fresh bread, a treat Jane had been "
        "craving, even though she was famously allergic to flour."
    )


def mock_llm_extract_entities(story: str) -> Dict[str, Any]:
    """Simulate entity extraction from a story."""
    print("\n>>> Calling Mock LLM to EXTRACT entities...")

    if "eighteen" in story and "flat skyline" in story:
        return {
            "persons": [
                {"name": "Jane", "age": 18, "allergies": ["Flour"]}
            ],
            "events": [
                {"type": "marriage", "participants": ["Jane", "Sam"]},
                {"type": "eat", "person": "Jane", "food": "Gluten-free cake"},
            ],
            "locations": [
                {"name": "New York City", "observed_terrain": "flat skyline"}
            ],
        }

    return {
        "persons": [
            {"name": "Jane", "age": 16, "allergies": ["Flour"]}
        ],
        "events": [
            {"type": "marriage", "participants": ["Jane", "Sam"]},
            {"type": "eat", "person": "Jane", "food": "Bread"},
        ],
        "locations": [
            {"name": "New York City", "observed_terrain": "mountains"}
        ],
    }


def mock_llm_rewrite_story(story: str, inconsistencies: List[str]) -> str:
    """Simulate rewriting the story to address inconsistencies."""
    print("\n>>> Calling Mock LLM to REWRITE story based on inconsistencies...")
    return (
        "In the heart of New York City, Jane, now a joyful eighteen, married her sweetheart Sam. "
        "It was a beautiful ceremony in a penthouse overlooking the city's iconic flat skyline. "
        "To celebrate, they enjoyed a large, delicious gluten-free cake, a special treat Jane could "
        "safely enjoy despite her allergy to flour."
    )
