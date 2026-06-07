import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SafeBrowsingClient:
    """
    Client for interacting with the Google Safe Browsing API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the Safe Browsing client.

        Args:
            api_key (str): The Google Safe Browsing API key.
        """
        self.api_key = api_key
        self.url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.api_key}"

    def check_domain(self, domain: str) -> Optional[bool]:
        """
        Checks if a domain is flagged by Google Safe Browsing.

        Args:
            domain (str): The domain to check.

        Returns:
            Optional[bool]: True if malicious, False if safe, None on error or if no API key.
        """
        if not self.api_key or self.api_key == "your_google_safe_browsing_api_key_here":
            logger.debug(f"GSB check skipped for {domain} (No API key configured)")
            return None

        # Format required by Google Safe Browsing API
        payload = {
            "client": {
                "clientId": "ct-phishing-detector",
                "clientVersion": "1.0.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": f"http://{domain}"},
                    {"url": f"https://{domain}"}
                ]
            }
        }

        try:
            response = requests.post(self.url, json=payload, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # If there's a match, the "matches" key will exist
            if "matches" in data and len(data["matches"]) > 0:
                return True
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking Google Safe Browsing for {domain}")
            logger.debug(f"GSB Error details: {str(e).replace(self.api_key, '***')}")
            return None
