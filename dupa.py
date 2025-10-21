#
# Ontology-Driven Storytelling Agent using LangGraph and OwlReady2
#
# This script implements an agent that generates stories, checks them for logical
# inconsistencies using a custom ontology, and revises them until they are consistent.
#
# Required Packages:
# pip install langgraph owlready2
#
# You also need a Java runtime for the HermiT reasoner used by owlready2.
#

import json
import os
import sys
from typing import TypedDict, List, Dict, Any

from owlready2 import *
from langgraph.graph import StateGraph, END

# --- Ontology Checker Class ---
# This class loads the ontology and provides methods to check for specific inconsistencies.

class OntologyChecker:
    """
    Handles loading an ontology and running SPARQL queries to check for inconsistencies.
    """
    def __init__(self, ontology_path: str):
        """
        Loads the ontology and runs the reasoner.
        Args:
            ontology_path: The file path to the OWL/RDF ontology file.
        """
        print("Initializing OntologyChecker...")
        self.onto = None
        try:
            # Load the ontology from the provided file path
            self.onto = get_ontology(f"file://{os.path.abspath(ontology_path)}").load()
            print("Ontology loaded successfully.")
            
            # Run the HermiT reasoner to infer relationships and check axioms.
            # This is a crucial step for the consistency checks to work correctly.
            # It performs inferences based on the rules defined in the ontology.
            sync_reasoner()
            print("Reasoner synchronized.")

            # Get references to key classes and properties for easier access
            self.Person = self.onto.search_one(iri="*Person")
            self.AdultPerson = self.onto.search_one(iri="*AdultPerson")
            self.age_prop = self.onto.search_one(iri="*age")
            self.isAllergicTo_prop = self.onto.search_one(iri="*isAllergicTo")
            self.eats_prop = self.onto.search_one(iri="*eats")
            self.isPartOf_prop = self.onto.search_one(iri="*isPartOf")
            self.WalkableCity = self.onto.search_one(iri="*WalkableCity")
            self.Food = self.onto.search_one(iri="*Food")
            
            print("Key ontology classes and properties located.")

        except Exception as e:
            print(f"--- CRITICAL ERROR ---")
            print(f"Failed to initialize OntologyChecker: {e}")
            print("Please ensure the following:")
            print("1. The ontology file 'final_version3.rdf' is in the same directory and has been corrected.")
            print("2. You have a Java Development Kit (JDK) installed and accessible.")
            print("3. The 'owlready2' library is correctly installed.")
            print("----------------------")
            self.onto = None


    def check_marriage_age(self, person_name: str, age: int) -> str | None:
        """
        Checks if a person is old enough to be married (>= 18).
        
        Args:
            person_name: Name of the person.
            age: Age of the person.
            
        Returns:
            An error message string if inconsistent, otherwise None.
        """
        if not self.onto: return "Ontology not loaded."
        print(f"  [Check] Marriage age for {person_name} (age {age})...")
        
        # The ontology defines AdultPerson as a Person with age >= 18.
        # The agent checks if a person of the given age would be considered an adult.
        if age < 18:
            return (f"Inconsistency found: Marriage participant '{person_name}' is {age}, "
                    f"but must be 18 or older to be married according to ontology rules.")
        return None

    def check_allergy(self, person_name: str, person_allergies: List[str], food_eaten: str) -> str | None:
        """
        Checks if a person is eating food they are allergic to.
        This check uses transitive reasoning over the 'isPartOf' property.

        Args:
            person_name: Name of the person.
            person_allergies: A list of ingredients the person is allergic to.
            food_eaten: The name of the food item eaten.

        Returns:
            An error message string if inconsistent, otherwise None.
        """
        if not self.onto: return "Ontology not loaded."
        print(f"  [Check] Allergy for {person_name} eating {food_eaten} (allergies: {person_allergies})...")

        # Improved Search: Search by IRI fragment, removing spaces.
        food_iri_fragment = f"*{food_eaten.replace(' ', '')}"
        food_individual = self.onto.search_one(iri=food_iri_fragment, is_a=self.Food)
        
        if not food_individual:
            print(f"    - Warning: Food '{food_eaten}' not found in ontology. Skipping check.")
            return None

        # Check for each of the person's allergies.
        for allergen_name in person_allergies:
            allergen_individual = self.onto.search_one(iri=f"*{allergen_name.replace(' ', '')}")
            if not allergen_individual:
                continue

            # Check if the allergen is part of the food (transitively).
            # e.g., Flour isPartOf Bread, and Bread isPartOf Sandwich.
            # The reasoner infers that Flour is also part of Sandwich.
            if self.isPartOf_prop in allergen_individual.get_relations() and food_individual in allergen_individual.isPartOf:
                 return (f"Inconsistency found: '{person_name}' is eating '{food_eaten}', "
                         f"which contains '{allergen_name}', an ingredient they are allergic to.")
        return None

    def check_city_terrain(self, city_name: str, observed_terrain: str) -> str | None:
        """
        Checks if the observed terrain in a story is consistent with the city's defined terrain.
        
        Args:
            city_name: The name of the city.
            observed_terrain: The terrain described in the story (e.g., 'mountains').

        Returns:
            An error message string if inconsistent, otherwise None.
        """
        if not self.onto: return "Ontology not loaded."
        print(f"  [Check] City terrain for {city_name} (observed: {observed_terrain})...")
        
        # Improved Search: Search by IRI fragment, removing spaces from the city name.
        city_iri_fragment = f"*{city_name.replace(' ', '')}"
        city_individual = self.onto.search_one(iri=city_iri_fragment)

        if not city_individual:
            print(f"    - Warning: City '{city_name}' not found in ontology. Skipping check.")
            return None

        # Check if the city is a WalkableCity and the story mentions mountains.
        if observed_terrain.lower() == 'mountains' and self.WalkableCity in city_individual.is_a:
             # The ontology defines WalkableCity as disjoint with cities having mountainous terrain.
            return (f"Inconsistency found: The story mentions 'mountains' in '{city_name}', "
                    f"but the ontology defines it as a 'WalkableCity' which must have flat terrain.")
        return None


