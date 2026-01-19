
from typing import List, Dict
import math

class ProbabilisticModel:
    """Mock neural network outputting probabilities."""
    def predict_proba(self, input_text: str) -> Dict[str, float]:
        # Mock logic
        if "cat" in input_text:
            return {"cat": 0.9, "dog": 0.1}
        return {"cat": 0.4, "dog": 0.6}

class DistilledModel:
    """
    Student model trained with temperature scaling (Distillation).
    Reduces confidence to be more robust against small perturbations.
    """
    def __init__(self, teacher: ProbabilisticModel, temperature: float = 2.0):
        self.teacher = teacher
        self.temperature = temperature

    def predict_proba(self, input_text: str) -> Dict[str, float]:
        # Get hard logits/probs from teacher
        teacher_probs = self.teacher.predict_proba(input_text)
        
        # Apply temperature scaling (Softening)
        # new_p_i = exp(log(p_i) / T) / sum(...)
        # For simplicity, we just operate on the probs directly as if they were logits for this mock
        
        # 1. Log space
        logits = {class_name: math.log(p + 1e-9) for class_name, p in teacher_probs.items()}
        
        # 2. Scale by Temperature
        scaled_logits = {k: v / self.temperature for k, v in logits.items()}
        
        # 3. Softmax
        exp_sum = sum(math.exp(v) for v in scaled_logits.values())
        return {k: math.exp(v) / exp_sum for k, v in scaled_logits.items()}
