import os
import logging
from config import Config
from threat_intel.virustotal import VirusTotalClient
from threat_intel.google_safe_browsing import SafeBrowsingClient

logging.basicConfig(level=logging.INFO)

vt_configured = bool(Config.VT_API_KEY and Config.VT_API_KEY != 'your_virustotal_api_key_here')
gsb_configured = bool(Config.GSB_API_KEY and Config.GSB_API_KEY != 'your_google_safe_browsing_api_key_here')

print("=== API TEST ===")
print(f"VT Key configured: {vt_configured}")
print(f"GSB Key configured: {gsb_configured}")

test_domain = "testsafebrowsing.appspot.com" # A known test domain for GSB

if vt_configured:
    vt = VirusTotalClient(Config.VT_API_KEY)
    print("Testing VirusTotal API...")
    try:
        res = vt.check_domain(test_domain)
        print(f"VT Result for {test_domain}: {res}")
    except Exception as e:
        print(f"VT Error: {e}")
else:
    print("Skipping VT test (no key).")

if gsb_configured:
    gsb = SafeBrowsingClient(Config.GSB_API_KEY)
    print("Testing Google Safe Browsing API...")
    try:
        res = gsb.check_domain(test_domain)
        print(f"GSB Result for {test_domain}: {res}")
    except Exception as e:
        print(f"GSB Error: {e}")
else:
    print("Skipping GSB test (no key).")
