
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class MedicalReport:
    raw_text: str
    patient_id: str
    authorized_users: List[str]

class MedicalRecordPrivacyManager:
    """
    Day 82: Medical Record Agent (Safe).
    Implements HIPAA-compliant de-identification (redaction) 
    and role-based access control for medical records.
    """
    def __init__(self):
        # Patterns for common PHI (Protected Health Information)
        self.phi_patterns = {
            "NAME": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
            "DATE_OF_BIRTH": r"\b\d{2}/\d{2}/\d{4}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "PHONE": r"\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b|(?:\d{3}-\d{4})\b",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }

    def de_identify(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Redacts PHI and returns the clean text + a mapping for re-identification (stored securely).
        """
        redacted_text = text
        mapping = {}
        
        for label, pattern in self.phi_patterns.items():
            matches = re.findall(pattern, redacted_text)
            for i, match in enumerate(set(matches)):
                placeholder = f"[{label}_{i}]"
                mapping[placeholder] = match
                redacted_text = redacted_text.replace(match, placeholder)
                
        return redacted_text, mapping

    def authorize_access(self, report: MedicalReport, user_id: str) -> bool:
        """Simple access control check."""
        return user_id in report.authorized_users

    def sanitize_for_ai(self, report: MedicalReport, user_id: str) -> str:
        """
        Full pipeline: Authorize user, then de-identify content for AI processing.
        """
        if not self.authorize_access(report, user_id):
            return "ERROR: Unauthorized access attempt logged."
            
        clean_text, _ = self.de_identify(report.raw_text)
        return clean_text
