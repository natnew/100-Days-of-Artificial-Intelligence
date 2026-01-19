
from typing import List
import math

class ConceptVector:
    """
    Mock Concept Activation Vector.
    Represents a high-level concept (e.g., 'Politeness') as a vector direction.
    """
    def __init__(self, name: str, vector: List[float]):
        self.name = name
        self.vector = vector

    def measure_sensitivity(self, input_embedding: List[float]) -> float:
        """
        Calculates similarity (dot product) to see if the input 'activates' this concept.
        """
        if len(input_embedding) != len(self.vector):
            return 0.0
            
        dot_product = sum(a*b for a,b in zip(input_embedding, self.vector))
        return dot_product

class CAProbe:
    def __init__(self):
        # Mock embeddings for demonstration
        # 2D space: x=Politeness, y=Aggression
        self.concepts = {
            "Politeness": ConceptVector("Politeness", [1.0, 0.0]),
            "Aggression": ConceptVector("Aggression", [0.0, 1.0])
        }

    def get_embedding(self, text: str) -> List[float]:
        """
        Mock embedding generator.
        """
        text = text.lower()
        if "please" in text or "kindly" in text:
            return [0.9, 0.1]
        if "hate" in text or "stupid" in text:
            return [0.1, 0.9]
        return [0.5, 0.5]

    def analyze(self, text: str) -> dict:
        emb = self.get_embedding(text)
        results = {}
        for name, concept in self.concepts.items():
            activation = concept.measure_sensitivity(emb)
            results[name] = activation
        return results
