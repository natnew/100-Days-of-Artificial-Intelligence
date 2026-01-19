
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class EvalFeedback:
    score: float # 0.0 to 1.0
    critique: str
    suggested_revision: str

class RecursiveRewardManager:
    """
    Day 96: Recursive Reward Modeling.
    Simulates using an AI 'Evaluator' to provide feedback on an 
    AI 'Worker', scaling alignment for complex tasks.
    """
    def __init__(self, target_alignment_goal: str):
        self.goal = target_alignment_goal

    def critique_output(self, worker_output: str) -> EvalFeedback:
        """Simulates an AI evaluator critiquing a worker's draft."""
        score = 1.0
        critique = "The output is excellent and fully aligned."
        revision = worker_output
        
        # Simple heuristic critique for demonstration
        if "harmful" in worker_output.lower():
            score = 0.2
            critique = f"The output contains concepts that violate the goal: {self.goal}."
            revision = worker_output.replace("harmful", "[SAFE_CONTENT]")
            
        elif len(worker_output) <= 20:
            score = 0.5
            critique = "The output is too brief and lacks depth."
            revision = worker_output + " (Extended for alignment compliance)"
            
        return EvalFeedback(score, critique, revision)

    def recursive_improvement(self, initial_draft: str, iterations: int = 2) -> List[EvalFeedback]:
        """
        Simulates multiple rounds of Critique -> Revise.
        """
        history = []
        current_draft = initial_draft
        
        for _ in range(iterations):
            feedback = self.critique_output(current_draft)
            history.append(feedback)
            current_draft = feedback.suggested_revision
            
        return history
