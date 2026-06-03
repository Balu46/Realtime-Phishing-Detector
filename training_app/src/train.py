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

def load_phishtank_data():
    """
    To use PhishTank, you should register at:
    https://www.phishtank.com/developer_info.php
    to get an API key. 
    
    You can download the database (e.g. JSON or CSV format) from:
    http://data.phishtank.com/data/<YOUR_API_KEY>/online-valid.csv
    
    For benign domains, you can use Tranco list:
    https://tranco-list.eu/
    """
    logger.info("Loading PHISHTANK dataset...")
    api_key = os.environ.get("PHISHTANK_API_KEY")
    if not api_key:
        logger.warning("PHISHTANK_API_KEY is not set in environment variables.")
        logger.warning("Please get an API key at https://www.phishtank.com/developer_info.php")
        logger.info("Falling back to dummy data for demonstration...")
        return load_dummy_data()
    
    # Example logic to load from actual downloaded CSVs
    logger.info("PhishTank API Key found! Here you would load the CSV and extract features using FeatureExtractor.")
    # For now, returning dummy data as a placeholder until the real dataset is downloaded.
    return load_dummy_data()

def load_csv_data(csv_path):
    logger.info(f"Loading CSV dataset from {csv_path}...")
    # TODO: Load CSV, extract features for each domain using src.analysis.feature_extraction
    # return X, y
    return load_dummy_data()

def train_model(dataset_source, csv_path=None):
    if dataset_source == 'dummy':
        X, y = load_dummy_data()
    elif dataset_source == 'phishtank':
        X, y = load_phishtank_data()
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
    parser.add_argument('--dataset', type=str, choices=['dummy', 'phishtank', 'csv'], default='dummy',
                        help="Choose the dataset source for training.")
    parser.add_argument('--csv-path', type=str, default=None,
                        help="Path to the CSV file if dataset is 'csv'.")
    
    args = parser.parse_args()
    
    if args.dataset == 'csv' and not args.csv_path:
        parser.error("--csv-path is required when --dataset is 'csv'")
        
    train_model(args.dataset, args.csv_path)
