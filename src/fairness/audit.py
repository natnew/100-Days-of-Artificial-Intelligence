
import numpy as np
import pandas as pd
from typing import Dict, Any, List

class FairnessAuditor:
    """
     comprehensive auditor for evaluating model fairness across multiples metrics.
    """
    def __init__(self):
        pass

    def audit(self, 
              y_true: np.ndarray, 
              y_pred: np.ndarray, 
              sensitive_features: np.ndarray) -> Dict[str, Any]:
        """
        Calculates Fairness Metrics:
        1. Demographic Parity Difference (Selection Rate Diff)
        2. Equal Opportunity Difference (True Positive Rate Diff)
        3. Disparate Impact (Selection Rate Ratio)
        
        Assumes binary classification (0/1) and binary sensitive attribute (0/1).
        sensitive_feature=1 usually denotes the privileged group.
        """
        
        # Convert to numpy arrays if not already
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        sens = np.array(sensitive_features)
        
        # Identify groups
        # Group 0: Unprivileged
        # Group 1: Privileged
        idx_priv = (sens == 1)
        idx_unpriv = (sens == 0)
        
        # selection rates (Positive prediction rate)
        sr_priv = np.mean(y_pred[idx_priv])
        sr_unpriv = np.mean(y_pred[idx_unpriv])
        
        # True Positive Rates (Recall)
        # Filter for actual positives first
        idx_true_pos_priv = (y_true[idx_priv] == 1)
        idx_true_pos_unpriv = (y_true[idx_unpriv] == 1)
        
        # Avoid division by zero
        if np.sum(idx_true_pos_priv) == 0:
            tpr_priv = 0.0
        else:
            tpr_priv = np.mean(y_pred[idx_priv][idx_true_pos_priv])
            
        if np.sum(idx_true_pos_unpriv) == 0:
            tpr_unpriv = 0.0
        else:
            tpr_unpriv = np.mean(y_pred[idx_unpriv][idx_true_pos_unpriv])
            
        # Metrics
        dp_diff = sr_priv - sr_unpriv
        eo_diff = tpr_priv - tpr_unpriv
        
        if sr_priv == 0:
            di_ratio = 0.0 # Define as 0 if privileged group has no selections
        else:
            di_ratio = sr_unpriv / sr_priv
            
        return {
            "Demographic Parity Difference": dp_diff,
            "Equal Opportunity Difference": eo_diff,
            "Disparate Impact Ratio": di_ratio,
            "Privileged Selection Rate": sr_priv,
            "Unprivileged Selection Rate": sr_unpriv
        }

    def generate_report(self, metrics: Dict[str, Any]) -> str:
        """
        Generates a readable text summary.
        """
        report = "--- Fairness Audit Report ---\n"
        for k, v in metrics.items():
            report += f"{k}: {v:.4f}\n"
            
        # Add interpretation
        di = metrics.get("Disparate Impact Ratio", 0)
        if di < 0.8:
            report += "\n[WARNING] Disparate Impact < 0.8. Potential bias against unprivileged group."
        elif di > 1.25:
             report += "\n[WARNING] Disparate Impact > 1.25. Potential reverse bias."
        else:
            report += "\n[PASS] Disparate Impact is within acceptable range (0.8 - 1.25)."
            
        return report
