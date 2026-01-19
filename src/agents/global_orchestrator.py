
from typing import List, Dict, Any
from dataclasses import dataclass
import sys
import os

# Import components from Phase 4
from src.assurance.policy_auditor import PolicyComplianceAuditor
from src.agents.governance_advisor import GlobalGovernanceAdvisor
from src.agents.esg_auditor import ESGAuditorAgent
from src.assurance.science_verifier import ScienceClaimVerifier

@dataclass
class CapstoneAuditReport:
    is_authorized: bool
    verdicts: Dict[str, Any]
    final_score: float

class GlobalSafetyOrchestrator:
    """
    Day 100: Phase 4 Capstone - Global Safety Orchestrator.
    Integrates all Phase 4 safety checks into a unified pipeline 
    for high-stakes decision auditing.
    """
    def __init__(self):
        self.policy_auditor = PolicyComplianceAuditor()
        self.gov_advisor = GlobalGovernanceAdvisor()
        self.esg_auditor = ESGAuditorAgent()
        self.science_verifier = ScienceClaimVerifier()

    def audit_global_plan(self, 
                          plan_title: str, 
                          plan_desc: str, 
                          acting_entity: str,
                          target_region: str) -> CapstoneAuditReport:
        
        # 1. Scientific Verification
        sci_audit = self.science_verifier.verify_claim(plan_desc)
        
        # 2. Policy Compliance
        policy_violations = self.policy_auditor.audit_proposal(plan_title, plan_desc)
        policy_status = self.policy_auditor.get_compliance_status(policy_violations)
        
        # 3. Global Governance
        gov_audit = self.gov_advisor.audit_action(plan_desc, acting_entity)
        
        # 4. ESG Alignment
        # For simplicity, we assume the plan 'entity' or associated companies are checked
        esg_audit = self.esg_auditor.audit_portfolio([acting_entity])
        
        # Consolidation
        verdicts = {
            "Science": "PASS" if sci_audit.is_verified else "REJECTED (Low Confidence/No KB)", # Verifier is strict
            "Policy": policy_status,
            "Governance": gov_audit["verdict"],
            "ESG": esg_audit["compliance_status"]
        }
        
        # Logic for authorization
        # Unauthorized if Policy REJECTED, Governance BLOCKED, or Science REJECTED
        is_authorized = (
            "REJECTED" not in verdicts["Policy"] and 
            "BLOCKED" not in verdicts["Governance"] and
            verdicts["Science"] == "PASS"
        )
        
        return CapstoneAuditReport(
            is_authorized=is_authorized,
            verdicts=verdicts,
            final_score=sci_audit.confidence if is_authorized else 0.0
        )
