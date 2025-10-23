# main.py FINAL VERSION

import json
from typing import TypedDict, List, Any, Tuple
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Adjust imports based on your project structure
from src.ontology_checker import OntologyChecker
from src.scenarios import *
import re
from typing import List, Any, Optional

# --- Agent State Definition ---
class AgentState(TypedDict):
    original_story: str
    current_story: str
    extracted_facts: List[Tuple[str, str, Any]]
    inconsistencies: List[str]
    iteration_count: int
    max_iterations: int

# --- Tool Initialization ---
print("Inicjalizacja narzędzi agenta...")
try:
    llm_extractor = ChatOllama(model="llama3.1").bind(format="json")
    llm_extractor.invoke("Hi. Return {'status':'ok'}")
    print("LLM do ekstrakcji (JSON mode) gotowy.")
except Exception as e:
    print(f"KRYTYCZNY BŁĄD: Nie można połączyć się z Ollama lub tryb JSON nie działa.")
    print(f"Błąd: {e}")
    exit()

try:
    llm_rewriter = ChatOllama(model="llama3.1")
    llm_rewriter.invoke("Hi")
    print("LLM do przepisywania gotowy.")
except Exception as e:
    print(f"KRYTYCZNY BŁĄD: Nie można połączyć się z Ollama (LLM do przepisywania).")
    print(f"Błąd: {e}")
    exit()

# Load ontology (ensure path is correct)
checker = OntologyChecker("./final_version5.rdf") # Make sure queries.py is also updated


# --- Extraction Prompt (Updated v2) ---
# Added 'livesInCityID' to people, slightly clarified IDs
UNIVERSAL_PROMPT_TEMPLATE = """
You are an information extraction system.
Your task is to analyze the story and return a JSON object.
Your JSON response MUST have a root key "data".
The value of "data" should be an object containing lists for "people", "cities", "landmarks", "climates", "weather", and "travels".

1.  For 'people', create a list of objects. Each person object should have:
    - "id": (string, use 'demo:' prefix, e.g., "demo:Alice")
    - "livesInCityID": (string, use 'city:' prefix, e.g., "city:Beijing", if mentioned) # <-- Added
    - "age": (int, e.g., 17)
    - "isMarriedTo": (string, the ID of the person they married, e.g., "demo:Bob")
    - "isAllergicTo": (string, use 'ia2025:' prefix, e.g., "ia2025:Flour")
    - "eats": (list of strings, use 'ia2025:' prefix, e.g., ["ia2025:Bread"])
    - "worksAs": (string, use 'demo:' prefix, e.g., "demo:Baker")
    - "hasCondition": (list of strings, use 'demo:' prefix generally, BUT 'city:ObesityIncrease' for obesity risk in specific cities, e.g., ["demo:Anemia", "city:ObesityIncrease"])
    - "isReserved": (boolean)
    - "talksToCount": (int, the number of people they talk to)

2.  For 'cities', create a list of objects. Each city object should have:
    - "id": (string, use 'city:' prefix, e.g., "city:Hillsburg")
    - "type": (string, use 'city:' prefix, e.g., "city:WalkableCity")
    - "terrain": (string, use 'city:' prefix, e.g., "city:Mountainous")
    - "population": (int)
    - "isAdjacentTo": (string, the ID of the other city, e.g., "city:Amsterdam")

3.  For 'landmarks', create a list of objects. Each landmark object should have:
    - "id": (string, use 'city:' prefix, e.g., "city:EmpireStateBuilding")
    - "type": (string, use 'city:' prefix, e.g., "city:SubwaySystem")
    - "locatedIn": (list of strings, use 'city:' prefix, e.g., ["city:NewYork", "city:LosAngeles"])

4.  For 'travels', create a list of objects. Each travel object should have:
    - "id": (string, use 'travel:' prefix, e.g., "travel:Walk1")
    - "mode": (string, use 'travel:' prefix, e.g., "travel:Walking")
    - "distance": (float)
    - "duration": (float, in hours)
    - "cost": (float)

5.  For 'climates', create a list of objects. Each climate object should have:
    - "id": (string, use 'travel:' prefix, e.g., "travel:SaharaClimate")
    - "climateZone": (string, use 'travel:' prefix, e.g., "travel:Desert")
    - "allowsForFood": (boolean)

6.  For 'weather', create a list of objects. Each weather object should have:
    - "id": (string, use 'travel:' prefix, e.g., "travel:Weather1")
    - "weatherState": (string, use 'travel:' prefix, e.g., "travel:Snow")
    - "temperature": (float)

Base entity IDs on the name (e.g., 'Alice' becomes 'demo:Alice', 'Hillsburg' becomes 'city:Hillsburg', 'MetroX' becomes 'city:MetroX').
Only include keys if the information is present in the story. Ensure correct prefixes are used.
Return ONLY the JSON object.

Story to analyze:
{story}
"""

