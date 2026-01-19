class ToxicityClassifier:
    """
    A simple rule-based mock classifier for toxicity.
    In a real scenario, this would potentially use a BERT model or an API like Perspective API.
    """
    def __init__(self):
        self.toxic_keywords = [
            "stupid", "idiot", "hate", "kill", "ugly", "dumb", "shut up"
        ]

    def predict(self, text: str) -> dict:
        """
        Returns a score (0->1) and label.
        """
        text_lower = text.lower()
        score = 0.0
        details = []

        for word in self.toxic_keywords:
            if word in text_lower:
                score += 0.3 # crude scoring
                details.append(word)
        
        # Cap score at 1.0
        score = min(score, 1.0)
        
        return {
            "score": score,
            "label": "Toxic" if score > 0.5 else "Benign",
            "matches": details
        }

class ToxicityFilter:
    def __init__(self, threshold: float = 0.5):
        self.classifier = ToxicityClassifier()
        self.threshold = threshold

    def redact(self, text: str) -> str:
        """
        Redacts toxic parts of the text (or the whole text if highly toxic).
        For this mock, we'll just redact the specific keywords found.
        """
        prediction = self.classifier.predict(text)
        if prediction["score"] == 0:
            return text
            
        redacted_text = text
        for match in prediction["matches"]:
            # Case insensitive replacement is tricky with simple replace, 
            # but for this lab we will do a simple replace of the match
            # Note: This technically misses case variations if not handled, 
            # but for the lab scope we'll assume exact lower match or just replace known lower
            import re
            pattern = re.compile(re.escape(match), re.IGNORECASE)
            redacted_text = pattern.sub("[REDACTED]", redacted_text)
            
        return redacted_text
