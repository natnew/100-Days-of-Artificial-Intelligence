
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ValidationResult:
    is_valid: bool
    risk_level: str # "LOW", "MEDIUM", "HIGH"
    clarifying_questions: List[str] = field(default_factory=list)
    reason: str = ""

class GoalValidator:
    """
    Validates user goals for ambiguity and safety risks.
    In a real system, this would call an LLM.
    Here, we use keyword heuristics for demonstration.
    """
    def __init__(self):
        # Heuristics for demo purposes
        self.risky_keywords = ["delete", "remove", "destroy", "format", "kill", "wipe"]
        self.ambiguous_keywords = ["stuff", "things", "files", "data", "fix", "clean"]
        
    def validate(self, goal: str) -> ValidationResult:
        goal_lower = goal.lower()
        
        # 1. Check High Risk
        for word in self.risky_keywords:
            if word in goal_lower:
                return ValidationResult(
                    is_valid=False,
                    risk_level="HIGH",
                    reason=f"Goal contains risky action '{word}'.",
                    clarifying_questions=[f"What specific items do you want to {word}?", "Do you have a backup?"]
                )
                
        # 2. Check Ambiguity
        for word in self.ambiguous_keywords:
            if word in goal_lower:
                # Check if it's too generic like "delete files" (already caught by risky) 
                # or just "organize files" (ambiguous)
                return ValidationResult(
                    is_valid=False,
                    risk_level="MEDIUM",
                    reason=f"Goal is ambiguous due to vague term '{word}'.",
                    clarifying_questions=[f"Which specific {word} are you referring to?", "What is the criteria?"]
                )
        
        # 3. Default Safe
        return ValidationResult(
            is_valid=True,
            risk_level="LOW",
            reason="Goal appears specific and safe."
        )
