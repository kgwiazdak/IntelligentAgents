from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, OWL
from owlrl import DeductiveClosure, RDFS_Semantics
from typing import List, Tuple, Any

from src.queries import ALL_QUERIES


class OntologyChecker:
    def __init__(self, ontology_path: str):
        self.namespaces = {
            "demo": Namespace("http://www.semanticweb.org/alexandrosxanthopoulos/ontologies/2025/9/ProjectDemo#"),
            "ia2025": Namespace("http://example.org/ia2025#"),
            "city": Namespace("http://www.semanticweb.org/gwiazdk01/ontologies/2025/8/untitled-ontology-4#"),
            "travel": Namespace("http://www.semanticweb.org/rubyorsmth/ontologies/2025/9/untitled-ontology-5#"),
            "base": Namespace("http://www.semanticweb.org/user/ontologies/2025/9/untitled-ontology-24#"),
            "rdf": RDF,
            "rdfs": RDFS,
            "owl": OWL,
            "xsd": XSD
        }

        self.base_graph = Graph()
        self.base_graph.parse(ontology_path, format="xml")

        for prefix, namespace in self.namespaces.items():
            self.base_graph.bind(prefix, namespace)

        self.queries = ALL_QUERIES
        print(f"Załadowano ontologię i {len(self.queries)} zapytań sprawdzających.")

    def check_consistency(self, extracted_facts: List[Tuple[str, str, Any]]) -> List[str]:
        temp_graph = Graph()
        temp_graph += self.base_graph

        self._add_facts_to_graph(temp_graph, extracted_facts)

        print("Uruchamianie reasonera...")
        DeductiveClosure(RDFS_Semantics).expand(temp_graph)
        print("Zakończono wnioskowanie.")

        violations = []
        print(f"Uruchamianie {len(self.queries)} zapytań sprawdzających...")
        for query_name, query_string in self.queries.items():
            try:
                results = temp_graph.query(query_string)

                if len(results) > 0:
                    for row in results:
                        violation_message = f"Naruszenie reguły '{query_name}': {', '.join(map(str, row))}"
                        violations.append(violation_message)
            except Exception as e:
                print(f"BŁĄD podczas wykonywania zapytania '{query_name}': {e}")

        if not violations:
            print("Nie znaleziono żadnych naruszeń spójności.")
        else:
            print(f"Znaleziono {len(violations)} naruszeń.")

        return violations

    def _add_facts_to_graph(self, g: Graph, facts: List[Tuple[str, str, Any]]):
        for s_str, p_str, o_val in facts:
            try:
                s_node = self._resolve_uri(s_str)
                p_node = self._resolve_uri(p_str)

                if isinstance(o_val, str) and ":" in o_val and not o_val.startswith("http"):
                    o_node = self._resolve_uri(o_val)
                else:
                    o_node = Literal(o_val)

                g.add((s_node, p_node, o_node))

            except Exception as e:
                print(f"Pominięto nieprawidłowy fakt ({s_str}, {p_str}, {o_val}): {e}")

    def _resolve_uri(self, uri_str: str) -> URIRef:
        if uri_str.startswith("http"):
            return URIRef(uri_str)

        try:
            prefix, name = uri_str.split(":", 1)
            if prefix in self.namespaces:
                return self.namespaces[prefix][name]
            else:
                raise ValueError(f"Nieznany prefix: '{prefix}' w '{uri_str}'")
        except ValueError:
            raise ValueError(f"Nieprawidłowy format URI: '{uri_str}'. Oczekiwano 'prefix:nazwa'.")


if __name__ == "__main__":
    print("--- Testowanie OntologyChecker ---")

    checker = OntologyChecker("./src/final_version4.rdf")

    test_facts_story_3 = [
        ("demo:Alice", "rdf:type", "demo:Person"),
        ("demo:Alice", "demo:age", 17),
        ("demo:Bob", "rdf:type", "demo:Person"),
        ("demo:Bob", "demo:age", 19),
        ("demo:Alice", "demo:isMarriedTo", "demo:Bob")
    ]

    print("\n--- Sprawdzanie Scenariusza 3 (Małżeństwo nieletniej) ---")
    violations_3 = checker.check_consistency(test_facts_story_3)
    for v in violations_3:
        print(f"WYKRYTO: {v}")

    test_facts_story_8 = [
        ("city:Hillsburg", "rdf:type", "city:WalkableCity"),
        ("city:Hillsburg", "city:hasTerrain", "city:Mountainous")
    ]

    print("\n--- Sprawdzanie Scenariusza 8 (Górzyste miasto dla pieszych) ---")
    violations_8 = checker.check_consistency(test_facts_story_8)
    for v in violations_8:
        print(f"WYKRYTO: {v}")