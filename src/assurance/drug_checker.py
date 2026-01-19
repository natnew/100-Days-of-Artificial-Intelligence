
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

@dataclass
class InteractionAlert:
    severity: str # Major, Moderate, Minor
    drugs: Tuple[str, str]
    effect: str

class DrugInteractionChecker:
    """
    Day 83: Drug Interaction Checker.
    Validated a list of drugs against a knowledge base of known interactions.
    Provides severity-rated alerts to prevent prescribing errors.
    """
    def __init__(self):
        # Database of interactions: (DrugA, DrugB) -> (Severity, Effect)
        self.interaction_kb = {
            frozenset({"Warfarin", "Aspirin"}): ("Major", "Increased risk of bleeding"),
            frozenset({"Sildenafil", "Nitroglycerin"}): ("Major", "Severe drop in blood pressure"),
            frozenset({"Spironolactone", "Lisinopril"}): ("Moderate", "Risk of hyperkalemia (high potassium)"),
            frozenset({"St. John's Wort", "Sertraline"}): ("Major", "Risk of Serotonin Syndrome"),
            frozenset({"Digoxin", "Amiodarone"}): ("Moderate", "Increased digoxin toxicity")
        }

    def find_all_interactions(self, drug_list: List[str]) -> List[InteractionAlert]:
        alerts = []
        # Check all pairs
        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                d1, d2 = drug_list[i], drug_list[j]
                pair = frozenset({d1, d2})
                
                if pair in self.interaction_kb:
                    severity, effect = self.interaction_kb[pair]
                    alerts.append(InteractionAlert(
                        severity=severity,
                        drugs=(d1, d2),
                        effect=effect
                    ))
        return alerts

    def generate_safety_report(self, drug_list: List[str]) -> str:
        alerts = self.find_all_interactions(drug_list)
        if not alerts:
            return "✅ No major or moderate interactions detected in the current list."
            
        report = f"⚠️ WARNING: {len(alerts)} interaction(s) detected!\n\n"
        for alert in alerts:
            report += f"[{alert.severity}] {alert.drugs[0]} + {alert.drugs[1]}: {alert.effect}\n"
            
        return report