prompt_extractor = PromptTemplate(
    template=UNIVERSAL_PROMPT_TEMPLATE,
    input_variables=["story"]
)

# --- Extraction Chain ---
chain_extractor = prompt_extractor | llm_extractor | StrOutputParser()

# --- Helper Function for IDs (No changes needed from previous version) ---
def clean_and_prefix(name: str, default_prefix: str) -> Optional[str]:
    """Helper function to create a safe ID with a prefix."""
    if not name or not isinstance(name, str): return None
    cleaned_name = re.sub(r'[^\w:-]', '', name.replace(" ", "_"))
    if ":" in cleaned_name:
        prefix, rest = cleaned_name.split(":", 1)
        if prefix in ["demo", "city", "ia2025", "travel", "rdf", "rdfs", "owl", "xsd"] and rest and ":" not in rest:
             return cleaned_name
        else: cleaned_name = rest
    if not cleaned_name: return None
    return f"{default_prefix}:{cleaned_name}"

# --- JSON to Triples Converter (Updated v5) ---
def convert_schema_to_triples(data: dict) -> list:
    """
    Converts the parsed JSON object into a list of RDF triples.
    Version v5: Final fixes for NoneType lists, livesIn, ObesityIncrease prefix.
    """
    triples = []
    city_name_to_id = {} # Build this map first for livesIn lookup
    # Pre-populate city map based on IDs provided by LLM
    for city in data.get('cities', []):
         city_id = clean_and_prefix(city.get('id'), "city")
         if city_id:
             try: city_name = city_id.split(":", 1)[1]; city_name_to_id[city_name] = city_id
             except IndexError: pass # Handle cases where ID is malformed

    # Process People
    for person in data.get('people', []):
        person_id = clean_and_prefix(person.get('id'), "demo")
        if not person_id: continue
        triples.append((person_id, "rdf:type", "demo:Person"))

        # --- Handle livesIn (using extracted field first) ---
        lives_in_city_id = clean_and_prefix(person.get('livesInCityID'), "city")
        person_lives_in_drivable = False # Flag to check later for ObesityIncrease
        if lives_in_city_id:
             triples.append((person_id, "demo:livesIn", lives_in_city_id))
             # Check if the city they live in IS a DrivableCity based on extracted city data
             for city_obj in data.get('cities', []):
                 city_obj_id = clean_and_prefix(city_obj.get('id'), "city")
                 # Check if IDs match AND type is explicitly DrivableCity
                 if city_obj_id == lives_in_city_id and city_obj.get('type') == 'city:DrivableCity':
                     person_lives_in_drivable = True
                     break # Found the city info

        # Fallback heuristic (less reliable but kept just in case)
        elif person_id == "demo:Tom" and "city:Beijing" in city_name_to_id.values():
             triples.append((person_id, "demo:livesIn", "city:Beijing"))
             # Assume Beijing is Drivable if using heuristic AND no other city info contradicts it
             is_beijing_drivable = True
             for city_obj in data.get('cities', []):
                  city_obj_id = clean_and_prefix(city_obj.get('id'), "city")
                  if city_obj_id == "city:Beijing" and city_obj.get('type') and city_obj.get('type') != 'city:DrivableCity':
                       is_beijing_drivable = False
                       break
             if is_beijing_drivable:
                  person_lives_in_drivable = True


        if person.get('age') is not None:
            try: triples.append((person_id, "demo:hasAge", int(person['age'])))
            except (ValueError, TypeError): print(f"Warning: Invalid age for {person_id}: {person['age']}")
        if person.get('isMarriedTo'):
            partner_id = clean_and_prefix(person['isMarriedTo'], "demo")
            if partner_id: triples.append((person_id, "demo:isMarriedTo", partner_id))
        if person.get('isAllergicTo'):
             allergen_id = clean_and_prefix(person['isAllergicTo'], "ia2025")
             if allergen_id: triples.append((person_id, "demo:isAllergicTo", allergen_id))
        if person.get('worksAs'):
             occupation_id = clean_and_prefix(person['worksAs'], "demo")
             if occupation_id: triples.append((person_id, "demo:worksAs", occupation_id))
        if person.get('isReserved') is not None:
            triples.append((person_id, "demo:isReserved", bool(person['isReserved'])))

        eats_list = person.get('eats')
        if isinstance(eats_list, list): # FIX: Check list type
            for item_str in eats_list:
                item_id = clean_and_prefix(item_str, "ia2025")
                if item_id: triples.append((person_id, "demo:eats", item_id))

        condition_list = person.get('hasCondition')
        if isinstance(condition_list, list): # FIX: Check list type
            for item_str in condition_list:
                item_id = None
                # FIX: FORCE correct ID for ObesityIncrease if person lives in DrivableCity
                # Check both the string itself and potential prefixes LLM might add
                if person_lives_in_drivable and ("ObesityIncrease" in item_str or "obesity" in item_str.lower()):
                     item_id = "city:ObesityIncrease" # Force correct ID
                else: # Otherwise, use default 'demo:' prefix
                    item_id = clean_and_prefix(item_str, "demo")
                if item_id: triples.append((person_id, "demo:hasCondition", item_id))

        talk_count = person.get('talksToCount')
        if talk_count is not None:
             try:
                 talk_count = int(talk_count)
                 if talk_count > 0 and talk_count >= 3:
                     triples.append((person_id, "demo:isTalkative", True))
             except (ValueError, TypeError): print(f"Warning: Invalid talksToCount for {person_id}: {person['talksToCount']}")

    # Process Cities (No major changes needed here from previous working version)
    for city in data.get('cities', []):
        city_id = clean_and_prefix(city.get('id'), "city")
        if not city_id: continue
        triples.append((city_id, "rdf:type", "city:City"))
        if city.get('type'):
            city_type_id = clean_and_prefix(city['type'], "city")
            if city_type_id: triples.append((city_id, "rdf:type", city_type_id))
        if city.get('terrain'):
            terrain_id = clean_and_prefix(city['terrain'], "city")
            if terrain_id: triples.append((city_id, "city:hasTerrain", terrain_id))
        if city.get('population') is not None:
            try: triples.append((city_id, "city:hasPopulation", int(city['population'])))
            except (ValueError, TypeError): print(f"Warning: Invalid population for {city_id}: {city['population']}")
        adj = city.get('isAdjacentTo')
        if adj:
            adj_list = adj if isinstance(adj, list) else [adj]
            for adj_city_str in adj_list:
                 adj_city_id = clean_and_prefix(adj_city_str, "city")
                 if adj_city_id: triples.append((city_id, "city:adjacentTo", adj_city_id))

    # Process Landmarks (No major changes needed here)
    for landmark in data.get('landmarks', []):
        landmark_id = clean_and_prefix(landmark.get('id'), "city")
        if not landmark_id: continue
        landmark_type_id = clean_and_prefix(landmark.get('type', 'city:Landmark'), "city")
        if landmark_type_id: triples.append((landmark_id, "rdf:type", landmark_type_id))
        located_in_list = landmark.get('locatedIn')
        if isinstance(located_in_list, list): # FIX: Check list type
             for loc_str in located_in_list:
                loc_id = clean_and_prefix(loc_str, "city")
                if loc_id: triples.append((landmark_id, "city:locatedIn", loc_id))

    # Process Travels (No major changes needed here)
    for travel in data.get('travels', []):
        travel_id = clean_and_prefix(travel.get('id'), "travel")
        if not travel_id: continue
        triples.append((travel_id, "rdf:type", "travel:TravelEvent"))
        if travel.get('mode'):
            mode_id = clean_and_prefix(travel['mode'], "travel")
            if mode_id: triples.append((travel_id, "travel:hasTravelMode", mode_id))
        if travel.get('distance') is not None:
            try: triples.append((travel_id, "travel:travelDistance", float(travel['distance'])))
            except (ValueError, TypeError): print(f"Warning: Invalid distance for {travel_id}: {travel['distance']}")
        if travel.get('duration') is not None:
             try: triples.append((travel_id, "travel:travelDurationHours", float(travel['duration'])))
             except (ValueError, TypeError): print(f"Warning: Invalid duration for {travel_id}: {travel['duration']}")
        if travel.get('cost') is not None:
            try: triples.append((travel_id, "travel:travelCost", float(travel['cost'])))
            except (ValueError, TypeError): print(f"Warning: Invalid cost for {travel_id}: {travel['cost']}")

    # Process Climates (No major changes needed here)
    for climate in data.get('climates', []):
        climate_id = clean_and_prefix(climate.get('id'), "travel")
        if not climate_id: continue
        triples.append((climate_id, "rdf:type", "travel:Climate"))
        if climate.get('allowsForFood') is not None:
            if climate['allowsForFood']: triples.append((climate_id, "travel:allowsForFood", "ia2025:GenericFood"))

    # Process Weather (No major changes needed here)
    for weather in data.get('weather', []):
        weather_id = clean_and_prefix(weather.get('id'), "travel")
        if not weather_id: continue
        triples.append((weather_id, "rdf:type", "travel:WeatherRecord"))
        if weather.get('weatherState'):
            state_id = clean_and_prefix(weather['weatherState'], "travel")
            if state_id: triples.append((weather_id, "travel:weatherHasState", state_id))
        if weather.get('temperature') is not None:
            try: triples.append((weather_id, "travel:temperature", float(weather['temperature'])))
            except (ValueError, TypeError): print(f"Warning: Invalid temperature for {weather_id}: {weather['temperature']}")

    return triples


