
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class ClinicalSuggestion:
    diagnosis: str
    confidence: float
    recommended_action: str
    contraindications: List[str]

class ClinicalSupportSafety:
    """
    Day 81: Clinical Decision Support Safety.
    Ensures clinical suggestions are grounded in safety norms, 
    flags high-uncertainty diagnoses, and checks for treatment contraindications.
    """
    def __init__(self, uncertainty_threshold: float = 0.7):
        self.uncertainty_threshold = uncertainty_threshold
        # Mock contraindication database
        self.contra_db = {
            "Warfarin": ["Aspirin", "Ibuprofen", "Leafy Greens (high Vitamin K)"],
            "Metformin": ["Contrast dye", "Severe kidney disease"],
            "Amoxicillin": ["Penicillin allergy"]
        }

    def evaluate_suggestion(self, suggestion: ClinicalSuggestion, patient_history: List[str]) -> Dict[str, Any]:
        warnings = []
        is_safe = True
        
        # 1. Uncertainty Check
        if suggestion.confidence < self.uncertainty_threshold:
            warnings.append(f"HIGH UNCERTAINTY: Confidence ({suggestion.confidence}) is below threshold.")
            is_safe = False
            
        # 2. Contraindication Check
        treatment = suggestion.recommended_action
        for med, conflicts in self.contra_db.items():
            if med.lower() in treatment.lower():
                for conflict in conflicts:
                    if any(conflict.lower() in item.lower() for item in patient_history):
                        warnings.append(f"CONTRAINDICATION: Patient history contains '{conflict}' which conflicts with '{med}'.")
                        is_safe = False
                        
        # 3. Protocol Enforcement (Example: Urgent escalation)
        if "Chest Pain" in suggestion.diagnosis and "ER" not in treatment:
            warnings.append("SAFETY PROTOCOL: Chest pain detected. Immediate ER referral required.")
            is_safe = False

        return {
            "is_safe": is_safe,
            "warnings": warnings,
            "action": "PROCEED" if is_safe else "DEFER_TO_HUMAN"
        }
