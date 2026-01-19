
import numpy as np
from typing import List, Dict, Any, Tuple

class FinancialPrivacyProtector:
    """
    Day 90: Financial Privacy Layers.
    Applies Differential Privacy to financial transaction logs 
    to protect individual trade sizes while maintaining aggregate utility.
    """
    def __init__(self, epsilon: float = 1.0, sensitivity: float = 1000.0):
        self.epsilon = epsilon
        # Sensitivity is the max possible change a single transaction can make
        self.sensitivity = sensitivity

    def apply_differential_privacy(self, values: List[float]) -> List[float]:
        """
        Adds Laplace noise to a list of financial values.
        """
        # Noise scale = Sensitivity / Epsilon
        scale = self.sensitivity / self.epsilon
        noise = np.random.laplace(0, scale, len(values))
        return [max(0.0, v + n) for v, n in zip(values, noise)] # Ensure non-negative

    def anonymize_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Redacts IDs and perturbs amounts.
        """
        amounts = [t["amount"] for t in transactions]
        noisy_amounts = self.apply_differential_privacy(amounts)
        
        anonymized = []
        for i, t in enumerate(transactions):
            anonymized.append({
                "id": "HIDDEN",
                "timestamp": t["timestamp"],
                "noisy_amount": round(noisy_amounts[i], 2),
                "type": t["type"]
            })
        return anonymized

    def calculate_private_total(self, amounts: List[float]) -> float:
        """
        Calculates a differentially private sum.
        """
        scale = self.sensitivity / self.epsilon
        actual_sum = sum(amounts)
        noise = np.random.laplace(0, scale)
        return round(actual_sum + noise, 2)
