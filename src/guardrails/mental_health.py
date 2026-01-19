
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SafetyResponse:
    triggered: bool
    category: Optional[str]
    message: str
    action: str # CONTINUE, REFUSE, ESCALATE

class MentalHealthSafeguard:
    """
    Day 84: Mental Health Support Boundaries.
    Detects crisis indicators and enforces professional scope 
    for AI-based support tools.
    """
    def __init__(self):
        # High-risk crisis indicators
        self.crisis_keywords = [
            r"\bkill myself\b", r"\bsuicide\b", r"\bend (?:my )?life\b",
            r"\bhurt (?:myself|someone)\b", r"\bend(?:ing)? it all\b", r"\bdone with life\b"
        ]
        
        # Medical advice boundaries
        self.medical_terms = [
            r"\bdiagnose me\b", r"\bwhat medicine\b", r"\bprescribe\b",
            r"\bdosage\b", r"\bsetraline\b", r"\bprozac\b", r"\bxanax\b"
        ]

        self.esc_message = (
            "I'm sorry you're feeling this way, but I'm an AI, not a professional. "
            "Please contact the National Suicide Prevention Lifeline at 988 (USA) "
            "or your local emergency services immediately."
        )
        
        self.refusal_message = (
            "I cannot provide medical diagnoses or prescribe medications. "
            "Please consult with a licensed psychiatrist or physician for this information."
        )

    def analyze_input(self, user_input: str) -> SafetyResponse:
        text = user_input.lower()
        
        # 1. Crisis Detection
        for pattern in self.crisis_keywords:
            if re.search(pattern, text):
                return SafetyResponse(True, "CRISIS", self.esc_message, "ESCALATE")
                
        # 2. Medical Advice Boundary
        for pattern in self.medical_terms:
            if re.search(pattern, text):
                return SafetyResponse(True, "MEDICAL_ADVICE", self.refusal_message, "REFUSE")
                
        # 3. Safe to continue
        return SafetyResponse(False, None, "Prompt appears safe within boundaries.", "CONTINUE")

    def wrap_persona(self, persona_prompt: str) -> str:
        """Adds scope constraints to the system prompt."""
        boundary = (
            "\n\nSCOPE LIMIT: You are an AI peer support tool. "
            "You CANNOT diagnose, prescribe, or handle crises. "
            "If a user mentions self-harm, immediately stop and provide hotline info."
        )
        return persona_prompt + boundary
