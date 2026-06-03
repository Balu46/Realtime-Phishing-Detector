import threading
import queue
import logging
import certstream

logger = logging.getLogger(__name__)

class CertstreamListener:
    """
    Listens to the certstream in real-time and pushes extracted domains to a thread-safe queue.
    Runs asynchronously in a background thread.
    """

    def __init__(self, domain_queue: queue.Queue):
        """
        Initializes the CertstreamListener.

        Args:
            domain_queue (queue.Queue): A thread-safe queue to push observed domains.
        """
        self.domain_queue = domain_queue
        self._stop_event = threading.Event()
        self._thread = None

    def _callback(self, message: dict, context) -> None:
        """
        Callback function executed on every new CT log event.
        Extracts domains from the event and pushes them to the queue.

        Args:
            message (dict): The event data payload.
            context: The certstream context.
        """
        if self._stop_event.is_set():
            return

        if message.get("message_type") == "heartbeat":
            return

        if message.get("message_type") == "certificate_update":
            all_domains = message["data"]["leaf_cert"]["all_domains"]
            for domain in all_domains:
                # Basic normalization: lowercasing and stripping wildcard prefixes
                clean_domain = domain.lower().strip()
                if clean_domain.startswith("*."):
                    clean_domain = clean_domain[2:]
                
                self.domain_queue.put(clean_domain)

    def start(self) -> None:
        """Starts the certstream listener in a background thread."""
        logger.info("Starting CertstreamListener...")
        
        def run_certstream():
            certstream.listen_for_events(self._callback, url='wss://certstream.calidog.io/')

        self._thread = threading.Thread(target=run_certstream, daemon=True)
        self._thread.start()
        logger.info("CertstreamListener started in background thread.")

    def stop(self) -> None:
        """Signals the listener to stop processing new events."""
        logger.info("Stopping CertstreamListener...")
        self._stop_event.set()
