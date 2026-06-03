import os
import logging
import numpy as np
from typing import List
import joblib

logger = logging.getLogger(__name__)

class PhishingDetectorModel:
    """
    Machine Learning model for classifying domains as phishing or benign.
    Loads a pre-trained model (Random Forest / Scikit-learn or future PyTorch model).
    """

    def __init__(self, model_path: str = None):
        """Initializes the model by loading pre-trained weights."""
        if model_path is None:
            model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared', 'models', 'model_weights.pkl'))
            
        self.model_path = model_path
        self.is_trained = False
        self.model = None
        
        self._load_model()

    def _load_model(self) -> None:
        """Loads the pre-trained model from disk."""
        if os.path.exists(self.model_path):
            try:
                # Currently using joblib for scikit-learn models
                # For PyTorch, this would be: self.model.load_state_dict(torch.load(self.model_path))
                self.model = joblib.load(self.model_path)
                self.is_trained = True
                logger.info(f"Successfully loaded pre-trained model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model from {self.model_path}: {e}")
        else:
            logger.warning(f"Model file not found at {self.model_path}.")
            logger.warning("Please run `python src/ml/train.py` to train the model first.")

    def predict(self, features: List[float]) -> bool:
        """
        Predicts if a domain is phishing based on its features.

        Args:
            features (List[float]): Extracted features for the domain.

        Returns:
            bool: True if predicted as phishing, False otherwise.
        """
        if not self.is_trained or self.model is None:
            logger.warning("Model is not loaded/trained. Returning False (Benign) to avoid blocking.")
            return False
            
        # Reshape for single prediction
        X_pred = np.array(features).reshape(1, -1)
        
        # Scikit-learn prediction
        # For PyTorch, this would be: 
        # with torch.no_grad():
        #     prediction = self.model(torch.tensor(X_pred, dtype=torch.float32))
        #     return bool(prediction.item() > 0.5)
        
        prediction = self.model.predict(X_pred)
        
        return bool(prediction[0] == 1)
