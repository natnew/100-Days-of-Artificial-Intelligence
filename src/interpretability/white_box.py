
from dataclasses import dataclass
from typing import Dict, Any, List
import sys
import os

from src.interpretability.tracer import Tracer
from src.interpretability.attention import SimpleAttention
from src.interpretability.counterfactual import CounterfactualProbe
from src.interpretability.cav import CAProbe

@dataclass
class Explanation:
    trace: List[Dict[str, Any]]
    attributions: List[tuple]
    concepts: Dict[str, float]
    # robustness: bool # Optional

class WhiteBoxAgent:
    """
    An agent that provides a full 'Safety Explanation' alongside its answer.
    """
    def __init__(self):
        self.tracer = Tracer()
        self.attention = SimpleAttention()
        self.cav = CAProbe()
        
    def run(self, input_text: str) -> Dict[str, Any]:
        self.tracer.clear()
        self.tracer.log("input", input_text)
        
        # 1. Internal Logic (Mock)
        thought = "Analyzing request..."
        self.tracer.log("thought", thought)
        
        output_text = "Processing " + input_text # Simple echo logic
        
        # 2. Generate Explanations
        # A. Feature Attribution
        attrs = self.attention.calculate_attribution(input_text, output_text)
        
        # B. Concept Activation
        concepts = self.cav.analyze(input_text)
        
        self.tracer.log("output", output_text)
        
        return {
            "result": output_text,
            "explanation": Explanation(
                trace=self.tracer.get_trace(),
                attributions=attrs,
                concepts=concepts
            )
        }
