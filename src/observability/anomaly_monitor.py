
import numpy as np
from collections import deque
from typing import Dict, Any

class RuntimeAnomalyMonitor:
    """
    Detects runtime anomalies (outliers) using a sliding window and Z-Score.
    Useful for monitoring latency, output length, or error rates.
    """
    def __init__(self, window_size: int = 50, z_threshold: float = 3.0):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.history = deque(maxlen=window_size)
    
    def update(self, value: float):
        """Add a new observation to the baseline."""
        self.history.append(value)
        
    def check_anomaly(self, value: float) -> Dict[str, Any]:
        """
        Check if 'value' is an anomaly compared to the CURRENT history.
        Does NOT add the value to history (call update() for that).
        This allows checking before committing.
        """
        if len(self.history) < 2:
            return {"is_anomaly": False, "z_score": 0.0, "mean": 0.0, "std": 0.0}
            
        data = np.array(self.history)
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            if value == mean:
                return {"is_anomaly": False, "z_score": 0.0, "mean": mean, "std": std}
            else:
                 # If std is 0 (all previous values identical), any deviation is theoretically infinite Z.
                 # We mark it as anomaly if it differs.
                 return {"is_anomaly": True, "z_score": 999.0, "mean": mean, "std": std}

        z_score = (value - mean) / std
        
        is_anomaly = abs(z_score) > self.z_threshold
        
        return {
            "is_anomaly": is_anomaly,
            "z_score": z_score,
            "mean": mean,
            "std": std
        }
