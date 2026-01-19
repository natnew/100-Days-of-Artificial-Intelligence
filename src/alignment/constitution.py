
from typing import List, Dict

class Constitution:
    def __init__(self, principles: List[str]):
        self.principles = principles

class ConstitutionalAgent:
    """
    Critiques and Revisions based on a set of principles.
    """
    def __init__(self, constitution: Constitution):
        self.constitution = constitution

    def respond(self, prompt: str) -> str:
        # 1. Draft
        draft = self.generate_draft(prompt)
        print(f"[Draft]: {draft}")
        
        # 2. Critique
        critique = self.critique(draft)
        print(f"[Critique]: {critique}")
        
        # 3. Revise (if needed)
        if critique:
            final = self.revise(draft, critique)
            print(f"[Revision]: {final}")
            return final
            
        return draft

    def generate_draft(self, prompt: str) -> str:
        # Mock logic
        if "steal" in prompt:
            return "Sure, here is how you remove the tag..."
        return "I can help with that."

    def critique(self, draft: str) -> str:
        # Check against principles
        violations = []
        for principle in self.constitution.principles:
            if "illegal" in principle and "remove the tag" in draft:
                violations.append("Violates legality: promotes theft.")
        
        if violations:
            return "; ".join(violations)
        return ""

    def revise(self, draft: str, critique: str) -> str:
        # Mock revision logic
        if "legality" in critique:
            return "I cannot assist with theft or illegal activities."
        return draft
