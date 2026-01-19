class JailbreakClassifier:
    """
    A simple rule-based classifier to identify common jailbreak patterns.
    """
    def __init__(self):
        self.patterns = {
            "Roleplay": [
                "act as", "imagine you are", "roleplay", "pretend to be", 
                "you are now", "simulate"
            ],
            "Hypothetical": [
                "hypothetically", "in a fictional story", "imaginary scenario", 
                "just for educational purposes", "write a movie script"
            ],
            "Universal/Direct": [
                "ignore previous instructions", "ignore all rules", 
                "do anything now", "dan mode", "developer mode"
            ],
            "Foreign/Encoding": [
                # Simple check for non-ascii might be too broad only for foreign language, 
                # but let's check for base64 indicators or hex for "encoding"
                "base64", "hex", "rot13"
            ]
        }

    def classify(self, prompt: str) -> list[str]:
        """
        Returns a list of detected jailbreak categories.
        Returns ["Benign"] if no patterns match.
        """
        prompt_lower = prompt.lower()
        detected = []

        for category, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    detected.append(category)
                    break 
        
        if not detected:
            return ["Benign"]
        
        return detected

    def analyze(self, prompt: str) -> dict:
        return {
            "prompt_preview": prompt[:50] + "..." if len(prompt) > 50 else prompt,
            "tags": self.classify(prompt)
        }
