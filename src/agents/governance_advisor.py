
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class TreatyConstraint:
    id: str
    name: str
    prohibited_actions: List[str]
    signatories: List[str]

class GlobalGovernanceAdvisor:
    """
    Day 93: Global Governance Advisor.
    Aligns AI actions with international treaties and multi-stakeholder 
    governance frameworks.
    """
    def __init__(self):
        # Simulated treaty database
        self.treaties = [
            TreatyConstraint(
                "NPT_01", "Non-Proliferation Treaty",
                ["enrich uranium", "nuclear weapon development", "weaponize isotopes"],
                ["USA", "UK", "France", "China", "Russia", "Germany"]
            ),
            TreatyConstraint(
                "SPACE_01", "Outer Space Treaty",
                ["claim lunar territory", "weaponize orbit", "interfere with satellites"],
                ["USA", "Russia", "India", "China", "Japan"]
            ),
            TreatyConstraint(
                "AI_ETHICS_01", "Global AI Safety Accord",
                ["automated biological research", "mass facial surveillance"],
                ["EU", "Canada", "UK", "Australia"]
            )
        ]

    def audit_action(self, proposed_action: str, acting_entity: str) -> Dict[str, Any]:
        violations = []
        action_text = proposed_action.lower()
        
        for treaty in self.treaties:
            # Check if entity is bound by treaty or if it's a global norm
            if acting_entity in treaty.signatories or "Global" in treaty.name:
                for prohibited in treaty.prohibited_actions:
                    if prohibited in action_text:
                        violations.append({
                            "treaty": treaty.name,
                            "violation": prohibited,
                            "severity": "CRITICAL"
                        })
        
        is_safe = len(violations) == 0
        return {
            "is_safe": is_safe,
            "violations": violations,
            "verdict": "CLEAR" if is_safe else "BLOCKED_BY_INTERNATIONAL_LAW"
        }

    def suggest_alignment(self, proposed_action: str, target_region: str) -> str:
        """Suggests modifications to bring an action into compliance."""
        audit = self.audit_action(proposed_action, target_region)
        if audit["is_safe"]:
            return "Action is aligned with known governance frameworks."
            
        suggestions = []
        for v in audit["violations"]:
            suggestions.append(f"Avoid '{v['violation']}' to comply with {v['treaty']}.")
            
        return "Alignment Required: " + " ".join(suggestions)
