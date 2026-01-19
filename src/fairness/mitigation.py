
import numpy as np
from typing import List, Union, Any

class AdversarialDebiaser:
    """
    Simulates the effect of Adversarial Debiasing by aligning the score distributions
    of different groups.
    
    In a real deep learning context, this would be a model with a gradient reversal layer
    that penalizes the network if an adversary can predict the sensitive attribute 
    from the internal representation.
    
    Here, we simulate the *result* of such a process: the output scores become
    uncorrelated with the sensitive attribute (at least on average).
    """
    
    def __init__(self):
        self.group_means = {}
        self.global_mean = 0.0

    def fit_transform(
        self, 
        y_scores: Union[List[float], np.ndarray], 
        sensitive_features: Union[List[Any], np.ndarray]
    ) -> np.ndarray:
        """
        Adjusts y_scores so that the mean score is identical across all groups.
        """
        y_scores = np.array(y_scores)
        sensitive_features = np.array(sensitive_features)
        groups = np.unique(sensitive_features)
        
        self.global_mean = np.mean(y_scores)
        
        # Calculate group means
        for group in groups:
            mask = (sensitive_features == group)
            if np.any(mask):
                self.group_means[group] = np.mean(y_scores[mask])
            else:
                self.group_means[group] = self.global_mean
                
        # Debias
        y_debiased = y_scores.copy()
        
        for group in groups:
            mask = (sensitive_features == group)
            if np.any(mask):
                # Shift distribution: score = score - group_mean + global_mean
                # This aligns the center of mass for this group to the global center
                adjustment = self.global_mean - self.group_means[group]
                y_debiased[mask] += adjustment
        
        # Clip to ensure valid probabilities [0, 1]
        y_debiased = np.clip(y_debiased, 0.0, 1.0)
        
        return y_debiased
