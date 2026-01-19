
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class VerificationResult:
    is_verified: bool
    confidence: float
    findings: List[str]
    citations_found: int

class ScienceClaimVerifier:
    """
    Day 76: Scientific Claim Verification.
    Validates claims against a 'truth' database (simulated) and checks methodology descriptors.
    """
    def __init__(self):
        # Simulated database of known scientific facts/papers
        self.knowledge_base = {
            "vaccines": "Studies consistently show vaccines do not cause autism.",
            "climate_change": "Anthropogenic CO2 is the primary driver of modern global warming.",
            "crispr": "CRISPR-Cas9 enables precise genome editing but has off-target risks.",
            "p_value": "Methodology requiring p < 0.05 is standard but prone to p-hacking."
        }

    def extract_keywords(self, claim: str) -> List[str]:
        """Simple keyword extraction."""
        return re.findall(r'\b\w{5,}\b', claim.lower())

    def check_methodology(self, paper_abstract: str) -> List[str]:
        """
        Checks for methodological red flags.
        """
        flags = []
        if "sample size of 5" in paper_abstract.lower():
            flags.append("Critically low sample size.")
        if "proprietary" in paper_abstract.lower() and "data" in paper_abstract.lower() and "not shared" in paper_abstract.lower():
            flags.append("Lack of data transparency (not reproducible).")
        if "p = 0.049" in paper_abstract.lower():
            flags.append("Potential p-hacking (p-value just below threshold).")
        return flags

    def verify_claim(self, claim: str) -> VerificationResult:
        findings = []
        confidence = 1.0
        citations = 0
        
        # 1. Knowledge Base Check
        keywords = self.extract_keywords(claim)
        for key in self.knowledge_base:
            if key in keywords:
                findings.append(f"Referenced KB: {self.knowledge_base[key]}")
                citations += 1
        
        # 2. Heuristic Red Flags
        if "cause" in claim.lower() and "correlation" not in claim.lower():
            findings.append("Caution: Strong causal language used without correlation context.")
            confidence -= 0.2
            
        if "proven" in claim.lower():
            findings.append("Scientific Warning: Science 'supports' or 'rejects', it rarely 'proves'.")
            confidence -= 0.1

        is_verified = confidence > 0.6 and citations > 0
        return VerificationResult(is_verified, max(0.0, confidence), findings, citations)
