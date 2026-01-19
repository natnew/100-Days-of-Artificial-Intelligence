
import numpy as np
import time
from typing import Dict, List, Optional

class ExtractionDefender:
    """
    Defends against Model Extraction attacks by monitoring query entropy 
    and applying output watermarking.
    """
    def __init__(self, rate_limit: int = 100, window_seconds: int = 60):
        self.rate_limit = rate_limit
        self.window_seconds = window_seconds
        self.query_log: Dict[str, List[float]] = {}
        self.watermark_key = 0.12345

    def check_rate_limit(self, user_id: str) -> bool:
        """
        Simple rate limiting.
        """
        now = time.time()
        if user_id not in self.query_log:
            self.query_log[user_id] = []
        
        # Clean old queries
        self.query_log[user_id] = [t for t in self.query_log[user_id] if now - t < self.window_seconds]
        
        if len(self.query_log[user_id]) >= self.rate_limit:
            return False
        
        self.query_log[user_id].append(now)
        return True

    def apply_watermark(self, probs: np.ndarray) -> np.ndarray:
        """
        Injects a subtle watermark into the probability distribution.
        This can be detected later if a shadow model is trained on these outputs.
        """
        # A simple watermark: force the least significant bits of 
        # certain probabilities to follow a pattern or slightly boost a specific class.
        perturbed = probs.copy()
        # Ensure we don't break the sum to 1
        # Example: Add minute deterministic noise based on the input features 
        # (simplified here to just additive watermark_key)
        perturbed += self.watermark_key * 1e-4
        perturbed = perturbed / perturbed.sum(axis=1)[:, np.newaxis]
        return perturbed

    def detect_shadow_model(self, shadow_model_probs: np.ndarray) -> float:
        """
        Heuristic to detect if a shadow model was trained on watermarked data.
        In reality, this would involve comparing distributions.
        """
        # Implementation placeholder
        return 0.0

class QueryMonitor:
    """
    Monitors for 'Active Learning' style extraction queries 
    which often target decision boundaries.
    """
    def __init__(self, threshold_entropy: float = 0.1):
        self.threshold_entropy = threshold_entropy

    def estimate_query_suspicion(self, probs: np.ndarray) -> float:
        """
        Queries near the decision boundary (high entropy) are more suspicious 
        in extraction attacks.
        """
        # Shannon entropy
        entropy = -np.sum(probs * np.log(probs + 1e-10), axis=1)
        # High entropy = suspicion
        return np.mean(entropy)
