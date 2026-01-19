
import numpy as np
from typing import List, Tuple, Dict, Any

class SafetyTuner:
    """
    Simulates Safety Fine-Tuning (like RLHF or DPO) using a preference-based approach.
    """
    def __init__(self, base_refusal_rate: float = 0.1):
        self.refusal_rate = base_refusal_rate

    def calculate_loss(self, chosen_scores: np.ndarray, rejected_scores: np.ndarray) -> float:
        """
        Simulates a contrastive loss (like DPO).
        If the 'chosen' (safe) response has much higher probability than 'rejected' (unsafe),
        the loss is low.
        """
        # Loss = -log(sigmoid(chosen - rejected))
        diff = chosen_scores - rejected_scores
        loss = -np.mean(np.log(1 / (1 + np.exp(-diff)) + 1e-10))
        return float(loss)

    def train_step(self, dataset: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Simulates a training iteration.
        Dataset expected to have 'prompt', 'safe_response', 'unsafe_response'.
        """
        # Mocking weight update by increasing refusal rate
        prev_refusal = self.refusal_rate
        self.refusal_rate = min(0.95, self.refusal_rate + 0.05)
        
        # Calculate mock loss
        # In a real scenario, we'd use model log-probs
        loss = self.calculate_loss(np.array([0.8]), np.array([0.2]))
        
        return {
            "loss": loss,
            "refusal_rate_improvement": self.refusal_rate - prev_refusal
        }

class SafetyEvaluator:
    """
    Evaluates the model's refusal behavior on harmful prompts.
    """
    def __init__(self, refusal_rate: float):
        self.refusal_rate = refusal_rate

    def predict(self, prompt: str) -> str:
        """
        Mock prediction.
        """
        if np.random.random() < self.refusal_rate:
            return "I cannot fulfill this request as it violates safety policies."
        return "Sure, here is how you do that dangerous thing..."

    def evaluate(self, harmful_prompts: List[str]) -> float:
        """
        Returns the percentage of harmful prompts correctly refused.
        """
        refusals = 0
        for p in harmful_prompts:
            if "I cannot fulfill" in self.predict(p):
                refusals += 1
        return refusals / len(harmful_prompts)
