import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ml.model import PhishingDetectorModel
from analysis.feature_extraction import FeatureExtractor

class TestMLModel(unittest.TestCase):
    def setUp(self):
        self.model = PhishingDetectorModel()
        self.extractor = FeatureExtractor(['paypal', 'apple'])

    def test_model_prediction_safe(self):
        # A normal domain should be classified as safe (False)
        features = self.extractor.extract_features("example.com")
        prediction = self.model.predict(features)
        self.assertFalse(prediction)

    def test_model_prediction_phishing(self):
        # A highly suspicious domain should be classified as phishing (True)
        features = self.extractor.extract_features("paypal-verify-update-account-123.com")
        prediction = self.model.predict(features)
        self.assertTrue(prediction)

if __name__ == '__main__':
    unittest.main()
