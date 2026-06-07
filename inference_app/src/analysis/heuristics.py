import logging
import re
from typing import Set, List
try:
    import dnstwist
except ImportError:
    dnstwist = None

logger = logging.getLogger(__name__)

class HeuristicsAnalyzer:
    """
    Analyzes domains using heuristic rules and typosquatting detection.
    Pre-computes typosquatted variants of target brands using dnstwist logic.
    """

    def __init__(self, target_brands: List[str]):
        """
        Initializes the analyzer and pre-computes typosquatted domains.

        Args:
            target_brands (List[str]): A list of brand names to protect.
        """
        self.target_brands = target_brands
        self.typosquatted_domains: Set[str] = set()
        self._generate_typosquatting_variants()

    def _generate_typosquatting_variants(self) -> None:
        """
        Generates typosquatted variants for all target brands and stores them.
        Uses dnstwist if available, otherwise falls back to basic keyword matching.
        """
        logger.info("Generating typosquatting variants for target brands...")
        for brand in self.target_brands:
            base_domain = f"{brand}.com"  # dnstwist usually requires a full domain
            if dnstwist:
                try:
                    # Initialize dnstwist fuzzer for the brand
                    fuzzer = dnstwist.Fuzzer(base_domain)
                    fuzzer.generate()
                    for domain_dict in fuzzer.domains:
                        variant = domain_dict.get('domain')
                        if variant:
                            # We only care about the keyword part, so strip '.com'
                            variant_keyword = variant.replace('.com', '')
                            self.typosquatted_domains.add(variant_keyword)
                except Exception as e:
                    logger.error(f"Error generating variants for {brand} with dnstwist: {e}")
                    self.typosquatted_domains.add(brand)
            else:
                self.typosquatted_domains.add(brand)
                
        logger.info(f"Generated {len(self.typosquatted_domains)} typosquatting variants in total.")

    def is_phishing_heuristic(self, domain: str) -> bool:
        """
        Checks if the observed domain matches any known typosquatted variant
        or directly contains a target brand keyword.

        Args:
            domain (str): The domain name to check.

        Returns:
            bool: True if it matches heuristics for phishing, False otherwise.
        """
        # 1. Direct keyword match (e.g., paypal-login.com)
        for brand in self.target_brands:
            if re.search(rf'(^|[^a-zA-Z0-9]){brand}([^a-zA-Z0-9]|$)', domain):
                return True

        # 2. Typosquatting match
        # To avoid false positives on very short domains, we can check if
        # the exact domain or its sub-parts match our typosquatted set.
        parts = domain.replace('.', '-').split('-')
        for part in parts:
            if part in self.typosquatted_domains and len(part) > 3:
                return True

        return False
