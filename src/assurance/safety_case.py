
from typing import List, Dict, Optional
from datetime import datetime
import json

class Evidence:
    """
    Represents a single piece of evidence (e.g., a test result, a metric).
    """
    def __init__(self, id: str, description: str, data: Dict, timestamp: Optional[datetime] = None):
        self.id = id
        self.description = description
        self.data = data
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }

class Argument:
    """
    Connects Evidence to a Claim.
    """
    def __init__(self, id: str, description: str, evidence_ids: List[str]):
        self.id = id
        self.description = description
        self.evidence_ids = evidence_ids
    
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "evidence_ids": self.evidence_ids
        }

class Claim:
    """
    A high-level safety claim.
    """
    def __init__(self, id: str, description: str, sub_claims: List['Claim'] = None, arguments: List[Argument] = None):
        self.id = id
        self.description = description
        self.sub_claims = sub_claims or []
        self.arguments = arguments or []
        self.status = "Pending"  # Pending, Verified, Failed

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "sub_claims": [c.to_dict() for c in self.sub_claims],
            "arguments": [a.to_dict() for a in self.arguments],
            "status": self.status
        }

class SafetyCase:
    """
    The main container for the safety case.
    """
    def __init__(self, title: str, version: str):
        self.title = title
        self.version = version
        self.claims: Dict[str, Claim] = {}
        self.evidence_store: Dict[str, Evidence] = {}
    
    def add_claim(self, claim: Claim):
        self.claims[claim.id] = claim
    
    def add_evidence(self, evidence: Evidence):
        self.evidence_store[evidence.id] = evidence
    
    def evaluate(self):
        """
        Simple evaluation logic:
        A claim is 'Verified' if it has at least one argument, and all arguments are supported by valid evidence.
        In a real system, this would involve complex logic or human review.
        """
        for claim_id, claim in self.claims.items():
            if not claim.arguments and not claim.sub_claims:
                 claim.status = "Pending (No Arguments)"
                 continue
            
            # For now, just mark verified if evidence exists for all arguments
            all_args_supported = True
            for arg in claim.arguments:
                for ev_id in arg.evidence_ids:
                    if ev_id not in self.evidence_store:
                        all_args_supported = False
            
            if all_args_supported:
                claim.status = "Verified"
            else:
                claim.status = "Failed (Missing Evidence)"

    def generate_report(self) -> str:
        report = [f"# Safety Case: {self.title} (v{self.version})", ""]
        
        for claim_id, claim in self.claims.items():
            report.append(f"## Claim: {claim.description} ({claim.status})")
            for arg in claim.arguments:
                report.append(f"- **Argument**: {arg.description}")
                for ev_id in arg.evidence_ids:
                    if ev_id in self.evidence_store:
                        ev = self.evidence_store[ev_id]
                        report.append(f"  - *Evidence*: {ev.description} (Data: {ev.data})")
                    else:
                        report.append(f"  - *Missing Evidence ID*: {ev_id}")
            report.append("")
        
        return "\n".join(report)

