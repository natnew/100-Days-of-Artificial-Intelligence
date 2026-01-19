class BasicSanitizer:
    def __init__(self):
        self.blacklist = [
            "ignore previous instructions",
            "ignore execution instructions", 
            "system prompt",
            "secret key"
        ]

    def check(self, user_input: str) -> bool:
        """
        Returns True if input is safe, False if unsafe.
        """
        user_input_lower = user_input.lower()
        for phrase in self.blacklist:
            if phrase in user_input_lower:
                return False
        return True

    def sanitize(self, user_input: str) -> str:
        """
        Returns the input if safe, or a refusal message if unsafe.
        """
        if self.check(user_input):
            return user_input
        else:
            return "[BLOCKED] Input detected as potential prompt injection."
