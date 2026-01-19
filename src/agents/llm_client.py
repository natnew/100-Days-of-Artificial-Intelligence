import os
import logging
from typing import Optional

# Check for OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Check for Anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Check for Google/Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from .mock_llm import MockLLM

class LLMClient:
    """
    A unified client that acts as a gateway to multiple LLM providers (OpenAI, Anthropic, Gemini)
    or the internal MockLLM simulator.
    
    Configuration:
    - Set 'LLM_PROVIDER' to 'openai', 'anthropic', 'gemini', or 'mock'.
    - Set 'LLM_MODEL' to specify the model (e.g., 'gpt-5.2', 'claude-3-opus', 'gemini-1.5-pro').
    - ensure the corresponding API key is set (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY).
    """
    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "mock")).lower()
        self.model = os.getenv("LLM_MODEL")
        self.mock = MockLLM()
        self.client = None

        # --- OpenAI Setup ---
        if self.provider == "openai" or (self.provider == "mock" and os.getenv("OPENAI_API_KEY")):
            if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                try:
                    self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    self.provider = "openai" # Confirm provider switch if auto-detected
                    if not self.model: self.model = "gpt-5.2-turbo" # Default to latest requested
                except Exception as e:
                    logging.warning(f"Failed to initialize OpenAI client: {e}")

        # --- Anthropic Setup ---
        elif self.provider == "anthropic":
            if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
                try:
                    self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                    if not self.model: self.model = "claude-3-5-sonnet-20240620"
                except Exception as e:
                    logging.warning(f"Failed to initialize Anthropic client: {e}")

        # --- Gemini Setup ---
        elif self.provider == "gemini":
            if GEMINI_AVAILABLE and os.getenv("GOOGLE_API_KEY"):
                try:
                    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                    self.client = genai
                    if not self.model: self.model = "gemini-1.5-pro"
                except Exception as e:
                    logging.warning(f"Failed to initialize Gemini client: {e}")

        if self.provider != "mock" and self.client is None:
             logging.warning(f"Provider '{self.provider}' requested but client failed to initialize. Falling back to Mock.")
             self.provider = "mock"

    def generate(self, prompt: str) -> str:
        """
        Generates a response from the configured provider.
        """
        if self.provider == "openai" and self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI Error: {e}"

        elif self.provider == "anthropic" and self.client:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                 return f"Anthropic Error: {e}"

        elif self.provider == "gemini" and self.client:
            try:
                model = self.client.GenerativeModel(self.model)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                 return f"Gemini Error: {e}"

        # Default / Fallback
        return self.mock.generate(prompt)
