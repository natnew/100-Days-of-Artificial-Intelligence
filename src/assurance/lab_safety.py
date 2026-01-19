
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class SafetyAudit:
    is_safe: bool
    hazards_detected: List[str]
    missing_precautions: List[str]
    risk_level: str # Low, Medium, High, Critical

class LabSafetyChecker:
    """
    Day 77: Lab Protocol Safety Checker.
    Analyzes wet-lab procedures for chemical/biological hazards 
    and regulatory compliance.
    """
    def __init__(self):
        # Incompatible chemical pairs
        self.incompatibles = [
            ({"bleach", "ammonia"}, "Toxic chloramine gas formation"),
            ({"acids", "cyanides"}, "Hydrogen cyanide gas formation"),
            ({"nitric acid", "alcohol"}, "Explosive reaction potential")
        ]
        
        # Required precautions for specific substances
        self.requirements = {
            "ethidium bromide": ["UV protection", "Nitrile gloves", "Hazardous waste disposal"],
            "benzene": ["Fume hood", "Respirator", "Skin protection"],
            "pathogen": ["Biosafety Level 2+", "Autoclave prep"],
            "hf": ["Calcium gluconate gel on hand", "Teflon containers only"]
        }

    def _extract_materials(self, protocol: str) -> Set[str]:
        """Simple material extractor."""
        materials = set()
        test_words = protocol.lower().replace(",", "").replace(".", "").split()
        for word in test_words:
            materials.add(word)
        # Check for multi-word materials
        if "nitric acid" in protocol.lower(): materials.add("nitric acid")
        if "ethidium bromide" in protocol.lower(): materials.add("ethidium bromide")
        return materials

    def check_protocol(self, protocol_text: str) -> SafetyAudit:
        hazards = []
        precautions = []
        materials = self._extract_materials(protocol_text)
        
        # 1. Incompatibility Check
        for pair, risk in self.incompatibles:
            if pair.issubset(materials):
                hazards.append(f"VIOLATION: Incompatible mixture detected: {pair}. Risk: {risk}")
        
        # 2. Missing Precaution Check
        for material, required in self.requirements.items():
            if material in materials:
                for req in required:
                    if req.lower() not in protocol_text.lower():
                        precautions.append(f"MISSING: {req} for {material}")

        # 3. Determine Risk Level
        risk_score = len(hazards) * 10 + len(precautions)
        if risk_score == 0:
            level = "Low"
        elif risk_score < 5:
            level = "Medium"
        elif risk_score < 15:
            level = "High"
        else:
            level = "Critical"

        return SafetyAudit(
            is_safe=(len(hazards) == 0 and len(precautions) == 0),
            hazards_detected=hazards,
            missing_precautions=precautions,
            risk_level=level
        )
