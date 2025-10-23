# queries.py
# This file contains SPARQL queries used by the OntologyChecker to verify story consistency.

# Define namespaces used throughout the queries
PREFIXES = """
    PREFIX : <http://www.semanticweb.org/user/ontologies/2025/9/untitled-ontology-24#>
    PREFIX demo: <http://www.semanticweb.org/alexandrosxanthopoulos/ontologies/2025/9/ProjectDemo#>
    PREFIX ia2025: <http://example.org/ia2025#>
    PREFIX city: <http://www.semanticweb.org/gwiazdk01/ontologies/2025/8/untitled-ontology-4#>
    PREFIX travel: <http://www.semanticweb.org/rubyorsmth/ontologies/2025/9/untitled-ontology-5#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# --- STORY_1 & STORY_6: Allergy Violation ---
# Checks if a person eats food containing an ingredient they are allergic to.
QUERY_ALLERGY = f"""
{PREFIXES}
SELECT ?person ?food ?ingredient
WHERE {{
    ?person demo:isAllergicTo ?ingredient .
    ?person demo:eats ?food .
    # Check if the allergen ingredient is part of the food eaten
    ?ingredient ia2025:isPartOf ?food .
}}
"""

# --- STORY_2: Drivable City & Health (Requires 'livesIn' relation) ---
# Checks if a person lives in a DrivableCity but doesn't have the expected health impact (ObesityIncrease).
QUERY_DRIVABLE_CITY_OBESITY = f"""
{PREFIXES}
SELECT ?person ?city
WHERE {{
    # Assumes converter adds 'livesIn' relation
    ?person demo:livesIn ?city .
    ?city rdf:type city:DrivableCity .
    # Check if the person does NOT have the expected condition
    FILTER NOT EXISTS {{
        ?person demo:hasCondition city:ObesityIncrease .
    }}
}}
"""

# --- STORY_3: Underage Marriage (Simplified) ---
# Checks if a person is married but is not classified as an AdultPerson (age >= 18) by the reasoner.
QUERY_UNDERAGE_MARRIAGE = f"""
{PREFIXES}
SELECT ?person ?age
WHERE {{
    # Find married individuals (symmetric check)
    {{ ?person demo:isMarriedTo ?spouse . }}
    UNION
    {{ ?spouse demo:isMarriedTo ?person . }}
    # Get their age
    ?person demo:hasAge ?age .
    # Check if the reasoner did NOT infer they are an AdultPerson
    FILTER NOT EXISTS {{
        ?person rdf:type demo:AdultPerson .
    }}
    # Optional but safer: Explicitly check age just in case reasoner fails
    FILTER (?age < 18)
}}
"""

# --- STORY_4: Conflicting Personality Traits (Corrected Property Names) ---
# Checks if a person is simultaneously 'isReserved' and 'isTalkative'.
QUERY_CONFLICTING_TRAITS = f"""
{PREFIXES}
SELECT ?person
WHERE {{
    # Use correct property names from the ontology
    ?person demo:isReserved true .
    ?person demo:isTalkative true .
}}
"""

# --- STORY_5: Baker Missing Oven (Specific Check) ---
# Checks if an instance classified as a Baker does not have the required 'usesTool Oven' relation.
QUERY_PERSON_AS_BAKER_MISSING_OVEN = f"""
{PREFIXES}
SELECT ?person
WHERE {{
    ?person rdf:type demo:Person .
    ?person demo:worksAs demo:Baker . 

    FILTER NOT EXISTS {{
         ?person demo:usesTool ?anyTool .
    }}
}}
"""

# --- STORY_7: Disjoint Health Conditions ---
# Checks if a person has two health conditions declared as disjoint in the ontology.

QUERY_DISJOINT_HEALTH_CONDITIONS_EXPLICIT_CHECK = f"""
{PREFIXES}
SELECT ?person ?conditionClass1 ?conditionClass2
WHERE {{
    # Find a person linked to two different condition class URIs
    ?person demo:hasCondition ?conditionClass1 .
    ?person demo:hasCondition ?conditionClass2 .

    # Ensure we are looking at two different conditions assigned to the person
    FILTER (?conditionClass1 != ?conditionClass2)

    # Now, explicitly check if these two classes are disjoint in the ontology
    # Use UNION for robustness
    {{ ?conditionClass1 owl:disjointWith ?conditionClass2 . }}
    UNION
    {{ ?conditionClass2 owl:disjointWith ?conditionClass1 . }}

    # Avoid duplicate pairs (e.g., Anemia/Cancer and Cancer/Anemia)
    FILTER(STR(?conditionClass1) < STR(?conditionClass2))
}}
"""

# --- STORY_8: Walkable City with Mountainous Terrain ---
# Checks for cities classified as WalkableCity that also have Mountainous terrain (contradiction).
QUERY_WALKABLE_MOUNTAIN_CITY = f"""
{PREFIXES}
SELECT ?city
WHERE {{
    ?city rdf:type city:WalkableCity .
    ?city city:hasTerrain city:Mountainous .
}}
"""

# --- STORY_9: Landmark in Multiple Cities ---
# Checks if any landmark has more than one 'locatedIn' relation.
QUERY_LANDMARK_MULTIPLE_CITIES = f"""
{PREFIXES}
SELECT ?landmark (COUNT(DISTINCT ?city) AS ?distinctCityCount) # Use DISTINCT
WHERE {{
    ?landmark city:locatedIn ?city .
}}
GROUP BY ?landmark
HAVING (COUNT(DISTINCT ?city) > 1) 
"""

# --- STORY_10: Subway System Without a City ---
# Checks if a SubwaySystem lacks the required 'locatedIn' relation.
QUERY_SUBWAY_NO_CITY = f"""
{PREFIXES}
SELECT ?subway
WHERE {{
    ?subway rdf:type city:SubwaySystem .
    FILTER NOT EXISTS {{
        ?subway city:locatedIn ?city .
    }}
}}
"""

# --- STORY_11: City Size/Population Mismatch (Corrected) ---
# Checks if a city's population conflicts with its inferred size class (Small/Medium/Large).
QUERY_CITY_SIZE_POPULATION_MISMATCH = f"""
{PREFIXES}
SELECT ?city ?pop ?typeLabel
WHERE {{
    {{
        # Check LargeCity inconsistency
        ?city city:hasPopulation ?pop .
        ?city rdf:type city:LargeCity . # Relies on reasoner classification
        BIND("LargeCity" as ?typeLabel)
        FILTER (?pop < 1000000) # Population is too small for LargeCity
    }}
    UNION
    {{
        # Check MediumCity inconsistency
        ?city city:hasPopulation ?pop .
        ?city rdf:type city:MediumCity .
        BIND("MediumCity" as ?typeLabel)
        FILTER (?pop < 100000 || ?pop >= 1000000) # Population outside MediumCity range
    }}
    UNION
    {{
        # Check SmallCity inconsistency
        ?city city:hasPopulation ?pop .
        ?city rdf:type city:SmallCity .
        BIND("SmallCity" as ?typeLabel)
        FILTER (?pop >= 100000) # Population is too large for SmallCity
    }}
}}
"""

# --- STORY_12: Adjacent City Symmetry Check ---
# Finds pairs where CityA is adjacentTo CityB, but the inverse is missing.
QUERY_ADJACENT_COMPLETION = f"""
{PREFIXES}
SELECT ?cityA ?cityB
WHERE {{
    ?cityA city:adjacentTo ?cityB .
    FILTER NOT EXISTS {{
        ?cityB city:adjacentTo ?cityA .
    }}
}}
"""

# --- STORY_13: Desert Climate Allowing Food ---
# Checks if a climate in a Desert zone has 'allowsForFood true' (contradiction).
QUERY_DESERT_CLIMATE_FOOD = f"""
{PREFIXES}
SELECT ?climate ?food # ?food variable might not bind if GenericFood isn't defined, but the pattern will still match
WHERE {{
    ?climate rdf:type travel:Climate . # Ensure it's a climate instance
    ?climate travel:hasClimateZone travel:Desert .
    # Check if it allows food growth (should be restricted by ontology axiom)
    ?climate travel:allowsForFood ?food . # ?food can be ia2025:GenericFood or any food
}}
"""

# --- STORY_14: Snow Above Zero Degrees ---
# Checks if a weather record reports Snow when the temperature is above 0.
QUERY_SNOW_ABOVE_ZERO = f"""
{PREFIXES}
SELECT ?record ?temp
WHERE {{
    ?record travel:weatherHasState travel:Snow .
    ?record travel:temperature ?temp .
    FILTER (?temp > 0)
}}
"""

# --- STORY_15: Travel Limit Violations ---
QUERY_WALKING_DISTANCE = f"""
{PREFIXES}
SELECT ?event ?dist
WHERE {{
    ?event travel:hasTravelMode travel:Walking .
    ?event travel:travelDistance ?dist .
    FILTER (?dist > 20) # Max walking distance is 20 km
}}
"""

QUERY_WALKING_SPEED = f"""
{PREFIXES}
SELECT ?event ?dist ?duration ?speed
WHERE {{
    ?event travel:hasTravelMode travel:Walking .
    ?event travel:travelDistance ?dist .
    ?event travel:travelDurationHours ?duration .
    FILTER (?duration > 0) # Avoid division by zero
    BIND ((?dist / ?duration) AS ?speed)
    FILTER (?speed > 6) # Max walking speed is 6 km/h
}}
"""

QUERY_WALKING_COST = f"""
{PREFIXES}
SELECT ?event ?cost
WHERE {{
    ?event travel:hasTravelMode travel:Walking .
    ?event travel:travelCost ?cost .
    FILTER (?cost > 0) # Walking cost must be 0
}}
"""

QUERY_CYCLING_DISTANCE = f"""
{PREFIXES}
SELECT ?event ?dist
WHERE {{
    ?event travel:hasTravelMode travel:Cycling .
    ?event travel:travelDistance ?dist .
    FILTER (?dist > 50) # Max cycling distance is 50 km
}}
"""

QUERY_CYCLING_SPEED = f"""
{PREFIXES}
SELECT ?event ?dist ?duration ?speed
WHERE {{
    ?event travel:hasTravelMode travel:Cycling .
    ?event travel:travelDistance ?dist .
    ?event travel:travelDurationHours ?duration .
    FILTER (?duration > 0) # Avoid division by zero
    BIND ((?dist / ?duration) AS ?speed)
    FILTER (?speed > 25) # Max cycling speed is 25 km/h
}}
"""

QUERY_CYCLING_COST = f"""
{PREFIXES}
SELECT ?event ?cost
WHERE {{
    ?event travel:hasTravelMode travel:Cycling .
    ?event travel:travelCost ?cost .
    FILTER (?cost > 0) # Cycling cost must be 0
}}
"""

# --- Final Dictionary of Queries ---
# Contains only the active, corrected queries.
ALL_QUERIES = {
    "allergy_violation": QUERY_ALLERGY,                     # STORY_1, STORY_6
    "drivable_city_obesity_missing": QUERY_DRIVABLE_CITY_OBESITY, # STORY_2 (needs livesIn)
    "underage_marriage": QUERY_UNDERAGE_MARRIAGE,           # STORY_3 (simplified + fix)
    "conflicting_traits": QUERY_CONFLICTING_TRAITS,         # STORY_4 (corrected names)
    "baker_missing_oven": QUERY_PERSON_AS_BAKER_MISSING_OVEN,           # STORY_5 (corrected logic)
    "disjoint_health_conditions": QUERY_DISJOINT_HEALTH_CONDITIONS_EXPLICIT_CHECK, # STORY_7
    "walkable_mountain_city": QUERY_WALKABLE_MOUNTAIN_CITY,   # STORY_8
    "landmark_multiple_cities": QUERY_LANDMARK_MULTIPLE_CITIES,# STORY_9
    "subway_no_city": QUERY_SUBWAY_NO_CITY,                 # STORY_10
    "city_size_population_mismatch": QUERY_CITY_SIZE_POPULATION_MISMATCH, # STORY_11 (corrected)
    "adjacent_to_completion": QUERY_ADJACENT_COMPLETION,      # STORY_12
    "desert_climate_food": QUERY_DESERT_CLIMATE_FOOD,         # STORY_13
    "snow_above_zero": QUERY_SNOW_ABOVE_ZERO,               # STORY_14
    # STORY_15 Queries:
    "walking_distance_violation": QUERY_WALKING_DISTANCE,
    "walking_speed_violation": QUERY_WALKING_SPEED,
    "walking_cost_violation": QUERY_WALKING_COST,
    "cycling_distance_violation": QUERY_CYCLING_DISTANCE,
    "cycling_speed_violation": QUERY_CYCLING_SPEED,
    "cycling_cost_violation": QUERY_CYCLING_COST,
}

# Print the number of queries loaded (for debugging)
print(f"Załadowano ontologię i {len(ALL_QUERIES)} zapytań sprawdzających.")