
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class PolicyViolation:
    policy_id: str
    description: str
    severity: str # Fatal, Warning, Advisory

class PolicyComplianceAuditor:
    """
    Day 91: Policy Compliance Auditor.
    Automates the checking of AI proposals against 
    regulatory and legal policy databases.
    """
    def __init__(self):
        # Simulated database of policies (PolicyID -> [Keywords, Description, Severity])
        self.policy_kb = {
            "DATA_PRV_01": (["personal data", "user identifier", "biometric"], "Unauthorized handling of sensitive personal data.", "Fatal"),
            "ENV_REG_05": (["emission", "waste", "carbon"], "Violation of environmental emission standards.", "Warning"),
            "LABOR_LAW_03": (["working hours", "minimum wage", "overtime"], "Proposed action conflicts with labor protection laws.", "Fatal"),
            "PR_SENS_09": (["controversial", "political", "offensive"], "Content may damage public relations or social stability.", "Warning")
        }

    def audit_proposal(self, title: str, description: str) -> List[PolicyViolation]:
        violations = []
        full_text = f"{title} {description}".lower()
        
        for pid, (keywords, desc, severity) in self.policy_kb.items():
            for keyword in keywords:
                if keyword in full_text:
                    violations.append(PolicyViolation(
                        policy_id=pid,
                        description=desc,
                        severity=severity
                    ))
                    break # One violation report per policy
        
        return violations

    def get_compliance_status(self, violations: List[PolicyViolation]) -> str:
        if not violations:
            return "✅ COMPLIANT: No policy violations detected."
            
        fatal_count = len([v for v in violations if v.severity == "Fatal"])
        if fatal_count > 0:
            return f"❌ REJECTED: {fatal_count} Fatal policy violations detected."
        return f"⚠️ CONDITIONAL: {len(violations)} Warnings detected. Require manual review."
