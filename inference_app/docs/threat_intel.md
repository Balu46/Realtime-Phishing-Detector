# Threat Intelligence Module

## What it does
The `threat_intel` module acts as the final verification authority. When our local Heuristics and Machine Learning modules suspect a domain is dangerous, this module reaches out to global cybersecurity databases to check if the domain is already known to be malicious by experts.

## Components

### 1. `virustotal.py` (VirusTotalClient)
*   **Purpose:** Queries the VirusTotal API (a service owned by Google Chronicle).
*   **How it works:** It sends the suspicious domain name to VirusTotal. VirusTotal checks the domain against dozens of different antivirus engines and website scanners. If a significant number of security vendors flag the domain as malicious, the client returns `True` (Confirmed Malicious).

### 2. `google_safe_browsing.py` (SafeBrowsingClient)
*   **Purpose:** Queries the Google Safe Browsing API.
*   **How it works:** It asks Google's massive threat database if the specific domain is currently listed on their official blacklist for malware, phishing, or unwanted software. If Google says yes, the client returns `True` (Confirmed Malicious).

*Note: Both clients require valid API keys stored in the `.env` file to function. If keys are missing, the system will gracefully skip this validation phase.*