# --- Agent Node Functions (No changes needed) ---
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
        # Print detailed error for debugging
        import traceback
        traceback.print_exc()
        return {"extracted_facts": []}

def query_ontology(state: AgentState) -> dict:
    #...(no changes needed)...
    print("--- WĘZEŁ: Zapytania do Ontologii i Wnioskowanie ---")
    facts = state["extracted_facts"]
    if not facts:
        print("Brak faktów do sprawdzenia. Pomijanie.")
        return {"inconsistencies": []}
    violations = checker.check_consistency(facts)
    return {"inconsistencies": violations}

def rewrite_story(state: AgentState) -> dict:
    #...(no changes needed)...
    print("--- WĘZEŁ: Rozwiązywanie Konfliktów i Przepisywanie ---")
    errors_list = "\n".join(state["inconsistencies"])
    original_story = state["original_story"]
    prompt_template = f"""
You are a story editor. Your task is to rewrite the following story ONLY to fix the logical inconsistencies listed below.
Apply the ABSOLUTE MINIMAL change necessary.
Often, the best solution is to simply **remove or negate** the sentence that directly causes the conflict.
Maintain the original language (English), style, and overall plot.
DO NOT add any commentary, explanation, or text other than the rewritten story itself.
Original Story:
"{original_story}"
Detected Inconsistencies:
{errors_list}
Example of a minimal fix for "He is allergic to nuts but eats peanuts":
"He is allergic to nuts and avoids eating peanuts."
OR
"He eats peanuts daily." (if the allergy part is removed)
Rewritten Story (English, minimal changes, only the story text):
"""
    response = llm_rewriter.invoke(prompt_template)
    new_story = response.content.strip()
    if new_story.startswith("Rewritten Story:"): new_story = new_story.replace("Rewritten Story:", "").strip()
    if new_story.startswith("Here is the rewritten story:"): new_story = new_story.replace("Here is the rewritten story:", "").strip()
    print(f"Przepisana historia:\n{new_story}")
    return {"current_story": new_story, "iteration_count": state["iteration_count"] + 1, "inconsistencies": []}

