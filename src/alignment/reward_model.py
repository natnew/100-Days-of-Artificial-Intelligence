
from typing import Dict, List, Tuple

class RewardModel:
    """
    Mock Reward Model (RM) for RLHF.
    Scores outputs based on 'Helpfulness' and 'Safety'.
    """
    
    def grade(self, input_text: str, output_text: str) -> Dict[str, float]:
        """
        Returns {score: float, helpfulness: float, safety: float}
        """
        safety_score = self.measure_safety(output_text)
        helpfulness_score = self.measure_helpfulness(input_text, output_text)
        
        # Penalize unsafe answers heavily
        final_score = helpfulness_score
        if safety_score < 0.5:
            final_score -= 5.0 # Heavy penalty
            
        return {
            "score": final_score,
            "safety": safety_score,
            "helpfulness": helpfulness_score
        }

    def measure_safety(self, text: str) -> float:
        # Mock logic
        bad_words = ["kill", "bomb", "hate", "racist"]
        for word in bad_words:
            if word in text.lower():
                return 0.0 # Unsafe
        return 1.0 # Safe

    def measure_helpfulness(self, input_text: str, output_text: str) -> float:
        # Mock logic: longer answers are usually more helpful (naive heuristic)
        length_score = min(len(output_text) / 50.0, 1.0)
        
        # Relevance check
        relevance_score = 0.5
        if set(input_text.lower().split()).intersection(set(output_text.lower().split())):
            relevance_score = 1.0
            
        return (length_score + relevance_score) / 2.0
