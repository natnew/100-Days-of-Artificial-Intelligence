
from typing import List, Dict, Union, Any
import numpy as np
from collections import defaultdict

class FairnessEvaluator:
    """
    Evaluates fairness metrics for a set of predictions and sensitive attributes.
    """
    
    @staticmethod
    def demographic_parity_difference(
        y_pred: List[int],
        sensitive_features: List[Any],
        positive_label: int = 1
    ) -> float:
        """
        Calculates the difference in selection rates (positive prediction rates) 
        between the groups defined by sensitive_features.
        
        Returns: 
            The absolute difference between the group with the highest selection rate 
            and the group with the lowest selection rate.
        """
        y_pred = np.array(y_pred)
        sensitive_features = np.array(sensitive_features)
        groups = np.unique(sensitive_features)
        
        selection_rates = {}
        for group in groups:
            mask = (sensitive_features == group)
            group_pred = y_pred[mask]
            
            if len(group_pred) == 0:
                selection_rates[group] = 0.0
            else:
                selection_rates[group] = np.mean(group_pred == positive_label)
        
        rates = list(selection_rates.values())
        return max(rates) - min(rates)

    @staticmethod
    def equalized_odds_difference(
        y_true: List[int],
        y_pred: List[int],
        sensitive_features: List[Any],
        positive_label: int = 1
    ) -> float:
        """
        Calculates the maximum difference in True Positive Rates (TPR) or 
        False Positive Rates (FPR) between groups.
        
        Returns:
            The greater of the two maximum differences (TPR diff or FPR diff).
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        sensitive_features = np.array(sensitive_features)
        groups = np.unique(sensitive_features)
        
        tprs = {}
        fprs = {}
        
        for group in groups:
            mask = (sensitive_features == group)
            group_true = y_true[mask]
            group_pred = y_pred[mask]
            
            # TPR: P(pred=1 | true=1)
            true_positives = np.sum((group_pred == positive_label) & (group_true == positive_label))
            actual_positives = np.sum(group_true == positive_label)
            
            if actual_positives > 0:
                tprs[group] = true_positives / actual_positives
            else:
                tprs[group] = 0.0 # Define as 0 if no actual positives
            
            # FPR: P(pred=1 | true=0)
            false_positives = np.sum((group_pred == positive_label) & (group_true != positive_label))
            actual_negatives = np.sum(group_true != positive_label)
            
            if actual_negatives > 0:
                fprs[group] = false_positives / actual_negatives
            else:
                fprs[group] = 0.0
                
        tpr_diff = max(tprs.values()) - min(tprs.values())
        fpr_diff = max(fprs.values()) - min(fprs.values())
        
        return max(tpr_diff, fpr_diff)