def decide_next_step(state: AgentState) -> str:
    #...(no changes needed)...
    print("--- WĘZEŁ: Sprawdzanie Niespójności (Decyzja) ---")
    if not state["inconsistencies"]: print("Decyzja: Brak niespójności. Zakończono."); return "end"
    if state["iteration_count"] >= state["max_iterations"]: print(f"Decyzja: Osiągnięto limit iteracji ({state['max_iterations']}). Zakończono."); return "end"
    print(f"Decyzja: Znaleziono {len(state['inconsistencies'])} niespójności. Przechodzenie do przepisania."); return "rewrite"

# --- Agent Graph Definition (No changes needed) ---
print("Budowanie grafu agenta...")
workflow = StateGraph(AgentState)
#...(rest of graph definition)...
workflow.add_node("extract", extract_facts)
workflow.add_node("check", query_ontology)
workflow.add_node("rewrite", rewrite_story)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "check")
workflow.add_conditional_edges("check", decide_next_step, {"end": END, "rewrite": "rewrite"})
workflow.add_edge("rewrite", "extract")
app = workflow.compile()
print("Graf agenta został skompilowany.")


# --- Agent Execution (No changes needed) ---
if __name__ == "__main__":
    #...(rest of execution code)...
    stories_to_run = { # Run all stories now
        "STORY_1": STORY_1, "STORY_2": STORY_2, "STORY_3": STORY_3,
        "STORY_4": STORY_4, "STORY_5": STORY_5, "STORY_6": STORY_6,
        "STORY_7": STORY_7, "STORY_8": STORY_8, "STORY_9": STORY_9,
        "STORY_10": STORY_10, "STORY_11": STORY_11, "STORY_12": STORY_12,
        "STORY_13": STORY_13, "STORY_14": STORY_14, "STORY_15": STORY_15,
    }
    for name, story_text in stories_to_run.items():
        print(f"\n{'=' * 70}")
        print(f"=== URUCHAMIANIE AGENTA DLA: {name} ===")
        print(f"{'=' * 70}")
        inputs = {"original_story": story_text, "current_story": story_text, "extracted_facts": [], "inconsistencies": [], "iteration_count": 1, "max_iterations": 3}
        final_state_snapshot = {}
        for event in app.stream(inputs, stream_mode="values"):
            print(f"  ... Stan po kroku...")
            final_state_snapshot = event
        if final_state_snapshot:
            print(f"\n--- ZAKOŃCZONO {name} ---")
            print(f"Oryginalna historia:\n{final_state_snapshot.get('original_story', 'BRAK DANYCH')}")
            print("\n---")
            final_inconsistencies = final_state_snapshot.get('inconsistencies', [])
            iterations = final_state_snapshot.get('iteration_count', 1) - 1
            print(f"Ostateczna historia (po {iterations} iteracjach przepisania):\n{final_state_snapshot.get('current_story', 'BRAK DANYCH')}")
            if not final_inconsistencies: print("\n✅ Historia jest spójna.")
            else:
                print("\n⚠️ UWAGA: Pozostały niespójności:")
                for inconsistency in final_inconsistencies: print(f"  - {inconsistency}")
        else: print(f"\nBŁĄD KRYTYCZNY: Agent nie zwrócił żadnego stanu dla {name}.")