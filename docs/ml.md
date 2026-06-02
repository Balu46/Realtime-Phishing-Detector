# Machine Learning Module

## What it does
The `ml` module provides artificial intelligence capabilities to the system. Instead of relying solely on hardcoded rules (like the heuristics module), it uses a trained algorithm to recognize complex patterns that might indicate a phishing attempt.

## Components

### `model.py` (PhishingDetectorModel)
*   **Purpose:** Classifies a domain as either "safe" (`False`) or "phishing" (`True`) based on its numerical features.
*   **Algorithm:** It uses a `RandomForestClassifier` from the `scikit-learn` library. A Random Forest is an ensemble learning method that creates many decision trees and merges them together to get a more accurate and stable prediction.
*   **Training Data:** Upon startup, the model automatically trains itself on a small, dummy dataset composed of known safe patterns and known phishing patterns. (Note: In a production environment, this would be replaced by a pre-trained model loaded from a disk file, trained on millions of real domains).
*   **How it works:** When the `predict()` function is called, it receives a dictionary of features (like entropy, length, unusual characters) calculated by the `analysis` module. The Random Forest evaluates these numbers and makes a final binary decision.
