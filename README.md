# CT Logs Phishing Detection System

## Overview

This project is an advanced, modular Python system designed to detect phishing domains in real-time by analyzing Certificate Transparency (CT) logs. It leverages heuristics, typosquatting generation, Machine Learning, and Threat Intelligence APIs to identify malicious domains mimicking targeted brands.

## Architecture & Modules

The system is built upon a robust, object-oriented architecture consisting of several specialized modules:

### 1. Data Ingestion (`ingestion/`)
This module is responsible for fetching a continuous stream of newly registered domains. It operates asynchronously to prevent blocking the main pipeline.
*   **`CertstreamListener`**: Connects to the public `certstream.calidog.io` WebSocket to receive a live firehose of global SSL certificates.
*   **`UrlScanListener`**: A fallback module that polls the URLScan.io API for recently scanned domains, ensuring a reliable data stream when CertStream is experiencing outages.
*   **`MockCertstreamListener`**: A simulator used for testing and demonstration. It generates realistic domain traffic and injects artificial phishing attempts to verify the pipeline's effectiveness.

### 2. Heuristics & Typosquatting (`analysis/heuristics.py`)
This component acts as the first line of defense. It initializes by generating thousands of potential typosquatting variants (e.g., character omission, repetition, transposition) for the defined target brands (like PayPal, Google, Amazon) using the logic inspired by `dnstwist`. Incoming domains are rapidly matched against this generated grid and a set of suspicious keywords (e.g., 'login', 'secure', 'update').

### 3. Feature Extraction & Machine Learning (`analysis/feature_extraction.py` & `ml/model.py`)
When a domain triggers the heuristics module, it is passed to the ML pipeline to reduce false positives.
*   **`FeatureExtractor`**: Calculates mathematical characteristics of the domain string, including Shannon Entropy (detecting random DGA-like strings), minimum Levenshtein distance to target brands, total length, and the count of unusual characters (like hyphens or numbers).
*   **`PhishingDetectorModel`**: A Machine Learning model (Random Forest Classifier via `scikit-learn`) trained on these features. It classifies the domain as either benign or malicious based on the extracted numerical profile.

### 4. Threat Intelligence Validation (`threat_intel/`)
If the ML model flags a domain as phishing, the system attempts to definitively confirm its malicious nature by querying external cybersecurity authorities.
*   **`VirusTotalClient`**: Queries the VirusTotal API to check if the domain has been flagged by global security vendors.
*   **`SafeBrowsingClient`**: Queries the Google Safe Browsing API to determine if the domain is currently blacklisted as a deceptive site.

### 5. Logging & Archiving (`main.py`)
All processed domains, along with their detection status across all three phases (Heuristics, ML, and Threat Intel), are permanently archived in a local `phishing_results.csv` file. This allows for historical analysis, reporting, and auditing.

---

## Configuration

The system requires API keys for Threat Intelligence validation. These are loaded securely via a `.env` file.

1.  Copy `.env.example` to `.env`.
2.  Add your `VT_API_KEY` (VirusTotal) and `GSB_API_KEY` (Google Safe Browsing).
3.  Target brands are configured in `config.py`.

## Usage

Start the main pipeline using the standard command:
```bash
python main.py
```

### Alternative Data Sources
If the primary CertStream network is down, you can use built-in alternatives:

*   **URLScan API (Real data fallback)**:
    ```bash
    python main.py --urlscan
    ```
*   **Mock Simulator (For testing and demonstrations)**:
    ```bash
    python main.py --mock
    ```

## Requirements
*   Python 3.8+
*   Dependencies listed in `requirements.txt` (install via `pip install -r requirements.txt`)
