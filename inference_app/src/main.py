import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import time
import queue
import logging
import argparse
import csv
from datetime import datetime
from config import Config
from ingestion.certstream_client import CertstreamListener
from ingestion.mock_certstream import MockCertstreamListener
from ingestion.urlscan_client import UrlScanListener
from analysis.heuristics import HeuristicsAnalyzer
from shared.feature_extraction import FeatureExtractor
from ml.model import PhishingDetectorModel
from threat_intel.virustotal import VirusTotalClient
from threat_intel.google_safe_browsing import SafeBrowsingClient

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PhishingDetectorMain")

def main():
    parser = argparse.ArgumentParser(description="CT Logs Phishing Detection System")
    parser.add_argument("--mock", action="store_true", help="Run with simulated mock traffic instead of real CertStream")
    parser.add_argument("--urlscan", action="store_true", help="Run with real data from URLScan.io instead of CertStream")
    args = parser.parse_args()

    logger.info("Starting CT Logs Phishing Detection System...")
    
    # Check if API keys are available, warn if not
    if not Config.VT_API_KEY or Config.VT_API_KEY == "your_virustotal_api_key_here":
        logger.warning("VirusTotal API key is missing. VT checks will be skipped.")
    if not Config.GSB_API_KEY or Config.GSB_API_KEY == "your_google_safe_browsing_api_key_here":
        logger.warning("Google Safe Browsing API key is missing. GSB checks will be skipped.")

    # Initialize modules
    domain_queue = queue.Queue(maxsize=10000)
    
    if args.mock:
        listener = MockCertstreamListener(domain_queue)
    elif args.urlscan:
        listener = UrlScanListener(domain_queue)
    else:
        listener = CertstreamListener(domain_queue)
    
    logger.info(f"Target brands for protection: {Config.TARGET_BRANDS}")
    
    heuristics = HeuristicsAnalyzer(Config.TARGET_BRANDS)
    extractor = FeatureExtractor(Config.TARGET_BRANDS)
    ml_model = PhishingDetectorModel()
    
    vt_client = VirusTotalClient(Config.VT_API_KEY)
    gsb_client = SafeBrowsingClient(Config.GSB_API_KEY)
    
    # Start listening to CT logs
    listener.start()
    
    logger.info("Pipeline initialized. Listening for new domains...")
    logger.info("Press Ctrl+C to stop.")

    # Setup CSV logging
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))
    os.makedirs(results_dir, exist_ok=True)
    csv_filename = os.path.join(results_dir, "phishing_results.csv")
    
    file_exists = os.path.isfile(csv_filename)
    csv_file = open(csv_filename, "a", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    if not file_exists:
        csv_writer.writerow(["Timestamp", "Domain", "Is_Phishing_Heuristics", "Is_Phishing_ML", "VirusTotal_Result", "SafeBrowsing_Result"])

    processed_count = 0
    try:
        while True:
            try:
                # Block until a domain is available in the queue
                domain = domain_queue.get(timeout=1.0)
            except queue.Empty:
                continue
                
            processed_count += 1
            if processed_count % 100 == 0:
                logger.info(f"⚡ Otrzymano i przeanalizowano {processed_count} domen... Ostatnia widziana domena: {domain}")
                
            # Default state for CSV logging
            heuristics_match = False
            ml_match = False
            vt_res = None
            gsb_res = None
                
            # --- Phase 1: Heuristics & Typosquatting ---
            if heuristics.is_phishing_heuristic(domain):
                heuristics_match = True
                logger.warning(f"🚨 HEURISTIC MATCH: Suspicious domain found: {domain}")
                
                # --- Phase 2: ML Feature Extraction & Classification ---
                features = extractor.extract_features(domain)
                is_phishing_ml = ml_model.predict(features)
                
                if is_phishing_ml:
                    ml_match = True
                    logger.warning(f"🚨 ML MATCH: Model classified as phishing: {domain}")
                    logger.info(f"Features: {extractor.extract_features_dict(domain)}")
                    
                    # --- Phase 3: Threat Intelligence Validation ---
                    # Optional: Verify with VirusTotal or GSB if available
                    vt_res = vt_client.check_domain(domain)
                    if vt_res is True:
                        logger.critical(f"💀 CONFIRMED MALICIOUS on VirusTotal: {domain}")
                    elif vt_res is False:
                        logger.info(f"VirusTotal considers it safe (for now): {domain}")
                        
                    gsb_res = gsb_client.check_domain(domain)
                    if gsb_res is True:
                        logger.critical(f"💀 CONFIRMED MALICIOUS on Google Safe Browsing: {domain}")
            
            # Log every single domain to CSV
            timestamp = datetime.now().isoformat()
            csv_writer.writerow([timestamp, domain, heuristics_match, ml_match, vt_res, gsb_res])
            csv_file.flush() # Ensure it's saved to disk immediately
                    
            domain_queue.task_done()

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        listener.stop()
        csv_file.close()
        logger.info("System stopped.")

if __name__ == "__main__":
    main()
