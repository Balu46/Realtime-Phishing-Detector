import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class VirusTotalClient:
    """
    Client for interacting with the VirusTotal API to check domain reputation.
    """

    def __init__(self, api_key: str):
        """
        Initializes the VT client.

        Args:
            api_key (str): The VirusTotal API key.
        """
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.api_key
        }

    def check_domain(self, domain: str) -> Optional[bool]:
        """
        Checks if a domain is flagged as malicious on VirusTotal.

        Args:
            domain (str): The domain to check.

        Returns:
            Optional[bool]: True if malicious, False if safe, None on error or if no API key.
        """
        if not self.api_key or self.api_key == "your_virustotal_api_key_here":
            logger.debug(f"VT check skipped for {domain} (No API key configured)")
            return None

        url = f"{self.base_url}/domains/{domain}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            
            if malicious > 0 or suspicious > 0:
                return True
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking VirusTotal for {domain}: {e}")
            return None
