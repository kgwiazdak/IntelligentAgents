import json
import re
from typing import List, Any
from typing import TypedDict, Tuple

from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

from src.ontology_checker import OntologyChecker
from src.scenarios import *
from src.llms import llm_rewriter, llm_extractor, prompt_extractor
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
    print(f"\n--- WĘZEŁ: Ekstrakcja Faktów (Iteracja {state['iteration_count']}) ---")
    try:
        response_string = chain_extractor.invoke({"story": state['current_story']})
        print(f"Otrzymano JSON od LLM:\n{response_string}")
        data_root = json.loads(response_string)
        if 'data' not in data_root:
            print(">>> BŁĄD: LLM zwrócił JSON bez klucza 'data'. <<<")
            return {"extracted_facts": []}
        triples = convert_schema_to_triples(data_root['data'])
        print(f"Wygenerowano {len(triples)} trójek RDF.")
        return {"extracted_facts": triples}
    except json.JSONDecodeError as e:
        print(f">>> BŁĄD DEKODOWANIA JSON (Model zignorował format='json'?): {e} <<<")
        print(f"Otrzymano:\n{response_string}")
        return {"extracted_facts": []}
    except Exception as e:
        print(f">>> KRYTYCZNY BŁĄD podczas ekstrakcji: {e} <<<")
        return {"extracted_facts": []}


def query_ontology(state: AgentState) -> dict:
    print("--- WĘZEŁ: Zapytania do Ontologii i Wnioskowanie ---")
    facts = state["extracted_facts"]
    if not facts:
        print("Brak faktów do sprawdzenia. Pomijanie.")
        return {"inconsistencies": []}
    print(facts)
    violations = checker.check_consistency(facts)
    return {"inconsistencies": violations}


def rewrite_story(state: AgentState) -> dict:
    """
    Węzeł 3: Przepisywanie Historii. Używa standardowego LLM.
    NOWA WERSJA: Z BARDZIEJ INSTRUKCYJNYM promptem dla sprzecznych cech.
    """
    print("--- WĘZEŁ: Rozwiązywanie Konfliktów i Przepisywanie ---")

    errors_list = "\n".join(state["inconsistencies"])
    original_story = state["original_story"]

    # --- NOWY, BARDZIEJ INSTRUKCYJNY PROMPT ---
    prompt_template = f"""
You are a story editor. Your task is to rewrite the following story ONLY to fix the logical inconsistencies listed below.
Apply the ABSOLUTE MINIMAL change necessary.

**Crucially, if the inconsistency involves a conflict between a described trait (like 'reserved') and a described action (like 'talks to many people'), you MUST choose EITHER the trait OR the action to keep and REMOVE the conflicting part.**

Maintain the original language (English), style, and overall plot.
DO NOT add any commentary, explanation, or text other than the rewritten story itself.

Original Story:
"{original_story}"

Detected Inconsistencies:
{errors_list}

Example fix for "reserved vs talks to many":
Option A (Keep 'reserved'): "Luca is described as 'very reserved.' He preferred to keep to himself at the office."
Option B (Keep 'talks to many'): "Luca, despite initial impressions, chatted with at least six different people every day at the office."

Rewritten Story (English, minimal changes, choose ONE option if traits conflict, only the story text):
"""

    response = llm_rewriter.invoke(prompt_template)
    new_story = response.content.strip()

    # Clean potential LLM preamble
    if new_story.startswith("Rewritten Story:"): new_story = new_story.replace("Rewritten Story:", "").strip()
    if new_story.startswith("Here is the rewritten story:"): new_story = new_story.replace(
        "Here is the rewritten story:", "").strip()
    # Remove potential notes in parentheses added by LLM
    new_story = re.sub(r'\s*\([^)]*\)$', '', new_story).strip()

    print(f"Przepisana historia:\n{new_story}")

    return {
        "current_story": new_story,
        "iteration_count": state["iteration_count"] + 1,
        "inconsistencies": []
    }


def decide_next_step(state: AgentState) -> str:
    print("--- WĘZEŁ: Sprawdzanie Niespójności (Decyzja) ---")
    if not state["inconsistencies"]: print("Decyzja: Brak niespójności. Zakończono."); return "end"
    if state["iteration_count"] >= state["max_iterations"]: print(
        f"Decyzja: Osiągnięto limit iteracji ({state['max_iterations']}). Zakończono."); return "end"
    print(f"Decyzja: Znaleziono {len(state['inconsistencies'])} niespójności. Przechodzenie do przepisania.");
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


# --- Agent Execution ---
stories_to_run = {  # Run all stories now
    # "STORY_1": STORY_1,
    # "STORY_2": STORY_2,
    # "STORY_3": STORY_3,
    # "STORY_4": STORY_4,
    # "STORY_5": STORY_5,
    # "STORY_6": STORY_6,
    # "STORY_7": STORY_7,
    # 'STORY_8': STORY_8,
    # 'STORY_9': STORY_9,
    # "STORY_10": STORY_10, "STORY_11": STORY_11, "STORY_12": STORY_12,
    "STORY_13": STORY_13,
    # "STORY_14": STORY_14, "STORY_15": STORY_15,
}
if __name__ == "__main__":
    app = create_agent_state()
    for name, story_text in stories_to_run.items():
        print(f"=== URUCHAMIANIE AGENTA DLA: {name} ===")
        inputs = {"original_story": story_text, "current_story": story_text, "extracted_facts": [],
                  "inconsistencies": [], "iteration_count": 1, "max_iterations": 3}
        final_state_snapshot = {}
        for event in app.stream(inputs, stream_mode="values"):
            final_state_snapshot = event
        if final_state_snapshot:
            print(f"Oryginalna historia:\n{final_state_snapshot.get('original_story', 'BRAK DANYCH')}")
            final_inconsistencies = final_state_snapshot.get('inconsistencies', [])
            iterations = final_state_snapshot.get('iteration_count', 1) - 1
            print(f"Ostateczna historia (po {iterations} iteracjach przepisania):\n{final_state_snapshot.get('current_story', 'BRAK DANYCH')}")
            if not final_inconsistencies:
                print("\n✅ Historia jest spójna.")
            else:
                print("\n⚠️ UWAGA: Pozostały niespójności:")
                for inconsistency in final_inconsistencies:
                    print(f"  - {inconsistency}")
        else:
            print(f"\nBŁĄD KRYTYCZNY: Agent nie zwrócił żadnego stanu dla {name}.")
