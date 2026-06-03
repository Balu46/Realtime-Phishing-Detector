import threading
import queue
import logging
import time
import random

logger = logging.getLogger(__name__)

class MockCertstreamListener:
    """
    A fallback listener that simulates the CertStream firehose.
    Useful when the real public CertStream servers are down or blocked.
    Generates a stream of realistic domains at a high rate.
    """

    def __init__(self, domain_queue: queue.Queue):
        self.domain_queue = domain_queue
        self._stop_event = threading.Event()
        self._thread = None
        
        # Base realistic domains
        self.base_domains = [
            "google.com", "facebook.com", "example.org", "test.net", "university.edu",
            "shop-online.com", "my-personal-blog.info", "aws.amazon.com", "github.io",
            "news-portal.com", "tech-forum.org", "local-business.net"
        ]
        
        # Phishing templates to occasionally inject
        self.phishing_templates = [
            "paypal-login-secure-{}.com",
            "apple-id-verification-{}.com",
            "security-update-microsoft-{}.net",
            "facebook-support-ticket-{}.com",
            "bankofamerica-alert-{}.org"
        ]

    def start(self) -> None:
        logger.info("Starting MOCK CertstreamListener (Simulation Mode)...")
        
        def generate_stream():
            logger.info("Connection established to MOCK CertStream! Listening for events...")
            counter = 0
            
            while not self._stop_event.is_set():
                # Simulate receiving a batch of domains
                batch_size = random.randint(10, 50)
                
                for _ in range(batch_size):
                    # 99.5% chance of normal domain, 0.5% chance of phishing domain
                    if random.random() > 0.005:
                        # Generate random normal looking domain
                        prefix = random.choice(["www.", "api.", "dev.", "test.", "app.", ""])
                        base = random.choice(self.base_domains)
                        suffix = random.randint(100, 9999)
                        domain = f"{prefix}{base.split('.')[0]}-{suffix}.{base.split('.')[1]}"
                    else:
                        # Inject a phishing domain!
                        template = random.choice(self.phishing_templates)
                        domain = template.format(random.randint(1000, 9999))
                        
                    self.domain_queue.put(domain)
                    counter += 1
                
                # Simulate network delay between certificate batches (like real certstream)
                time.sleep(random.uniform(0.5, 1.5))

        self._thread = threading.Thread(target=generate_stream, daemon=True)
        self._thread.start()
        logger.info("MOCK CertstreamListener started in background thread.")

    def stop(self) -> None:
        logger.info("Stopping MOCK CertstreamListener...")
        self._stop_event.set()
