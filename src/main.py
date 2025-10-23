import json
import re
from typing import List, Any
from typing import TypedDict, Tuple

from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

from src.ontology_checker import OntologyChecker
from src.scenarios import *
from src.llms import llm_rewriter, llm_extractor, prompt_extractor, rewriting_template
from src.facts2triples import convert_schema_to_triples

class AgentState(TypedDict):
    original_story: str
    current_story: str
    extracted_facts: List[Tuple[str, str, Any]]
    inconsistencies: List[str]
    iteration_count: int
    max_iterations: int


checker = OntologyChecker("./final_version5.rdf")

chain_extractor = prompt_extractor | llm_extractor | StrOutputParser()

def extract_facts(state: AgentState) -> dict:
    print(f"\n--- NODE: Fact extraction (Interation {state['iteration_count']})")
    try:
        response_string = chain_extractor.invoke({"story": state['current_story']})
        data_root = json.loads(response_string)
        if 'data' not in data_root:
            return {"extracted_facts": []}
        triples = convert_schema_to_triples(data_root['data'])
        print(f"Generated {len(triples)} triples.")
        return {"extracted_facts": triples}
    except json.JSONDecodeError as e:
        print(f"Received:\n{response_string}")
        return {"extracted_facts": []}
    except Exception as e:
        print(f"Error: {e}")
        return {"extracted_facts": []}


def query_ontology(state: AgentState) -> dict:
    print("--- NODE: Ontology and reasoning")
    facts = state["extracted_facts"]
    if not facts:
        return {"inconsistencies": []}
    print(facts)
    violations = checker.check_consistency(facts)
    return {"inconsistencies": violations}


def rewrite_story(state: AgentState) -> dict:
    print("--- NODE: Fixing issues and rewriting ---")

    errors_list = "\n".join(state["inconsistencies"])
    original_story = state["original_story"]

    prompt_template = rewriting_template(original_story, errors_list)

    response = llm_rewriter.invoke(prompt_template)
    new_story = response.content.strip()

    if new_story.startswith("Rewritten Story:"): new_story = new_story.replace("Rewritten Story:", "").strip()
    if new_story.startswith("Here is the rewritten story:"): new_story = new_story.replace(
        "Here is the rewritten story:", "").strip()
    new_story = re.sub(r'\s*\([^)]*\)$', '', new_story).strip()

    print(f"Rewrited history:\n{new_story}")

    return {
        "current_story": new_story,
        "iteration_count": state["iteration_count"] + 1,
        "inconsistencies": []
    }


def decide_next_step(state: AgentState) -> str:
    print("--- NODE: Checking violoaitons (decision) ---")
    if not state["inconsistencies"]:
        print("Decision: No violences. Ended"); return "end"
    if state["iteration_count"] >= state["max_iterations"]: print(
        f"Decision: Interation range error ({state['max_iterations']}). Ended."); return "end"
    print(f"Decision: Found {len(state['inconsistencies'])} violations. Rewriting.")
    return "rewrite"

def create_agent_state():
    workflow = StateGraph(AgentState)
    workflow.add_node("extract", extract_facts)
    workflow.add_node("check", query_ontology)
    workflow.add_node("rewrite", rewrite_story)
    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "check")
    workflow.add_conditional_edges("check", decide_next_step, {"end": END, "rewrite": "rewrite"})
    workflow.add_edge("rewrite", "extract")
    app = workflow.compile()
    return app


stories_to_run = {
    "STORY_1": STORY_1,
    "STORY_2": STORY_2,
    "STORY_3": STORY_3,
    "STORY_4": STORY_4,
    "STORY_5": STORY_5,
    "STORY_6": STORY_6,
    "STORY_7": STORY_7,
    'STORY_8': STORY_8,
    'STORY_9': STORY_9,
    "STORY_10": STORY_10,
    "STORY_11": STORY_11,
    "STORY_12": STORY_12,
    "STORY_13": STORY_13,
    "STORY_14": STORY_14,
    "STORY_15": STORY_15,
}
if __name__ == "__main__":
    app = create_agent_state()
    for name, story_text in stories_to_run.items():
        print(f"=== Run AGENT FOR: {name} ===")
        inputs = {"original_story": story_text, "current_story": story_text, "extracted_facts": [],
                  "inconsistencies": [], "iteration_count": 1, "max_iterations": 3}
        final_state_snapshot = {}
        for event in app.stream(inputs, stream_mode="values"):
            final_state_snapshot = event
        if final_state_snapshot:
            print(f"Original story:\n{final_state_snapshot.get('original_story', 'NO DATA')}")
            final_inconsistencies = final_state_snapshot.get('inconsistencies', [])
            iterations = final_state_snapshot.get('iteration_count', 1) - 1
            print(f"Final story (after {iterations} iterations of rewriting):\n{final_state_snapshot.get('current_story', 'NO DATA')}")
            if not final_inconsistencies:
                print("\nStory succed.")
            else:
                print("\nStory failed. Found the following inconsistencies:")
                for inconsistency in final_inconsistencies:
                    print(f"  - {inconsistency}")
        else:
            print(f"\nERROR: No state for {name}.")
