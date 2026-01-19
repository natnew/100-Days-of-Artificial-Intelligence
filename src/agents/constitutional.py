from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ConstitutionalPrinciple:
    name: str
    description: str

class ConstitutionalAgent:
    """
    An agent that uses Constitutional AI (CAI) to self-correct its outputs.
    It generates an initial response, critiques it against a set of principles,
    and revises it if necessary.
    """
    def __init__(self, base_model):
        self.model = base_model

    def generate(self, prompt: str, principles: List[ConstitutionalPrinciple]) -> Dict:
        """
        Generates a response, critiques it, and revisions it.
        Returns the final response and the trace of the process.
        """
        trace = []
        
        # 1. Initial Response
        initial_response = self.model.generate(prompt)
        current_response = initial_response
        trace.append({"step": "initial", "content": initial_response})

        # 2. Critique and Revise Loop
        for principle in principles:
            # Critique
            critique_prompt = (
                f"Critique the following response based on this principle: {principle.description}\n"
                f"Response: {current_response}\n"
                f"If there is no violation, say 'No violation'."
            )
            critique = self.model.generate(critique_prompt)
            trace.append({"step": "critique", "principle": principle.name, "content": critique})

            # If violation detected (heuristic: if critique is long or doesn't say "No violation")
            # For this mock, let's assume if the critique contains "violation" or "harmful" it's a hit.
            if "violation" in critique.lower() and "no violation" not in critique.lower():
                # Revise
                revision_prompt = (
                    f"Rewrite the response to address the following critique: {critique}\n"
                    f"Original Response: {current_response}"
                )
                revision = self.model.generate(revision_prompt)
                current_response = revision
                trace.append({"step": "revision", "principle": principle.name, "content": revision})
            else:
                trace.append({"step": "revision_skipped", "principle": principle.name})

        return {
            "final_response": current_response,
            "trace": trace
        }
