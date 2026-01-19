
import numpy as np

class LaplaceMechanism:
    """
    Implements the Laplace Mechanism for Differential Privacy.
    Adds noise drawn from a Laplace distribution to the output of a query.
    """
    def __init__(self):
        pass

    def add_noise(self, value: float, sensitivity: float, epsilon: float) -> float:
        """
        Adds Laplace noise to the value.
        
        Args:
            value: The true answer to the query.
            sensitivity: The maximum change in the query's result if one individual is changed.
                         (e.g., for a count query, sensitivity is 1).
            epsilon: The privacy budget. Smaller epsilon -> more privacy (more noise).
        
        Returns:
            Noisy value.
        """
        # Scale of Laplace distribution = sensitivity / epsilon
        scale = sensitivity / epsilon
        
        # Draw noise
        noise = np.random.laplace(0, scale)
        
        return value + noise
