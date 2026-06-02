import logging
import numpy as np
from typing import List
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

class PhishingDetectorModel:
    """
    Machine Learning model for classifying domains as phishing or benign.
    Uses a Random Forest Classifier based on extracted domain features.
    """

    def __init__(self):
        """Initializes the Random Forest model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self._dummy_train() # Train on some dummy data so it can predict immediately

    def _dummy_train(self) -> None:
        """
        Trains the model on a small synthetic dataset for demonstration purposes.
        In a real scenario, this would load a pre-trained model or train on a large dataset.
        Features: [entropy, min_levenshtein, length, unusual_chars_count]
        """
        logger.info("Training ML model on dummy dataset...")
        
        # X: Features, y: Labels (0 = Benign, 1 = Phishing)
        # Benign examples: low entropy, high levenshtein distance to brands, normal length, few unusual chars
        # Phishing examples: high entropy, low levenshtein distance, long length, many unusual chars
        X = np.array([
            [2.1, 15.0, 10.0, 0.0], # Benign (e.g. google.com - dist to paypal is high)
            [1.5, 12.0, 8.0, 0.0],  # Benign
            [2.8, 14.0, 15.0, 1.0], # Benign
            [4.5, 1.0, 25.0, 4.0],  # Phishing (e.g. pay-pal-update-security.com)
            [3.9, 0.0, 18.0, 3.0],  # Phishing (e.g. paypa1-login.com)
            [4.2, 2.0, 30.0, 5.0],  # Phishing
        ])
        y = np.array([0, 0, 0, 1, 1, 1])
        
        self.model.fit(X, y)
        self.is_trained = True
        logger.info("ML model training complete.")

    def predict(self, features: List[float]) -> bool:
        """
        Predicts if a domain is phishing based on its features.

        Args:
            features (List[float]): Extracted features for the domain.

        Returns:
            bool: True if predicted as phishing, False otherwise.
        """
        if not self.is_trained:
            logger.warning("Model is not trained. Returning False.")
            return False
            
        # Reshape for single prediction
        X_pred = np.array(features).reshape(1, -1)
        prediction = self.model.predict(X_pred)
        
        return bool(prediction[0] == 1)
