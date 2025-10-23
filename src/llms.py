from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

UNIVERSAL_PROMPT_TEMPLATE = """
You are an information extraction system.
Your task is to analyze the story and return a JSON object.
**Important:** Extract facts *strictly and literally* based on the text provided in the story, even if the facts seem illogical or contradict common knowledge. Do not apply external knowledge or assumptions. Consistency checks will be performed separately.
Your JSON response MUST have a root key "data".
The value of "data" should be an object containing lists for "people", "cities", "landmarks", "climates", "weather", and "travels".

1.  For 'people', create a list of objects. Each person object should have:
    - "id": (string, a unique name for the person, e.g., "demo:Alice")
    - "livesInCityID": (string, the ID of the city the person lives in, e.g., "city:Beijing", if mentioned) # <-- NEW FIELD
    - "age": (int, e.g., 17)
    - "isMarriedTo": (string, the ID of the person they married, e.g., "demo:Bob")
    - "isAllergicTo": (string, the ID of the allergen, e.g., "ia2025:Flour")
    - "eats": (list of strings, e.g., ["ia2025:Bread"])
    - "worksAs": (string, the ID of the occupation, e.g., "demo:Baker")
    - "hasCondition": (list of strings, e.g., ["demo:Anemia", "city:ObesityIncrease"]) # <-- Note city prefix here
    - "isReserved": (boolean)
    - "talksToCount": (int, the number of people they talk to)

2.  For 'cities', create a list of objects. Each city object should have:
    - "id": (string, a unique name, e.g., "city:London")
    - "type": (string, e.g., "city:WalkableCity")
    - "terrain": (string, e.g., "city:Mountainous")
    - "population": (int)
    - "isAdjacentTo": (string, the ID of the other city)

3.  For 'landmarks', create a list of objects. Each landmark object should have:
    - "id": (string, e.g., "city:EmpireStateBuilding")
    - "type": (string, e.g., "city:SubwaySystem")
    - "locatedIn": (list of strings, e.g., ["city:NewYork", "city:LosAngeles"])

4.  For 'travels', create a list of objects. Each travel object should have:
    - "id": (string, e.g., "travel:Walk1")
    - "mode": (string, e.g., "travel:Walking")
    - "distance": (float)
    - "duration": (float, in hours)
    - "cost": (float)

5.  For 'climates', create a list of objects. Each climate object should have:
    - "id": (string, e.g., "travel:SaharaClimate")
    - "climateZone": (string, e.g., "travel:Desert")
    - "allowsForFood": (boolean)

6.  For 'weather', create a list of objects. Each weather object should have:
    - "id": (string, e.g., "travel:Weather1")
    - "weatherState": (string, e.g., "travel:Snow")
    - "temperature": (float)

Base entity IDs on the name (e.g., 'Alice' becomes 'demo:Alice', 'Paris' becomes 'city:Paris').
Only include keys if the information is present in the story. Use correct prefixes (demo:, city:, ia2025:, travel:).
Return ONLY the JSON object.

Story to analyze:
{story}
"""

prompt_extractor = PromptTemplate(
    template=UNIVERSAL_PROMPT_TEMPLATE,
    input_variables=["story"]
)

print("Inicjalizing agent")
try:
    llm_extractor = ChatOllama(model="llama3.1").bind(format="json")
    llm_extractor.invoke("Hi. Return {'status':'ok'}")
    print("LLM extractor (JSON mode) ready")
except Exception as e:
    print(f"ERROR: {e}")
    exit()

try:
    llm_rewriter = ChatOllama(model="llama3.1")
    llm_rewriter.invoke("Hi")
    print("LLM rewriter ready")
except Exception as e:
    print(f"ERROR: {e}")
    exit()