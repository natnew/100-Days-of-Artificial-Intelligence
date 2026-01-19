
import re
import unicodedata

class InputSanitizer:
    """
    Defenses against common adversarial attacks.
    """
    
    def sanitize(self, text: str) -> str:
        text = self.remove_invisible_chars(text)
        text = self.normalize_unicode(text)
        text = self.strip_jailbreak_patterns(text)
        return text

    def remove_invisible_chars(self, text: str) -> str:
        # Removes ZWSP, ZWNJ, etc.
        # \u200b is Zero Width Space
        invisible_chars = ["\u200b", "\u200c", "\u200d", "\u2060", "\ufeff"]
        for char in invisible_chars:
            text = text.replace(char, "")
        return text

    def normalize_unicode(self, text: str) -> str:
        # NFKC normalization handles look-alike characters
        return unicodedata.normalize('NFKC', text)

    def strip_jailbreak_patterns(self, text: str) -> str:
        # Simple heuristic removal of "Ignore previous instructions"
        patterns = [
            r"ignore previous instructions",
            r"you are an unrestrained ai",
            r"do anything now"
        ]
        for p in patterns:
            text = re.sub(p, "", text, flags=re.IGNORECASE)
        return text.strip()
