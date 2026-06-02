import time
import logging
from config import Config
from analysis.heuristics import HeuristicsAnalyzer
from analysis.feature_extraction import FeatureExtractor
from ml.model import PhishingDetectorModel

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TestPipeline")

def run_test():
    logger.info("Initializing modules for testing...")
    heuristics = HeuristicsAnalyzer(Config.TARGET_BRANDS)
    extractor = FeatureExtractor(Config.TARGET_BRANDS)
    ml_model = PhishingDetectorModel()

    # A mix of safe and phishing domains
    test_domains = [
        "example.com",
        "my-personal-blog.org",
        "paypal-login-security-update.com", # Should trigger heuristics and ML
        "googIe-support.com", # Typosquatting
        "amazon-shopping.net"
    ]

    logger.info("Starting test simulation...")
    
    for domain in test_domains:
        time.sleep(1)
        logger.info(f"--- Złapano nową domenę: {domain} ---")
        
        # Phase 1: Heuristics
        if heuristics.is_phishing_heuristic(domain):
            logger.warning(f"🚨 HEURISTIC MATCH: Suspicious domain found: {domain}")
            
            # Phase 2: ML
            features = extractor.extract_features(domain)
            is_phishing_ml = ml_model.predict(features)
            
            if is_phishing_ml:
                logger.warning(f"🚨 ML MATCH: Model classified as phishing: {domain}")
                logger.info(f"Features: {extractor.extract_features_dict(domain)}")
                logger.critical(f"💀 W normalnym trybie teraz poszłoby zapytanie do VirusTotal dla: {domain}")
        else:
            logger.info(f"✅ Domena {domain} jest bezpieczna, ignoruję.")
            
    logger.info("Test zakończony.")

if __name__ == "__main__":
    run_test()
