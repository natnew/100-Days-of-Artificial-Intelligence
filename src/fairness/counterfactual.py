
import re
from typing import List, Dict, Tuple

class CounterfactualGenerator:
    """
    Generates counterfactual text by swapping sensitive attributes (e.g., gender terms).
    """

    GENDER_PAIRS = {
        "he": "she", "she": "he",
        "him": "her", "her": "him",
        "his": "hers", "hers": "his",
        "man": "woman", "woman": "man",
        "male": "female", "female": "male",
        "boy": "girl", "girl": "boy",
        "father": "mother", "mother": "father",
        "brother": "sister", "sister": "brother",
        "actor": "actress", "actress": "actor",
        "king": "queen", "queen": "king"
    }

    def __init__(self):
        pass

    def generate_gender_counterfactuals(self, text: str) -> List[str]:
        """
        Generates a list of counterfactuals by identifying gendered terms and creating versions
        where they are swapped.
        
        Currently simple: swaps ALL occurrences to the opposite.
        Future improvements could do partial swaps or handle ambiguous grammar.
        """
        words = text.split()
        modified_words = []
        changed = False

        for word in words:
            # Handle punctuation roughly
            clean_word = re.sub(r'[^\w\s]', '', word).lower()
            
            if clean_word in self.GENDER_PAIRS:
                target = self.GENDER_PAIRS[clean_word]
                
                # Match casing
                if word[0].isupper():
                    target = target.capitalize()
                
                # Re-attach punctuation if any (simple check for trailing)
                if not word[-1].isalnum():
                    target += word[-1]
                
                modified_words.append(target)
                changed = True
            else:
                modified_words.append(word)
        
        if changed:
            return [" ".join(modified_words)]
        return []

    def evaluate_consistency(self, original_output: str, counterfactual_output: str) -> float:
        """
        Simple consistency score: 1.0 if identical, < 1.0 if different.
        For text generation, we might use string similarity.
        For binary classification (0/1), just 0 or 1.
        """
        if original_output == counterfactual_output:
            return 1.0
        return 0.0
