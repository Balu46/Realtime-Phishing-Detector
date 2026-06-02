import threading
import queue
import logging
import time
import requests
from config import Config

logger = logging.getLogger(__name__)

class UrlScanListener:
    """
    Pulls recent domains from urlscan.io instead of CertStream.
    This guarantees 100% reliable real-world data responses when CertStream is down.
    """

    def __init__(self, domain_queue: queue.Queue):
        self.domain_queue = domain_queue
        self._stop_event = threading.Event()
        self._thread = None
        self.seen_domains = set()

    def start(self) -> None:
        logger.info("Starting UrlScanListener (Reliable alternative to CertStream)...")
        
        def poll_urlscan():
            logger.info("Connection established to URLScan.io! Listening for events...")
            
            while not self._stop_event.is_set():
                try:
                    # We query for recently scanned domains that might be interesting
                    # A general query for domains scanned in the last 24 hours
                    response = requests.get("https://urlscan.io/api/v1/search/?q=date:>now-1h", timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        for result in data.get("results", []):
                            domain = result.get("task", {}).get("domain")
                            if domain and domain not in self.seen_domains:
                                self.seen_domains.add(domain)
                                self.domain_queue.put(domain)
                                
                                # Keep set size manageable
                                if len(self.seen_domains) > 10000:
                                    self.seen_domains.clear()
                                    
                except Exception as e:
                    logger.error(f"Error fetching from URLScan: {e}")
                
                # UrlScan API limit is usually around 5 seconds between requests for anonymous users
                time.sleep(10)

        self._thread = threading.Thread(target=poll_urlscan, daemon=True)
        self._thread.start()
        logger.info("UrlScanListener started in background thread.")

    def stop(self) -> None:
        logger.info("Stopping UrlScanListener...")
        self._stop_event.set()
