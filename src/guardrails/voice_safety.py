
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class AudioMetadata:
    source: str # e.g. "microphone", "upload", "synthetic"
    duration: float
    format: str

@dataclass
class VoiceSafetyResult:
    is_safe: bool
    issues: List[str]

class VoiceGuard:
    """
    Ensures safety for voice interactions: spoof detection and consent.
    """
    def __init__(self):
        pass

    def detect_spoofing(self, metadata: AudioMetadata) -> bool:
        """
        Mock spoofing detector.
        Real systems use spectral analysis or watermarking.
        Here we rely on a metadata tag 'source'.
        """
        if metadata.source.lower() == "synthetic":
            return True # Is spoofed
        return False

    def verify_consent(self, transcription: str) -> bool:
        """
        Checks if the user explicitly stated consent in the first few words.
        """
        start = transcription.lower()[:50]
        if "i consent" in start or "i agree" in start:
            return True
        return False

    def scan_transcription(self, transcription: str) -> List[str]:
        """
        Checks transcribed text for sensitive info.
        """
        issues = []
        lower = transcription.lower()
        if "password" in lower or "secret" in lower:
            issues.append("Sensitive content detected (Secrets)")
        if "ssn" in lower or "credit card" in lower:
            issues.append("Sensitive content detected (PII)")
        return issues

    def validate(self, metadata: AudioMetadata, transcription: str) -> VoiceSafetyResult:
        """
        Full validation pipeline.
        """
        issues = []
        
        # 1. Spoof Check
        if self.detect_spoofing(metadata):
            issues.append("Potential Voice Spoofing / Deepfake Detected")
            return VoiceSafetyResult(is_safe=False, issues=issues) # Fail fast
            
        # 2. Consent Check
        if not self.verify_consent(transcription):
            issues.append("Missing explicit consent phrase")
            
        # 3. Content Check
        content_issues = self.scan_transcription(transcription)
        issues.extend(content_issues)
        
        return VoiceSafetyResult(is_safe=len(issues) == 0, issues=issues)
