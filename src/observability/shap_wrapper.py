
import numpy as np
import warnings

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("SHAP library not found. Please install it using `pip install shap`.")

class ShapExplainer:
    """
    A simplified wrapper for generating SHAP explanations.
    """
    def __init__(self):
        self.explainer = None

    def fit(self, model, X_background):
        """
        Initialize the SHAP explainer.
        
        Args:
            model: The trained model (e.g., sklearn model, xgboost).
            X_background: Background dataset for KernelExplainer (representative sample).
        """
        if not SHAP_AVAILABLE:
            print("SHAP not available.")
            return

        # Generic approach: use KernelExplainer for flexibility
        # In production, specific explainers (TreeExplainer, DeepExplainer) are faster.
        # Here we assume model.predict_proba or model.predict exists.
        
        # Determine if model has predict_proba (classifier) or predict (regressor)
        if hasattr(model, 'predict_proba'):
            model_fn = model.predict_proba
        else:
            model_fn = model.predict
            
        self.explainer = shap.KernelExplainer(model_fn, X_background)

    def explain_local(self, X_instance):
        """
        Explain a single instance or a small batch.
        
        Args:
            X_instance: Data to explain.
            
        Returns:
            shap_values: The calculated SHAP values.
        """
        if self.explainer is None:
            raise ValueError("Explainer not initialized. Call fit() first.")
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            shap_values = self.explainer.shap_values(X_instance, nsamples=100)
            
        return shap_values

    def plot_summary(self, shap_values, X):
        """
        Plots the summary plot.
        """
        if not SHAP_AVAILABLE:
            return
            
        shap.summary_plot(shap_values, X)
