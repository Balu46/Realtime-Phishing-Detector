# Ingestion Module

## What it does
The `ingestion` module is responsible for feeding the entire system with a continuous stream of domains to analyze. Think of it as the "eyes and ears" of the application. It listens to the internet and pushes new domain names into a queue for processing.

## Components

### 1. `certstream_client.py` (CertstreamListener)
*   **Purpose:** Connects to the public Certificate Transparency (CT) log firehose (`wss://certstream.calidog.io/`).
*   **How it works:** It opens a WebSocket connection and waits for new SSL certificates to be issued anywhere in the world. When a certificate is issued, it extracts the domain name and adds it to the queue.

### 2. `urlscan_client.py` (UrlScanListener)
*   **Purpose:** Acts as a reliable fallback when the CertStream network is down.
*   **How it works:** It queries the `urlscan.io` API every 10 seconds to fetch a batch of up to 100 recently scanned domains (many of which are malicious). This provides a steady, guaranteed flow of real-world data.

### 3. `mock_certstream.py` (MockCertstreamListener)
*   **Purpose:** A testing simulator for local development or presentations.
*   **How it works:** Instead of connecting to the internet, it generates thousands of fake domain names internally (e.g., `test.example.com`). Very rarely, it intentionally generates a fake phishing domain (e.g., `paypal-login-secure-123.com`) to test if the rest of the system is working properly.
