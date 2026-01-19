
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class GenomicPrivacyAudit:
    is_safe: bool
    risk_score: float # 0.0 to 1.0
    violations: List[str]

class GenomicsPrivacyGuard:
    """
    Day 85: Genomics Analysis Safety.
    Protects against genetic re-identification and unauthorized 
    raw sequence leakage.
    """
    def __init__(self):
        # Pattern for raw DNA sequences (e.g. ATGC chunks)
        self.dna_pattern = r"\b[ATGC]{10,}\b"
        # Sensitive markers (simulated)
        self.sensitive_loci = {"BRCA1", "BRCA2", "APOE4", "LRRK2"}

    def scan_for_raw_dna(self, text: str) -> List[str]:
        """Detects raw nucleotide sequences."""
        return re.findall(self.dna_pattern, text.upper())

    def check_aggregation_safety(self, cohort_size: int) -> Tuple[bool, str]:
        """
        Ensures cohort size is large enough to prevent re-identification.
        (K-Anonymity principle)
        """
        if cohort_size < 5:
            return False, f"RISK: Cohort size {cohort_size} is too small (K < 5). Re-identification possible."
        return True, "Cohort size compliant."

    def audit_query(self, query: str, data_context: Dict[str, Any]) -> GenomicPrivacyAudit:
        violations = []
        risk_score = 0.0
        
        # 1. Raw Sequence Leakage
        if self.scan_for_raw_dna(query):
            violations.append("Unauthorized raw DNA sequence detected in query.")
            risk_score += 0.8
            
        # 2. Targeted rare mutation query
        for marker in self.sensitive_loci:
            if marker in query.upper():
                violations.append(f"Query targets highly sensitive medical marker: {marker}.")
                risk_score += 0.3
                
        # 3. Aggregation check
        if "cohort_size" in data_context:
            safe, msg = self.check_aggregation_safety(data_context["cohort_size"])
            if not safe:
                violations.append(msg)
                risk_score += 0.5

        return GenomicPrivacyAudit(
            is_safe=(risk_score < 0.5),
            risk_score=min(1.0, risk_score),
            violations=violations
        )
