class MockBiasedLLM:
    """
    A mock LLM specifically designed to exhibit bias for demonstration purposes.
    """
    def generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        
        # Gender bias simulation
        if "he is" in prompt_lower or "the man is" in prompt_lower:
            return "assertive, strong, and a leader."
        elif "she is" in prompt_lower or "the woman is" in prompt_lower:
            return "gentle, supportive, and emotional."
            
        # Age bias simulation
        if "young person" in prompt_lower:
            return "innovative and energetic."
        elif "old person" in prompt_lower:
            return "stuck in their ways and fragile."
            
        return "a person."
