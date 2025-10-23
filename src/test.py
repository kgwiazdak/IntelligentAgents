# test_query_7.py

import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, OWL
from owlrl import DeductiveClosure, RDFS_Semantics

# Adjust the import path based on your project structure
try:
    # Assuming queries.py is inside an 'src' folder relative to this script
    from src.queries import PREFIXES, QUERY_DISJOINT_HEALTH_CONDITIONS_EXPLICIT_CHECK
except ImportError:
    print("BŁĄD: Nie można zaimportować zapytania. Sprawdź ścieżkę do src/queries.py")
    exit()

# Define Namespaces (must match ontology and query)
DEMO = Namespace("http://www.semanticweb.org/alexandrosxanthopoulos/ontologies/2025/9/ProjectDemo#")
BASE = Namespace("http://www.semanticweb.org/user/ontologies/2025/9/untitled-ontology-24#") # Added BASE for Anemia/Cancer

# --- Test Data Setup ---
ontology_file = "./final_version5.rdf"
query_to_test = QUERY_DISJOINT_HEALTH_CONDITIONS_EXPLICIT_CHECK

# Hardcoded triples representing STORY_7
story_7_triples = [
    (URIRef(DEMO + "Maya"), RDF.type, URIRef(DEMO + "Person")),
    (URIRef(DEMO + "Maya"), URIRef(DEMO + "hasCondition"), URIRef(BASE + "Anemia")), # Use BASE prefix based on ontology
    (URIRef(DEMO + "Maya"), URIRef(DEMO + "hasCondition"), URIRef(BASE + "Cancer"))  # Use BASE prefix based on ontology
]

# --- Test Execution ---
print(f"Ładowanie ontologii: {ontology_file}")
g = Graph()
try:
    g.parse(ontology_file, format="xml")
    print(f"Ontologia załadowana ({len(g)} trójek).")
except Exception as e:
    print(f"BŁĄD: Nie udało się załadować ontologii: {e}")
    exit()

print("\nDodawanie zahardcodowanych trójek dla STORY_7:")
for triple in story_7_triples:
    g.add(triple)
    print(f"  Dodano: {triple}")

print(f"\nCałkowita liczba trójek przed wnioskowaniem: {len(g)}")

print("\nUruchamianie reasonera (owlrl)...")
try:
    # Use RDFS reasoning plus some OWL rules needed for disjointness
    # You might experiment with OWLRL_Semantics if RDFS is insufficient,
    # but it can be much slower. RDFS_Semantics should handle disjointWith.
    DeductiveClosure(RDFS_Semantics).expand(g)
    print(f"Wnioskowanie zakończone. Całkowita liczba trójek po wnioskowaniu: {len(g)}")
except Exception as e:
    print(f"BŁĄD podczas wnioskowania: {e}")
    exit()

print(f"\nWykonywanie zapytania QUERY_DISJOINT_HEALTH_CONDITIONS_EXPLICIT_CHECK:")
print("-" * 40)
print(query_to_test)
print("-" * 40)

try:
    results = g.query(query_to_test)
    print(f"\nWyniki zapytania ({len(results)}):")
    if len(results) == 0:
        print(">>> ŻADNE naruszenia nie zostały znalezione.")
    else:
        print(">>> ZNALEZIONO NARUSZENIA:")
        for row in results:
            # Assuming the query returns person, condition1, condition2
            print(f"  - Osoba: {row.person}, Warunki: {row.conditionClass1}, {row.conditionClass2}")

except Exception as e:
    print(f"\nBŁĄD podczas wykonywania zapytania SPARQL: {e}")