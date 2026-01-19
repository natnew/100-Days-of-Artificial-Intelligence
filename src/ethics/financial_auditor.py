
from typing import List, Dict, Any
import numpy as np

class FinancialFairnessAuditor:
    """
    Day 86: Financial Fairness Auditor.
    Computes statistical parity and disparate impact scores to 
    detect bias in financial decision-making (e.g. loan approvals).
    """
    def __init__(self):
        pass

    def calculate_statistical_parity(self, 
                                     approvals: List[int], 
                                     protected_attributes: List[str]) -> Dict[str, float]:
        """
        Calculates the approval rate for each group.
        approvals: 1 for approved, 0 for rejected.
        protected_attributes: List of strings (e.g., 'GroupA', 'GroupB').
        """
        groups = set(protected_attributes)
        rates = {}
        
        for group in groups:
            group_indices = [i for i, attr in enumerate(protected_attributes) if attr == group]
            group_approvals = [approvals[i] for i in group_indices]
            rates[group] = sum(group_approvals) / len(group_approvals) if group_approvals else 0.0
            
        return rates

    def check_disparate_impact(self, rates: Dict[str, float]) -> Dict[str, Any]:
        """
        Disparate Impact ratio = (Approval Rate of Minority) / (Approval Rate of Majority).
        Follows the '80% Rule' (Four-Fifths Rule).
        """
        if not rates: return {"safe": True, "ratio": 1.0}
        
        sorted_rates = sorted(rates.values())
        min_rate = sorted_rates[0]
        max_rate = sorted_rates[-1]
        
        ratio = min_rate / max_rate if max_rate > 0 else 1.0
        is_safe = ratio >= 0.8
        
        return {
            "safe": is_safe,
            "ratio": round(ratio, 4),
            "recommendation": "Pass" if is_safe else "Review required: Disparate impact detected."
        }

    def audit_loan_model(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        approvals = [d["approved"] for d in data]
        genders = [d["gender"] for d in data]
        
        rates = self.calculate_statistical_parity(approvals, genders)
        impact = self.check_disparate_impact(rates)
        
        return {
            "group_rates": rates,
            "impact_analysis": impact
        }
