
import numpy as np
from typing import List

class FederatedClient:
    """
    Simulates a client in a federated learning setup.
    Holds local data and performs local model updates.
    """
    def __init__(self, id: str, data_X: np.ndarray, data_y: np.ndarray):
        self.id = id
        self.data_X = data_X
        self.data_y = data_y

    def train_epoch(self, global_weights: np.ndarray, learning_rate: float = 0.01) -> np.ndarray:
        """
        Simulates one epoch of local training (using Gradient Descent).
        Returns the updated weights.
        """
        # For simplicity, assume linear regression: y = w * x
        # Loss = (y_pred - y)^2
        # Gradient = 2 * (y_pred - y) * x
        
        local_weights = global_weights.copy()
        
        # Batch gradient descent on local data
        predictions = self.data_X.dot(local_weights)
        errors = predictions - self.data_y
        
        # Gradient
        # X shape: (N, D), weights shape: (D,)
        gradient = self.data_X.T.dot(errors) / len(self.data_y)
        
        # Update
        local_weights -= learning_rate * gradient
        
        return local_weights

class FederatedServer:
    """
    Aggregates updates from clients (FedAvg).
    """
    def __init__(self):
        pass

    def aggregate(self, client_weights_list: List[np.ndarray]) -> np.ndarray:
        """
        Averages the list of weight vectors.
        Arguments:
            client_weights_list: List of numpy arrays (must have same shape).
        Returns:
            The averaged weight vector.
        """
        if not client_weights_list:
            raise ValueError("No weights to aggregate.")
            
        return np.mean(client_weights_list, axis=0)
