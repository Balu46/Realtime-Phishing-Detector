# Analysis Module

## What it does
The `analysis` module contains the core logic for inspecting a domain name. Its job is to quickly determine if a domain looks suspicious before passing it to heavier Machine Learning algorithms.

## Components

### 1. `heuristics.py` (HeuristicsAnalyzer)
*   **Purpose:** Rapidly filters out obvious phishing attempts using static rules and typosquatting detection.
*   **How it works:** 
    *   **Typosquatting Grid:** When initialized, it takes a list of protected brands (like `paypal`, `apple`) and generates thousands of variations (e.g., `paypa1`, `appIe`, `ppaypal`). 
    *   **Keywords:** It checks if the domain contains suspicious words commonly used by hackers (e.g., `login`, `secure`, `verify`).
    *   **Matching:** If an incoming domain contains a generated typo or a suspicious keyword combined with a brand name, it immediately triggers a warning and forwards the domain for deeper ML inspection.

### 2. `feature_extraction.py` (FeatureExtractor)
*   **Purpose:** Converts a domain name (text) into mathematical numbers (features) that a Machine Learning model can understand.
*   **How it works:** It calculates several key metrics:
    *   `entropy`: Measures how "random" a string is. High entropy often means an auto-generated, malicious domain.
    *   `min_levenshtein`: Calculates the mathematical distance (how many edits are needed) between the domain and our protected brands.
    *   `length`: The total length of the domain.
    *   `unusual_chars_count`: Counts the number of hyphens (`-`) or numbers (`0-9`), which are frequently abused by phishers to make domains look official (e.g., `paypal-update-2024.com`).
