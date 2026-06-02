from config import Config
from threat_intel.google_safe_browsing import SafeBrowsingClient

gsb = SafeBrowsingClient(Config.GSB_API_KEY)
test_domain = "testsafebrowsing.appspot.com/s/malware.html"
res = gsb.check_domain(test_domain)
print(f"GSB Result: {res}")
