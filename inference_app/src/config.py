import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the CT Logs Phishing Detection System.
    Loads API keys and defines target brands for typosquatting checks.
    """
    
    VT_API_KEY: str = os.getenv("VT_API_KEY", "")
    GSB_API_KEY: str = os.getenv("GSB_API_KEY", "")

    # Target brands to monitor for phishing and typosquatting
    TARGET_BRANDS: List[str] = [
        "paypal",
        "societegenerale",
        "bankofamerica",
        "apple",
        "microsoft",
        "google",
        "facebook",
        "amazon"
    ]

