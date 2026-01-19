
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DesignReview:
    is_valid: bool
    weaknesses: List[str]
    score: float # 0.0 to 1.0

class ExperimentValidator:
    """
    Day 78: Experiment Design Validator.
    Checks scientific research designs for common structural flaws 
    such as bias, lack of controls, or small sample sizes.
    """
    def __init__(self):
        self.red_flag_patterns = {
            "no control": "No control group specified in the design.",
            "not randomized": "Lack of randomization detected.",
            "self-selected": "Selection bias likely from self-selected participants.",
            "low sample": "Sample size mentioned is likely insufficient for statistical power.",
            "blind": "Design does not mention blinding or double-blinding."
        }

    def _analyze_text(self, design_text: str) -> List[str]:
        weaknesses = []
        text = design_text.lower()
        
        # 1. Missing Control Group
        if "control group" not in text and "baseline" not in text:
            weaknesses.append(self.red_flag_patterns["no control"])
            
        # 2. Randomization Check
        if "random" not in text:
            weaknesses.append(self.red_flag_patterns["not randomized"])
            
        # 3. Selection Bias
        if "volunteer" in text or "self-selected" in text:
            weaknesses.append(self.red_flag_patterns["self-selected"])
            
        # 4. Blinding
        if "blind" not in text:
            weaknesses.append(self.red_flag_patterns["blind"])
            
        # 5. Sample Size (Heuristic)
        # Check for numbers < 30 followed by units
        import re
        small_n = re.search(r'\bn\s*=\s*([1-2]?[0-9])\b', text)
        if small_n:
            weaknesses.append(f"{self.red_flag_patterns['low sample']} (n={small_n.group(1)})")
            
        return weaknesses

    def validate_design(self, design_text: str) -> DesignReview:
        weaknesses = self._analyze_text(design_text)
        
        # Calculate score
        max_flaws = len(self.red_flag_patterns)
        score = max(0.0, 1.0 - (len(weaknesses) / max_flaws))
        
        return DesignReview(
            is_valid=(len(weaknesses) <= 1), # Allow at most 1 minor flaw
            weaknesses=weaknesses,
            score=score
        )
