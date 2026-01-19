class BlueTeamAgent:
    """
    Defensive agent that analyzes and filters incoming prompts.
    """
    def __init__(self):
        # Rule-based signatures for common attacks
        self.attack_signatures = [
            "ignore previous instructions",
            "do anything now",
            "dan",
            "roleplay",
            "act as",
            "fake",
            "pretend",
            "hypothetical"
        ]

    def analyze(self, prompt: str) -> dict:
        """
        Analyzes the prompt for potential threats.
        """
        prompt_lower = prompt.lower()
        detected_threats = []
        
        for signature in self.attack_signatures:
            if signature in prompt_lower:
                detected_threats.append(signature)
        
        return {
            "is_safe": len(detected_threats) == 0,
            "threats": detected_threats
        }

    def filter(self, prompt: str) -> str:
        """
        Returns the prompt if safe, or None if blocked.
        """
        analysis = self.analyze(prompt)
        if analysis["is_safe"]:
            return prompt
        return None
