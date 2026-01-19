
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class PRResponse:
    content: str
    is_safe: bool
    warnings: List[str]

class SafePRAgent:
    """
    Day 92: Safe Public Relations Agent.
    Filters automated public communications for hallucinations, 
    offensive content, and reputational risk.
    """
    def __init__(self, brand_name: str):
        self.brand_name = brand_name
        # Prohibited topics/keywords (Simulated)
        self.prohibited = ["leaked", "confidential", "rumors", "scandal", "incompetent"]
        # Approved facts (Simulated knowledge base)
        self.fact_kb = {
            "launch_date": "Next Friday",
            "price": "$199",
            "feature": "AI Safety Core"
        }

    def _check_facts(self, text: str) -> List[str]:
        warnings = []
        # Detection of hallucinated prices or dates (Simplified)
        if "$" in text and self.fact_kb["price"] not in text:
            warnings.append(f"HALLUCINATION: Proposed price in text does not match official KB ({self.fact_kb['price']}).")
        return warnings

    def _check_tone(self, text: str) -> List[str]:
        warnings = []
        for word in self.prohibited:
            if word in text.lower():
                warnings.append(f"REPUTATIONAL RISK: Prohibited keyword '{word}' detected.")
        if "!" in text and text.count("!") > 3:
            warnings.append("TONE WARNING: Excessive use of exclamation marks (unprofessional).")
        return warnings

    def generate_release(self, input_topic: str, draft_text: str) -> PRResponse:
        warnings = []
        # 1. Fact Check
        warnings.extend(self._check_facts(draft_text))
        # 2. Tone Check
        warnings.extend(self._check_tone(draft_text))
        
        is_safe = len(warnings) == 0
        
        return PRResponse(
            content=draft_text if is_safe else "[REDACTED: SAFETY VIOLATION]",
            is_safe=is_safe,
            warnings=warnings
        )
