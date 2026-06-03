import unittest
import os
import sys

# Add the src directory to the python path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from analysis.heuristics import HeuristicsAnalyzer
from shared.feature_extraction import FeatureExtractor
from config import Config

class TestHeuristicsAndExtraction(unittest.TestCase):
    def setUp(self):
        self.target_brands = ['paypal', 'apple', 'google']
        self.heuristics = HeuristicsAnalyzer(self.target_brands)
        self.extractor = FeatureExtractor(self.target_brands)

    def test_phishing_heuristic(self):
        # Should flag typosquatting or brand usage
        self.assertTrue(self.heuristics.is_phishing_heuristic("paypal-login-secure.com"))
        self.assertTrue(self.heuristics.is_phishing_heuristic("apple-support-update.net"))
        self.assertTrue(self.heuristics.is_phishing_heuristic("goog1e.com"))
        
        # Should not flag unrelated domains
        self.assertFalse(self.heuristics.is_phishing_heuristic("example.com"))
        self.assertFalse(self.heuristics.is_phishing_heuristic("my-personal-blog.org"))

    def test_feature_extraction(self):
        # Safe domain features
        features_safe = self.extractor.extract_features_dict("example.com")
        self.assertGreaterEqual(features_safe['min_levenshtein'], 3.0)
        self.assertEqual(features_safe['unusual_chars_count'], 0)

        # Phishing domain features
        features_phish = self.extractor.extract_features_dict("paypal-verify-update-123.com")
        self.assertEqual(features_phish['min_levenshtein'], 0.0) # Contains 'paypal' exactly
        self.assertGreaterEqual(features_phish['unusual_chars_count'], 2.0) # Contains hyphens and numbers

if __name__ == '__main__':
    unittest.main()
