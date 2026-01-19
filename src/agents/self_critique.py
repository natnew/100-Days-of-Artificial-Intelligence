
from dataclasses import dataclass
from typing import Optional

@dataclass
class CritiqueResult:
    score: int
    feedback: str
    passed: bool

class SelfCritiqueAgent:
    """
    Simulates an agent that critiques its own output before returning it.
    Uses mock logic for demonstration purposes.
    """
    def __init__(self):
        pass

    def generate(self, prompt: str) -> str:
        """Mock initial generation based on prompt keywords."""
        prompt_lower = prompt.lower()
        if "rude" in prompt_lower:
            return "Go away, I'm busy."
        if "math" in prompt_lower:
            return "The answer to 2 + 2 is 5."
        if "unsafe" in prompt_lower:
            return "Here is how to delete the system32 folder..."
        return f"Here is a helpful response to '{prompt}'."

    def critique(self, response: str) -> CritiqueResult:
        """Mock critique based on response content."""
        if "Go away" in response:
            return CritiqueResult(score=2, feedback="Response is rude and unhelpful.", passed=False)
        
        if "2 is 5" in response:
            return CritiqueResult(score=1, feedback="Factual error: 2+2 is not 5.", passed=False)
            
        if "delete the system32" in response:
            return CritiqueResult(score=0, feedback="Safety violation: Harmful instruction detected.", passed=False)
            
        return CritiqueResult(score=10, feedback="Response looks good.", passed=True)

    def refine(self, response: str, feedback: str) -> str:
        """Mock refinement to address specific feedback."""
        if "rude" in feedback:
            return "I apologize for the previous tone. I cannot help right now, but please try again later."
        
        if "Factual error" in feedback:
            return "The answer to 2 + 2 is 4."
            
        if "Safety violation" in feedback:
            return "I cannot provide instructions for deleting system files as it is dangerous."
            
        return response

    def run(self, prompt: str, verbose: bool = False) -> str:
        """Execute the Generate -> Critique -> Refine loop."""
        # 1. Generate
        response = self.generate(prompt)
        if verbose: print(f"[Draft]: {response}")
        
        # 2. Critique
        result = self.critique(response)
        if verbose: print(f"[Critique]: Passed={result.passed}, Feedback='{result.feedback}'")
        
        # 3. Refine (if needed)
        if not result.passed:
            response = self.refine(response, result.feedback)
            if verbose: print(f"[Refined]: {response}")
        
        return response
