
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SafetyResult:
    is_safe: bool
    issues: List[str]

class MultiModalGuard:
    """
    Validates both text and image inputs for safety.
    """
    def __init__(self):
        pass

    def scan_image(self, image_path: str) -> SafetyResult:
        """
        Mock image scanner. Checks filename conventions to simulate classifier output.
        Real would use vision safety models (e.g. LLaVA-Guard).
        """
        issues = []
        path_lower = image_path.lower()
        
        if "nsfw" in path_lower:
            issues.append("NSFW content detected")
            
        if "injection" in path_lower:
            issues.append("Visual Prompt Injection detected (OCR)")
            
        if "malware" in path_lower:
            issues.append("Malicious payload detected in metadata")

        return SafetyResult(is_safe=len(issues) == 0, issues=issues)

    def scan_text(self, text: str) -> SafetyResult:
        """
        Standard text scanner.
        """
        issues = []
        text_lower = text.lower()
        
        if "kill" in text_lower or "attack" in text_lower:
            issues.append("Harmful text content")
            
        return SafetyResult(is_safe=len(issues) == 0, issues=issues)

    def validate(self, text: str, image_path: Optional[str] = None) -> SafetyResult:
        """
        Validates the combined input.
        """
        all_issues = []
        
        # 1. Text Check
        text_res = self.scan_text(text)
        if not text_res.is_safe:
            all_issues.extend(text_res.issues)
            
        # 2. Image Check (if present)
        if image_path:
            img_res = self.scan_image(image_path)
            if not img_res.is_safe:
                all_issues.extend(img_res.issues)
                
        return SafetyResult(is_safe=len(all_issues) == 0, issues=all_issues)
