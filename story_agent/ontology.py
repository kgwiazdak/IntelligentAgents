"""Ontology tools for the storytelling agent."""

from __future__ import annotations

import os
from typing import List, Optional

from owlready2 import get_ontology, sync_reasoner


class OntologyChecker:
    """Loads an ontology and provides consistency checks for stories."""

    def __init__(self, ontology_path: str) -> None:
        """Load the ontology and prepare commonly used classes and properties."""
        print("Initializing OntologyChecker...")
        self.onto = None
        try:
            self.onto = get_ontology(
                f"file://{os.path.abspath(ontology_path)}"
            ).load()
            print("Ontology loaded successfully.")

            sync_reasoner()
            print("Reasoner synchronized.")

            self.Person = self.onto.search_one(iri="*Person")
            self.AdultPerson = self.onto.search_one(iri="*AdultPerson")
            self.age_prop = self.onto.search_one(iri="*age")
            self.isAllergicTo_prop = self.onto.search_one(iri="*isAllergicTo")
            self.eats_prop = self.onto.search_one(iri="*eats")
            self.isPartOf_prop = self.onto.search_one(iri="*isPartOf")
            self.WalkableCity = self.onto.search_one(iri="*WalkableCity")
            self.Food = self.onto.search_one(iri="*Food")

            print("Key ontology classes and properties located.")

        except Exception as exc:  # pragma: no cover - defensive logging
            print("--- CRITICAL ERROR ---")
            print(f"Failed to initialize OntologyChecker: {exc}")
            print("Please ensure the following:")
            print("1. The ontology file 'final_version3.rdf' is in the same directory and has been corrected.")
            print("2. You have a Java Development Kit (JDK) installed and accessible.")
            print("3. The 'owlready2' library is correctly installed.")
            print("----------------------")
            self.onto = None

    def _ensure_ontology_loaded(self) -> Optional[str]:
        if not self.onto:
            return "Ontology not loaded."
        return None

    def check_marriage_age(self, person_name: str, age: int) -> Optional[str]:
        """Check if a person meets the ontology's minimum marriage age."""
        error = self._ensure_ontology_loaded()
        if error:
            return error

        print(f"  [Check] Marriage age for {person_name} (age {age})...")
        if age < 18:
            return (
                f"Inconsistency found: Marriage participant '{person_name}' is {age}, "
                "but must be 18 or older to be married according to ontology rules."
            )
        return None

    def check_allergy(
        self,
        person_name: str,
        person_allergies: List[str],
        food_eaten: str,
    ) -> Optional[str]:
        """Check if the story feeds someone food that conflicts with known allergies."""
        error = self._ensure_ontology_loaded()
        if error:
            return error

        print(
            f"  [Check] Allergy for {person_name} eating {food_eaten} "
            f"(allergies: {person_allergies})..."
        )

        food_iri_fragment = f"*{food_eaten.replace(' ', '')}"
        food_individual = self.onto.search_one(iri=food_iri_fragment, is_a=self.Food)

        if not food_individual:
            print(f"    - Warning: Food '{food_eaten}' not found in ontology. Skipping check.")
            return None

        for allergen_name in person_allergies:
            allergen_individual = self.onto.search_one(iri=f"*{allergen_name.replace(' ', '')}")
            if not allergen_individual:
                continue

            if (
                self.isPartOf_prop in allergen_individual.get_relations()
                and food_individual in allergen_individual.isPartOf
            ):
                return (
                    f"Inconsistency found: '{person_name}' is eating '{food_eaten}', "
                    f"which contains '{allergen_name}', an ingredient they are allergic to."
                )
        return None

    def check_city_terrain(self, city_name: str, observed_terrain: str) -> Optional[str]:
        """Check if terrain descriptions align with ontology definitions for a city."""
        error = self._ensure_ontology_loaded()
        if error:
            return error

        print(f"  [Check] City terrain for {city_name} (observed: {observed_terrain})...")

        city_iri_fragment = f"*{city_name.replace(' ', '')}"
        city_individual = self.onto.search_one(iri=city_iri_fragment)

        if not city_individual:
            print(f"    - Warning: City '{city_name}' not found in ontology. Skipping check.")
            return None

        if (
            observed_terrain.lower() == "mountains"
            and self.WalkableCity in city_individual.is_a
        ):
            return (
                f"Inconsistency found: The story mentions 'mountains' in '{city_name}', "
                "but the ontology defines it as a 'WalkableCity' which must have flat terrain."
            )
        return None
