from typing import List, Tuple, Any

from owlrl import DeductiveClosure, RDFS_Semantics
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, OWL

from queries import ALL_QUERIES


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
        print(f"Loaded ontology and {len(self.queries)} queries.")

    def check_consistency(self, extracted_facts: List[Tuple[str, str, Any]]) -> List[str]:
        temp_graph = Graph()
        temp_graph += self.base_graph

        self._add_facts_to_graph(temp_graph, extracted_facts)

        print("Start of reasoner")
        DeductiveClosure(RDFS_Semantics).expand(temp_graph)
        print("Stop reasoning.")

        violations = []
        print(f"Run {len(self.queries)} queries")
        for query_name, query_string in self.queries.items():
            try:
                results = temp_graph.query(query_string)

                if len(results) > 0:
                    for row in results:
                        violation_message = f"Problem: '{query_name}': {', '.join(map(str, row))}"
                        violations.append(violation_message)
            except Exception as e:
                print(f"Error during query: '{query_name}': {e}")

        if not violations:
            print("Not found any violations.")
        else:
            print(f"Found {len(violations)} violations.")
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
                print(f"Skipped wrong facts ({s_str}, {p_str}, {o_val}): {e}")

    def _resolve_uri(self, uri_str: str) -> URIRef:
        if uri_str.startswith("http"):
            return URIRef(uri_str)

        try:
            prefix, name = uri_str.split(":", 1)
            if prefix in self.namespaces:
                return self.namespaces[prefix][name]
            else:
                raise ValueError(f"Not known prefix: '{prefix}' in '{uri_str}'")
        except ValueError:
            raise ValueError(f"Bad format of URI: '{uri_str}'. Expected 'prefix:name'.")
