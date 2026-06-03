import math
import re
from typing import List, Dict, Any
import Levenshtein

class FeatureExtractor:
    """
    Extracts numerical features from a domain name for Machine Learning classification.
    """

    def __init__(self, target_brands: List[str]):
        """
        Initializes the feature extractor.

        Args:
            target_brands (List[str]): List of brand names to calculate Levenshtein distance against.
        """
        self.target_brands = target_brands

    def _shannon_entropy(self, data: str) -> float:
        """
        Calculates the Shannon entropy of a string.

        Args:
            data (str): The input string.

        Returns:
            float: The entropy value.
        """
        if not data:
            return 0.0
        entropy = 0.0
        for x in set(data):
            p_x = float(data.count(x)) / len(data)
            entropy -= p_x * math.log(p_x, 2)
        return entropy

    def _min_levenshtein_distance(self, data: str) -> int:
        """
        Calculates the minimum Levenshtein distance from the domain to any of the target brands.

        Args:
            data (str): The domain string.

        Returns:
            int: The minimum distance.
        """
        if not self.target_brands:
            return 999
            
        distances = []
        # Check against parts of the domain to find the closest match
        parts = re.split(r'[\.\-]', data)
        for part in parts:
            if len(part) < 3:
                continue
            for brand in self.target_brands:
                dist = Levenshtein.distance(part, brand)
                distances.append(dist)
                
        # If no valid parts, compare whole domain to brands
        if not distances:
            for brand in self.target_brands:
                dist = Levenshtein.distance(data, brand)
                distances.append(dist)

        return min(distances) if distances else 999

    def _unusual_characters_count(self, data: str) -> int:
        """
        Counts the number of unusual characters (e.g., hyphens, numbers, special chars) in the domain.

        Args:
            data (str): The domain string.

        Returns:
            int: The count of unusual characters.
        """
        # Count non-alphabetic characters
        return sum(1 for char in data if not char.isalpha() and char != '.')

    def extract_features(self, domain: str) -> List[float]:
        """
        Extracts all features for a given domain to be fed into the ML model.

        Args:
            domain (str): The domain name.

        Returns:
            List[float]: A list containing [entropy, min_levenshtein, length, unusual_chars_count].
        """
        entropy = self._shannon_entropy(domain)
        min_lev = float(self._min_levenshtein_distance(domain))
        length = float(len(domain))
        unusual_chars = float(self._unusual_characters_count(domain))

        return [entropy, min_lev, length, unusual_chars]

    def extract_features_dict(self, domain: str) -> Dict[str, float]:
        """
        Extracts features and returns them as a dictionary (useful for logging/debugging).

        Args:
            domain (str): The domain name.

        Returns:
            Dict[str, float]: Feature dictionary.
        """
        return {
            "entropy": self._shannon_entropy(domain),
            "min_levenshtein": float(self._min_levenshtein_distance(domain)),
            "length": float(len(domain)),
            "unusual_chars_count": float(self._unusual_characters_count(domain))
        }
