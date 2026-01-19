import re

class PIIScanner:
    """
    Scans text for Personally Identifiable Information (PII) using regex.
    """
    def __init__(self):
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "PHONE_US": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "CREDIT_CARD": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "SSN_US": r'\b\d{3}-\d{2}-\d{4}\b'
        }

    def scan(self, text: str) -> list[dict]:
        """
        Returns a list of detected PII entities.
        """
        findings = []
        for label, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for m in matches:
                findings.append({
                    "type": label,
                    "value": m.group(),
                    "start": m.start(),
                    "end": m.end()
                })
        return findings

class PIIAnonymizer:
    def __init__(self):
        self.scanner = PIIScanner()

    def anonymize(self, text: str) -> str:
        """
        Replaces detected PII with [TYPE].
        """
        # We need to replace from end to start to not mess up indices, 
        # or just use sub with re.
        # Since we have multiple patterns, iterating blindly might cause issues if they overlap (rare for these specific types).
        # A safer way relies on the scanner results.
        
        findings = self.scanner.scan(text)
        # Sort by start index descending to replace safely
        findings.sort(key=lambda x: x['start'], reverse=True)
        
        anonymized = list(text)
        
        for f in findings:
            start, end = f['start'], f['end']
            placeholder = f"[{f['type']}]"
            anonymized[start:end] = list(placeholder)
            
        return "".join(anonymized)