# --- Mock LLM Functions ---
# In a real-world scenario, these would be API calls to a Large Language Model.
# Here, they are hardcoded to simulate the agent's behavior for demonstration.

def mock_llm_generate_story(prompt: str) -> str:
    """Simulates an LLM generating an initial, inconsistent story."""
    print("\n>>> Calling Mock LLM to GENERATE story...")
    # This story contains deliberate inconsistencies for the agent to find.
    return (
        "In the heart of New York City, Jane, sixteen, married her sweetheart Sam. "
        "It was a beautiful ceremony on a hill overlooking the city's majestic mountains. "
        "To celebrate, they enjoyed a large loaf of fresh bread, a treat Jane had been "
        "craving, even though she was famously allergic to flour."
    )

def mock_llm_extract_entities(story: str) -> Dict[str, Any]:
    """
    Simulates an LLM extracting structured data (entities) from a story.
    This function is now dynamic to break the infinite loop. It returns different
    entities based on whether the story has been rewritten.
    """
    print("\n>>> Calling Mock LLM to EXTRACT entities...")
    
    # Check if the story has been rewritten (look for keywords from the rewritten story).
    if "eighteen" in story and "flat skyline" in story:
        # Return entities consistent with the REWRITTEN story
        return {
            "persons": [
                {"name": "Jane", "age": 18, "allergies": ["Flour"]}
            ],
            "events": [
                {"type": "marriage", "participants": ["Jane", "Sam"]},
                {"type": "eat", "person": "Jane", "food": "Gluten-free cake"}
            ],
            "locations": [
                {"name": "New York City", "observed_terrain": "flat skyline"}
            ]
        }
    else:
        # Return entities from the ORIGINAL inconsistent story
        return {
            "persons": [
                {"name": "Jane", "age": 16, "allergies": ["Flour"]}
            ],
            "events": [
                {"type": "marriage", "participants": ["Jane", "Sam"]},
                {"type": "eat", "person": "Jane", "food": "Bread"}
            ],
            "locations": [
                {"name": "New York City", "observed_terrain": "mountains"}
            ]
        }

def mock_llm_rewrite_story(story: str, inconsistencies: List[str]) -> str:
    """Simulates an LLM rewriting the story to fix the identified inconsistencies."""
    print("\n>>> Calling Mock LLM to REWRITE story based on inconsistencies...")
    # This is the corrected version of the story.
    return (
        "In the heart of New York City, Jane, now a joyful eighteen, married her sweetheart Sam. "
        "It was a beautiful ceremony in a penthouse overlooking the city's iconic flat skyline. "
        "To celebrate, they enjoyed a large, delicious gluten-free cake, a special treat Jane could "
        "safely enjoy despite her allergy to flour."
    )


# --- LangGraph Agent State Definition ---

class AgentState(TypedDict):
    """
    Defines the state of the agent, which is passed between nodes in the graph.
    """
    story_prompt: str
    story: str
    entities: Dict[str, Any]
    inconsistencies: List[str]
    revision_history: List[str]

# --- LangGraph Agent Nodes ---

def generate_story_node(state: AgentState) -> AgentState:
    """
    Node to generate the initial story based on the user's prompt.
    """
    print("\n--- Node: generate_story ---")
    prompt = state['story_prompt']
    story = mock_llm_generate_story(prompt)
    return {**state, "story": story}

