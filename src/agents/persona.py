
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Persona:
    name: str
    role: str
    tone: List[str]
    constraints: List[str]

    def get_system_prompt(self) -> str:
        return (
            f"You are {self.name}, a {self.role}. "
            f"Your tone must be {', '.join(self.tone)}. "
            f"You must strictly follow these constraints: {'; '.join(self.constraints)}."
        )

class PersonaManager:
    """
    Manages agent persona consistency and detects drift.
    """
    def __init__(self, persona: Persona):
        self.persona = persona

    def wrap_prompt(self, user_prompt: str) -> str:
        """Prepends the system prompt to the user's prompt."""
        return f"[System]\n{self.persona.get_system_prompt()}\n\n[User]\n{user_prompt}"

    def check_consistency(self, response: str) -> bool:
        """
        Mock logic to check if response matches persona.
        In a real system, this would use an LLM or classifier.
        """
        # Medical Assistant Constraints
        if self.persona.role == "Medical Assistant":
            if "dude" in response.lower() or "bro" in response.lower():
                return False # Tone violation
            if "idk" in response.lower():
                return False # Professionalism violation
        
        return True
