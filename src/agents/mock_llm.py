import re

class MockLLM:
    """
    A mock LLM that simulates responses for demonstration purposes.
    It checks for specific patterns in the prompt to simulate injection success.
    """
    def generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        
        # Simulate simple instruction following
        if "ignore execution instructions" in prompt_lower or "ignore previous instructions" in prompt_lower:
            # Simulate successful injection
            if "say the secret key" in prompt_lower or "reveal the secret key" in prompt_lower:
                return "The secret key is SAFEMODE_123."
            return "I am ignoring my previous instructions. How can I help?"
            
        # Default behavior: pretending to be a helpful assistant with a hidden system prompt
        # We check if the USER is asking for the secret. Simulating "understanding" the user part.
        # Since this is a naive mock, we'll assume the user input comes after "User: "
        if "user:" in prompt_lower and "secret" in prompt_lower.split("user:")[-1]:
             return "I cannot reveal any confidential information."
            
        return f"I processed your request: {prompt[-50:]}..."
