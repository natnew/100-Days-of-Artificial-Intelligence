
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class Principle:
    id: str
    description: str

class ConstitutionalAI:
    """
    Day 97: Constitutional AI (RLAIF).
    Uses a predefined 'Constitution' (set of principles) to 
    evaluate and rank AI responses.
    """
    def __init__(self, principles: List[Principle]):
        self.constitution = principles

    def evaluate_response(self, response: str) -> Dict[str, Any]:
        """
        Evaluates a single response against all principles.
        """
        violations = []
        score = 1.0
        
        for p in self.constitution:
            # Simulated principle checks
            if p.id == "HELPFUL" and len(response) < 10:
                violations.append(f"Violates {p.id}: {p.description}")
                score -= 0.3
            elif p.id == "HARMLESS" and "harmful" in response.lower():
                violations.append(f"Violates {p.id}: {p.description}")
                score -= 0.7
            elif p.id == "HONEST" and "trust me" in response.lower():
                violations.append(f"Violates {p.id}: {p.description}")
                score -= 0.2
        
        return {
            "score": max(0.0, score),
            "violations": violations
        }

    def select_best_response(self, candidates: List[str]) -> Tuple[str, float]:
        """
        Selects the candidate with the highest constitutional score.
        """
        best_resp = ""
        best_score = -1.0
        
        for cand in candidates:
            eval_res = self.evaluate_response(cand)
            if eval_res["score"] > best_score:
                best_score = eval_res["score"]
                best_resp = cand
                
        return best_resp, best_score

    def generate_preference_data(self, response_pairs: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """
        Generates data for RLAIF training by preferring the response 
        with the higher constitutional score.
        """
        pref_data = []
        for r1, r2 in response_pairs:
            s1 = self.evaluate_response(r1)["score"]
            s2 = self.evaluate_response(r2)["score"]
            
            chosen, rejected = (r1, r2) if s1 >= s2 else (r2, r1)
            pref_data.append({
                "chosen": chosen,
                "rejected": rejected,
                "score_diff": abs(s1 - s2)
            })
        return pref_data
