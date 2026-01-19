
from typing import List, Callable, Any, Dict
import copy

class CounterfactualProbe:
    """
    Tests agent robustness by slightly modifying inputs (perturbations)
    and checking if the output remains consistent or changes unexpectedly.
    """
    
    def __init__(self, agent_func: Callable[[str], str]):
        self.agent_func = agent_func

    def generate_perturbations(self, text: str) -> List[str]:
        """
        Simple rule-based perturbations.
        """
        variations = []
        
        # 1. Gender Swap
        if "he" in text.lower():
            variations.append(text.replace("he", "she").replace("He", "She"))
        if "man" in text.lower():
            variations.append(text.replace("man", "woman").replace("Man", "Woman"))
            
        # 2. Tone Swap (Aggressive -> Polite)
        if "kill" in text.lower():
            variations.append(text.replace("kill", "terminate"))
        
        # 3. Noise injection
        variations.append(text + " ") # Trailing space check
        
        return variations

    def run_probe(self, original_input: str) -> Dict[str, Any]:
        """
        Runs the agent on original and perturbed inputs.
        Returns a report on consistency.
        """
        original_output = self.agent_func(original_input)
        perturbations = self.generate_perturbations(original_input)
        
        results = []
        for p in perturbations:
            output = self.agent_func(p)
            changed = (output != original_output)
            results.append({
                "input": p,
                "output": output,
                "changed": changed
            })
            
        return {
            "original_input": original_input,
            "original_output": original_output,
            "perturbations": results,
            "is_robust": not any(r['changed'] for r in results) # Simplistic definition of robustness
        }
