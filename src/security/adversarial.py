
import numpy as np
from typing import Callable

class AdversarialAttacker:
    """
    Simulates white-box adversarial attacks like FGSM.
    """
    
    def __init__(self):
        pass

    def fgsm_attack(self, image: np.ndarray, epsilon: float, data_grad: np.ndarray) -> np.ndarray:
        """
        Applies Fast Gradient Sign Method (FGSM).
        perturbed_image = image + epsilon * sign(data_grad)
        """
        # Collect the element-wise sign of the data gradient
        sign_data_grad = np.sign(data_grad)
        
        # Create the perturbed image by adjusting each pixel of the input image
        perturbed_image = image + epsilon * sign_data_grad
        
        # Adding clipping to maintain valid range might be needed depending on domain
        # But for raw math, we return it as is.
        # Ideally, we should also clip to [0,1] or [0,255] if it's an image.
        
        return perturbed_image

    def generate_adversarial_example(self, 
                                     model_predict_fn: Callable[[np.ndarray], np.ndarray],
                                     model_gradient_fn: Callable[[np.ndarray, int], np.ndarray],
                                     image: np.ndarray, 
                                     target_label: int, 
                                     epsilon: float = 0.1) -> np.ndarray:
        """
        Full workflow:
        1. Calculate gradient of loss w.r.t input image.
        2. Apply FGSM.
        """
        # In a real framework like PyTorch, we'd do a backward pass.
        # Here we rely on a provided gradient function simulation.
        data_grad = model_gradient_fn(image, target_label)
        
        perturbed_image = self.fgsm_attack(image, epsilon, data_grad)
        
        return perturbed_image
