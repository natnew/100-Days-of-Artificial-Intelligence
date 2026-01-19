
from typing import List, Tuple, Dict
import math

class DataSanitizer:
    """
    Detects potential data poisoning attacks.
    Strategies:
    1. Label Flip Detection (Mock influence check)
    2. Outlier Detection (Feature statistics)
    """
    
    def __init__(self):
        self.feature_stats: Dict[str, Tuple[float, float]] = {} # mean, std dev

    def fit_stats(self, legitimate_data: List[str]):
        """
        Learns the 'normal' distribution of data characteristics (e.g. length, unique words).
        """
        lengths = [len(x) for x in legitimate_data]
        if not lengths:
            return
            
        mean_l = sum(lengths) / len(lengths)
        variance = sum((l - mean_l) ** 2 for l in lengths) / len(lengths)
        std_l = math.sqrt(variance)
        
        self.feature_stats['length'] = (mean_l, std_l)

    def is_poison(self, text: str, label: str) -> bool:
        """
        Checks if a data point looks malicious.
        """
        # 1. Outlier Check
        if 'length' in self.feature_stats:
            mean, std = self.feature_stats['length']
            # If text is absurdly long or short (> 3 sigma)
            if abs(len(text) - mean) > 3 * std:
                return True
        
        # 2. Keyword Poisoning (Backdoor trigger components)
        # Often poisoning inserts rare tokens.
        rare_triggers = ["nonsensestring", "triggerword123", "sudo_mode"]
        for trigger in rare_triggers:
            if trigger in text:
                return True
                
        return False

class TrainingGuard:
    """
    Simulates a secure training loop that filters data.
    """
    def __init__(self, sanitizer: DataSanitizer):
        self.sanitizer = sanitizer
        self.clean_data = []
        self.quarantine = []

    def ingest_batch(self, batch: List[Tuple[str, str]]):
        for text, label in batch:
            if self.sanitizer.is_poison(text, label):
                print(f"POISON DETECTED: Discarding '{text[:20]}...'")
                self.quarantine.append((text, label))
            else:
                self.clean_data.append((text, label))
