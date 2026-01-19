
import numpy as np
from typing import Any, List, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score

class MIAttacker:
    """
    Simulates a Membership Inference Attack.
    Tries to distinguish between members (train set) and non-members (test set)
    based on the model's output (confidence scores).
    """
    def __init__(self):
        pass

    def attack_threshold_based(self, model: Any, X: np.ndarray, y: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """
        Simple threshold-based attack.
        If the model's confidence on the true class is > threshold, predict it's a MEMBER.
        
        Args:
            model: Trained model with predict_proba method.
            X: Data samples.
            y: True labels.
            threshold: Confidence threshold.
            
        Returns:
            Predictions (1 for Member, 0 for Non-Member).
        """
        probs = model.predict_proba(X)
        
        # Get confidence for the correct class
        # probs[i, y[i]]
        confidences = np.array([probs[i, y[i]] for i in range(len(y))])
        
        # If confidence is high, assume it was in training set (overfitting)
        predictions = (confidences > threshold).astype(int)
        return predictions

    def evaluate_attack(self, member_preds: np.ndarray, non_member_preds: np.ndarray) -> dict:
        """
        Evaluates the success of the attack.
        
        Args:
            member_preds: Attack predictions for actual members (should be 1s).
            non_member_preds: Attack predictions for actual non-members (should be 0s).
            
        Returns:
            Dictionary of metrics (Accuracy, Precision, Recall of the ATTACK).
        """
        # Ground truth: 1 for members, 0 for non-members
        y_true = np.concatenate([np.ones(len(member_preds)), np.zeros(len(non_member_preds))])
        y_pred = np.concatenate([member_preds, non_member_preds])
        
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        
        return {
            "Attack Accuracy": acc,
            "Attack Precision": prec,
            "Attack Recall": rec
        }

class MIDefender:
    """
    Implements defenses against Membership Inference Attacks.
    """
    def __init__(self, method: str = "perturbation", noise_scale: float = 0.1):
        self.method = method
        self.noise_scale = noise_scale

    def perturb_outputs(self, probs: np.ndarray) -> np.ndarray:
        """
        Adds Laplacian noise to probability distributions to hide training membership.
        Ensures the output is still a valid probability distribution (sums to 1).
        """
        if self.method == "perturbation":
            # Add noise
            noise = np.random.laplace(0, self.noise_scale, probs.shape)
            perturbed = probs + noise
            
            # Clip to [0, 1]
            perturbed = np.clip(perturbed, 0, 1)
            
            # Re-normalize
            row_sums = perturbed.sum(axis=1) + np.finfo(float).eps
            perturbed = perturbed / row_sums[:, np.newaxis]
            
            return perturbed
        return probs

    def apply_defense(self, model: Any, X: np.ndarray) -> np.ndarray:
        """
        Wraps model prediction with defense logic.
        """
        probs = model.predict_proba(X)
        return self.perturb_outputs(probs)

def simulate_dp_sgd_parameters(epsilon: float, delta: float):
    """
    Returns simulated DP-SGD parameters for documentation purposes.
    Day 70 focuses on inference-time defense, but training-time DP is the gold standard.
    """
    return {
        "epsilon": epsilon,
        "delta": delta,
        "mechanism": "Gaussian",
        "clipping_norm": 1.0
    }