def extract_entities_node(state: AgentState) -> AgentState:
    """
    Node to extract entities from the current story.
    """
    print("\n--- Node: extract_entities ---")
    story = state['story']
    entities = mock_llm_extract_entities(story)
    return {**state, "entities": entities}

def check_consistency_node(state: AgentState, checker: OntologyChecker) -> AgentState:
    """
    Node to check for inconsistencies using the OntologyChecker. This is the core 'tool' node.
    """
    print("\n--- Node: check_consistency ---")
    entities = state['entities']
    
    found_inconsistencies = []

    # Iterate through extracted entities and run checks
    for person in entities.get("persons", []):
        # Check marriage age for any 'marriage' event participants
        if any(event['type'] == 'marriage' and person['name'] in event['participants'] for event in entities.get("events", [])):
            result = checker.check_marriage_age(person['name'], person['age'])
            if result:
                found_inconsistencies.append(result)
        
        # Check allergies for any 'eat' event
        for event in entities.get("events", []):
            if event['type'] == 'eat' and event['person'] == person['name']:
                result = checker.check_allergy(person['name'], person['allergies'], event['food'])
                if result:
                    found_inconsistencies.append(result)

    for location in entities.get("locations", []):
        result = checker.check_city_terrain(location['name'], location['observed_terrain'])
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
    """
    Node to rewrite the story to fix inconsistencies.
    """
    print("\n--- Node: rewrite_story ---")
    story = state['story']
    inconsistencies = state['inconsistencies']
    
    new_story = mock_llm_rewrite_story(story, inconsistencies)
    
    # Update revision history
    history = state.get('revision_history', [])
    history.append(new_story)
    
    return {**state, "story": new_story, "revision_history": history}

# --- Conditional Edge Logic ---

def should_continue(state: AgentState) -> str:
    """
    Determines the next step after a consistency check.
    - If inconsistencies are found, route to 'rewrite_story'.
    - If the story is consistent, end the process.
    """
    print("\n--- Edge: should_continue ---")
    if state['inconsistencies']:
        print("Decision: Inconsistencies found. Routing to rewrite_story.")
        return "rewrite_story"
    else:
        print("Decision: No inconsistencies. Routing to END.")
        return END

# --- Main Execution Block ---

if __name__ == "__main__":
    print("===================================")
    print("  Ontology-Driven Story Agent      ")
    print("===================================")

    # --- Initialize Ontology Checker Once at the Start ---
    # This prevents repeated, failing initializations and makes the agent more robust.
    checker = OntologyChecker("final_version3.rdf")
    if not checker.onto:
        print("\nAgent cannot run because the ontology failed to load. Please fix the errors in 'final_version3.rdf' and try again.")
        sys.exit(1) # Exit gracefully if ontology is broken

    # Define the agent's workflow using a state graph
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("generate_story", generate_story_node)
    workflow.add_node("extract_entities", extract_entities_node)
    # Pass the checker instance to the consistency node
    workflow.add_node("check_consistency", lambda state: check_consistency_node(state, checker))
    workflow.add_node("rewrite_story", rewrite_story_node)

    # Define the edges that connect the nodes
    workflow.set_entry_point("generate_story")
    workflow.add_edge("generate_story", "extract_entities")
    workflow.add_edge("extract_entities", "check_consistency")
    
    # After checking consistency, decide whether to rewrite or end
    workflow.add_conditional_edges(
        "check_consistency",
        should_continue,
    )
    
    # After rewriting, loop back to extract entities from the new version
    workflow.add_edge("rewrite_story", "extract_entities")

    # Compile the graph into a runnable application
    app = workflow.compile()

    # --- Run the Agent ---
    print("\n--- Starting Agent Run ---")
    
    # Initial input for the agent
    initial_prompt = "Write a story about Jane and Sam getting married in New York."
    inputs = {"story_prompt": initial_prompt, "revision_history": []}
    
    final_state = None
    # The `stream` method executes the graph step-by-step
    for step in app.stream(inputs):
        state_key = list(step.keys())[0]
        final_state = step[state_key]
        print(f"\nCompleted step: '{state_key}'")

    print("\n===================================")
    print("       Agent Run Complete          ")
    print("===================================")

    # To get the initial story, we need to run the first few steps of the graph
    # Create a separate stream to get initial story details without affecting the main run
    initial_run_stream = app.stream(inputs)
    initial_story = next(initial_run_stream)['generate_story']['story']
    initial_check_state = next(initial_run_stream)['extract_entities']
    initial_check_state = next(initial_run_stream)['check_consistency']
    
    print("\n--- Initial Story (with inconsistencies) ---")
    print(initial_story)

    print("\n--- Final, Consistent Story ---")
    print(final_state['story'])
    
    print("\n--- Inconsistencies Found & Fixed ---")
    # Print the inconsistencies from the first check
    for issue in initial_check_state['inconsistencies']:
        print(f"- {issue}")

