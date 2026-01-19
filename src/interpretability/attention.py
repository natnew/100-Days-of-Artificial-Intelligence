
from typing import List, Dict, Tuple
import re

class SimpleAttention:
    """
    Mock Feature Attribution.
    Assigns 'importance scores' to input tokens based on their presence/relevance to the output.
    """
    
    def tokenize(self, text: str) -> List[str]:
        return text.split()

    def calculate_attribution(self, input_text: str, output_text: str) -> List[Tuple[str, float]]:
        """
        Returns a list of (token, score).
        If an input token appears in the output (or is very similar), it gets a high score.
        """
        input_tokens = self.tokenize(input_text)
        output_tokens = set(self.tokenize(output_text.lower()))
        
        attributions = []
        for token in input_tokens:
            clean_token = re.sub(r'[^\w\s]', '', token).lower()
            score = 0.1 # Base importance
            
            # Direct match
            if clean_token in output_tokens:
                score = 1.0
            # Contextual importance (mock: 'not', 'never' are always important)
            elif clean_token in ["not", "never", "always", "must"]:
                score = 0.8
            # Topic words (mock)
            elif clean_token in ["safety", "kill", "bomb", "love"]:
                score = 0.5
                
            attributions.append((token, score))
            
        return attributions

    def visualize(self, attributions: List[Tuple[str, float]]):
        """
        Simple console visualization.
        """
        print("Feature Attribution Map:")
        for token, score in attributions:
            bar = "#" * int(score * 10)
            print(f"{token.ljust(15)} | {score:.2f} {bar}")
