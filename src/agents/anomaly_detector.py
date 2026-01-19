import math
from collections import Counter

class AnomalyDetector:
    """
    Detects anomalous inputs such as gibberish, repetition, or extreme length.
    """
    def __init__(self, max_length=1000, entropy_threshold=4.5):
        self.max_length = max_length
        self.entropy_threshold = entropy_threshold

    def calculate_entropy(self, text: str) -> float:
        """
        Calculates Shannon entropy of the text.
        """
        if not text:
            return 0.0
        
        counter = Counter(text)
        length = len(text)
        entropy = 0.0
        
        for count in counter.values():
            prob = count / length
            entropy -= prob * math.log2(prob)
            
        return entropy

    def scan(self, text: str) -> dict:
        """
        Scans the text for anomalies.
        """
        anomalies = []
        
        # 1. Length Check
        if len(text) > self.max_length:
            anomalies.append(f"Length Exceeded ({len(text)} > {self.max_length})")
            
        # 2. Entropy Check (Gibberish detection)
        entropy = self.calculate_entropy(text)
        # Random gibberish often has high entropy (using many unique chars uniformally)
        # But extremely repetitive text has very low entropy.
        # For this lab, we'll flag High Entropy as "Gibberish" and Low as "Repetitive"
        
        if entropy > self.entropy_threshold:
             anomalies.append(f"High Entropy/Gibberish ({entropy:.2f})")
        
        # 3. Repetition Check (Simple approximation via low entropy or repeating patterns)
        # We can use a simple ratio of unique chars to total length
        unique_ratio = len(set(text)) / len(text) if text else 1
        if unique_ratio < 0.05 and len(text) > 50:
             anomalies.append(f"Excessive Repetition (Unique Ratio: {unique_ratio:.2f})")

        return {
            "is_anomaly": len(anomalies) > 0,
            "anomalies": anomalies,
            "metrics": {
                "length": len(text),
                "entropy": entropy,
                "unique_ratio": unique_ratio
            }
        }
