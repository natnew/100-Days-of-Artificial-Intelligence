
import numpy as np
from collections import deque
from typing import List, Dict, Any

class ModelMonitor:
    """
    Tracks model performance over time.
    Detects drift if performance drops below a threshold.
    """
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.history_metrics = [] # List of {'batch': int, 'accuracy': float}
        self.metric_buffer = deque(maxlen=window_size)
    
    def update(self, y_true: np.ndarray, y_pred: np.ndarray, batch_id: int):
        """
        Log a new batch of predictions and ground truth.
        """
        # Calculate accuracy for this batch
        if len(y_true) == 0:
            return
            
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        batch_acc = np.mean(y_true == y_pred)
        
        self.history_metrics.append({
            'batch': batch_id,
            'accuracy': batch_acc
        })
        self.metric_buffer.append(batch_acc)

    def check_drift(self, threshold: float = 0.8) -> Dict[str, Any]:
        """
        Checks if the moving average accuracy is below threshold.
        """
        if len(self.metric_buffer) == 0:
             return {"drift_detected": False, "current_metric": 0.0}

        avg_metric = np.mean(self.metric_buffer)
        
        drift = avg_metric < threshold
        
        return {
            "drift_detected": drift,
            "current_metric": avg_metric,
            "threshold": threshold
        }

    def get_metrics_history(self) -> List[Dict[str, Any]]:
        return self.history_metrics
