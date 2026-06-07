import os
import sys
import logging
import argparse
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'models', 'model_weights.pkl'))

def load_dummy_data():
    logger.info("Loading DUMMY dataset...")
    # Features: [entropy, min_levenshtein, length, unusual_chars_count]
    X = np.array([
        [2.1, 15.0, 10.0, 0.0], # Benign (e.g. google.com - dist to paypal is high)
        [1.5, 12.0, 8.0, 0.0],  # Benign
        [2.8, 14.0, 15.0, 1.0], # Benign
        [4.5, 1.0, 25.0, 4.0],  # Phishing (e.g. pay-pal-update-security.com)
        [3.9, 0.0, 18.0, 3.0],  # Phishing (e.g. paypa1-login.com)
        [4.2, 2.0, 30.0, 5.0],  # Phishing
    ])
    y = np.array([0, 0, 0, 1, 1, 1])
    return X, y

def load_public_datasets():
    import requests
    import zipfile
    import io
    from urllib.parse import urlparse
    from shared.feature_extraction import FeatureExtractor
    
    from inference_app.src.config import Config
    
    logger.info("Downloading public datasets (OpenPhish for malicious, Tranco for benign)...")
    
    target_brands = Config.TARGET_BRANDS
    extractor = FeatureExtractor(target_brands)
    
    X = []
    y = []
    
    # 1. OpenPhish (Malicious)
    try:
        logger.info("Downloading OpenPhish feed...")
        r = requests.get('https://openphish.com/feed.txt', timeout=10)
        urls = r.text.strip().split('\n')
        domains = set()
        for url in urls:
            try:
                domain = urlparse(url).netloc
                if domain:
                    domains.add(domain)
            except:
                pass
                
        logger.info(f"Extracted {len(domains)} malicious domains from OpenPhish.")
        for domain in domains:
            X.append(extractor.extract_features(domain))
            y.append(1) # 1 = Phishing
    except Exception as e:
        logger.error(f"Failed to download OpenPhish: {e}")

    # 2. Tranco (Benign)
    try:
        logger.info("Downloading Tranco Top 1M list (this might take a moment)...")
        # Downloading a recent Tranco list
        r = requests.get('https://tranco-list.eu/top-1m.csv.zip', timeout=30)
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            # Usually there is only one csv file inside
            csv_filename = z.namelist()[0]
            with z.open(csv_filename) as f:
                # Read only the first N lines to balance the dataset
                n_benign_to_read = max(len(X) * 2, 1000) # get at least 1000, or 2x the phishing samples
                logger.info(f"Extracting top {n_benign_to_read} benign domains from Tranco...")
                count = 0
                for line in f:
                    if count >= n_benign_to_read:
                        break
                    # Format is usually "rank,domain"
                    parts = line.decode('utf-8').strip().split(',')
                    if len(parts) >= 2:
                        domain = parts[1]
                        X.append(extractor.extract_features(domain))
                        y.append(0) # 0 = Benign
                        count += 1
                        
        logger.info(f"Extracted {count} benign domains from Tranco.")
    except Exception as e:
        logger.error(f"Failed to download Tranco: {e}")

    if not X or len(set(y)) < 2:
        logger.warning("Failed to load public datasets with both classes. Falling back to dummy data.")
        return load_dummy_data()

    logger.info(f"Public dataset loaded successfully: {len(X)} total samples.")
    return np.array(X), np.array(y)

def load_csv_data(csv_path):
    import csv
    from shared.feature_extraction import FeatureExtractor
    from inference_app.src.config import Config
    
    logger.info(f"Loading CSV dataset from {csv_path}...")
    
    if not csv_path or not os.path.exists(csv_path):
        logger.warning(f"CSV file not found: {csv_path}. Falling back to dummy.")
        return load_dummy_data()
        
    X, y = [], []
    extractor = FeatureExtractor(Config.TARGET_BRANDS)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Domain' in row:
                    domain = row['Domain']
                    vt_res = row.get('VirusTotal_Result', '').strip().lower()
                    gsb_res = row.get('SafeBrowsing_Result', '').strip().lower()
                    heuristics = row.get('Is_Phishing_Heuristics', '').strip().lower() == 'true'
                    
                    if vt_res == 'true' or gsb_res == 'true':
                        is_phishing = True
                    elif vt_res == 'false' or gsb_res == 'false':
                        is_phishing = False
                    else:
                        is_phishing = heuristics
                        
                    X.append(extractor.extract_features(domain))
                    y.append(1 if is_phishing else 0)
    except Exception as e:
        logger.error(f"Error parsing CSV: {e}")
        
    if not X or len(set(y)) < 2:
        logger.warning("Failed to load valid CSV data. Falling back to dummy data.")
        return load_dummy_data()
        
    return np.array(X), np.array(y)

def train_model(dataset_source, csv_path=None):
    if dataset_source == 'dummy':
        X, y = load_dummy_data()
    elif dataset_source == 'public':
        X, y = load_public_datasets()
    elif dataset_source == 'csv':
        X, y = load_csv_data(csv_path)
    else:
        raise ValueError(f"Unknown dataset source: {dataset_source}")

    logger.info(f"Training Random Forest Classifier on {len(X)} samples...")
    # Using scikit-learn for now. In the future, this can be swapped with PyTorch
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the scikit-learn model using joblib
    # When moving to PyTorch, you will use torch.save(model.state_dict(), MODEL_PATH)
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Model successfully saved to {MODEL_PATH}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train the Phishing Detection ML Model")
    parser.add_argument('--dataset', type=str, choices=['dummy', 'public', 'csv'], default='dummy',
                        help="Choose the dataset source for training.")
    parser.add_argument('--csv-path', type=str, default=None,
                        help="Path to the CSV file if dataset is 'csv'.")
    
    args = parser.parse_args()
    
    if args.dataset == 'csv' and not args.csv_path:
        parser.error("--csv-path is required when --dataset is 'csv'")
        
    train_model(args.dataset, args.csv_path)
