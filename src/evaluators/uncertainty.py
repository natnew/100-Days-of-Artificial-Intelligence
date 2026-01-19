import random

class ConfidenceSimulator:
    """
    Simulates model responses with attached confidence scores.
    """
    def predict(self, input_text: str) -> dict:
        """
        Returns a dict with 'text' and 'confidence' (0.0 to 1.0).
        """
        # Mock logic:
        # Long inputs -> Higher uncertainty (random simulation)
        # Specific keywords -> High confidence
        
        input_lower = input_text.lower()
        
        if "capital" in input_lower or "2+2" in input_lower:
            conf = 0.99
            text = "I am certain of this."
        elif "meaning of life" in input_lower:
            conf = 0.42
            text = "It might be 42, but I'm unsure."
        else:
            # Random confidence between 0.5 and 0.9
            conf = round(random.uniform(0.5, 0.9), 2)
            text = "This is a generated response."
            
        return {
            "text": text,
            "confidence": conf
        }

class UncertaintyMetrics:
    def __init__(self):
        pass

    def is_reliable(self, confidence: float, threshold: float = 0.75) -> bool:
        return confidence >= threshold
    
    def calibrate(self, predictions: list[dict]) -> dict:
        """
        Calculates simple calibration metrics.
        predictions: list of dicts with 'confidence' and 'correct' (bool)
        """
        if not predictions:
            return {"ece": 0.0}
            
        # Mock Expected Calibration Error (ECE) calculation
        # Group metrics into bins
        bins = {i: [] for i in range(10)} # 0-0.1, 0.1-0.2, etc.
        
        for p in predictions:
            conf = p['confidence']
            bin_idx = min(int(conf * 10), 9)
            bins[bin_idx].append(p)
            
        ece = 0.0
        total = len(predictions)
        
        for bin_idx, items in bins.items():
            if not items:
                continue
            
            avg_conf = sum(i['confidence'] for i in items) / len(items)
            accuracy = sum(1 for i in items if i['correct']) / len(items)
            
            ece += (len(items) / total) * abs(accuracy - avg_conf)
            
        return {"ece": round(ece, 4)}
