"""Command-line entry point for the storytelling agent."""

from __future__ import annotations

import sys
from typing import Any, Dict

from .ontology import OntologyChecker
from .runner import get_initial_results, run_agent
from .workflow import create_app


def build_inputs(initial_prompt: str) -> Dict[str, Any]:
    """Create the initial state for the workflow."""
    return {"story_prompt": initial_prompt, "revision_history": []}


def main() -> None:
    print("===================================")
    print("  Ontology-Driven Story Agent      ")
    print("===================================")

    checker = OntologyChecker("final_version3.rdf")
    if not checker.onto:
        print(
            "\nAgent cannot run because the ontology failed to load. Please fix the errors in "
            "'final_version3.rdf' and try again."
        )
        sys.exit(1)

    app = create_app(checker)

    initial_prompt = "Write a story about Jane and Sam getting married in New York."
    inputs = build_inputs(initial_prompt)

    print("\n--- Starting Agent Run ---")
    final_state = run_agent(app, inputs)

    initial_story, initial_inconsistencies = get_initial_results(app, inputs)

    print("\n===================================")
    print("       Agent Run Complete          ")
    print("===================================")

    print("\n--- Initial Story (with inconsistencies) ---")
    print(initial_story)

    print("\n--- Final, Consistent Story ---")
    print(final_state["story"])

    print("\n--- Inconsistencies Found & Fixed ---")
    for issue in initial_inconsistencies:
        print(f"- {issue}")


if __name__ == "__main__":
    main()
