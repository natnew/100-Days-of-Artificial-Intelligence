import numpy as np
from typing import List, Dict

class AttentionVisualizer:
    """
    Visualizes and analyzes model attention checks.
    """
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.attention_maps = {} # (layer, head) -> matrix

    def add_attention(self, layer: int, head: int, matrix: np.ndarray):
        """
        Adds an attention matrix for a specific layer and head.
        Matrix shape should be (len(tokens), len(tokens)).
        """
        if matrix.shape != (len(self.tokens), len(self.tokens)):
            raise ValueError(f"Matrix shape {matrix.shape} does not match tokens length {len(self.tokens)}")
        self.attention_maps[(layer, head)] = matrix

    def get_strongest_focus(self, token_index: int, layer: int, head: int) -> Dict:
        """
        Returns the token that input[token_index] attends to the most.
        """
        if (layer, head) not in self.attention_maps:
            raise KeyError(f"No attention map for L{layer} H{head}")
        
        matrix = self.attention_maps[(layer, head)]
        
        # Attention from token_index to all previous tokens
        # row = token_index, columns = attended_tokens
        weights = matrix[token_index]
        
        # Find max weight index
        max_idx = np.argmax(weights)
        
        return {
            "source_token": self.tokens[token_index],
            "focused_token": self.tokens[max_idx],
            "weight": float(weights[max_idx]),
            "focused_index": int(max_idx)
        }
