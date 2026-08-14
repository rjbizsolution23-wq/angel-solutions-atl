# =====================================================================
# ANGEL SOLUTIONS ATL - COMPLIANCE KEYWORD ENGINE (PYTHON PORT)
# =====================================================================
# Python implementation of the edge compliance rules for local testing.
# =====================================================================

import re

APPROVED_DOMAINS = [
    "skool.com/creditsolution/about",
    "angelsolutionsatl.com/book",
    "angelsolutionsatl.com/lobby"
]

PROHIBITED_TERM_MAP = {
    r"\bcredit sweep\b": "custom legal challenge",
    r"\bguarantee\b": "highly probable",
    r"\bguaranteed\b": "highly probable",
    r"\bbest\b": "premier",
    r"\byo\b": "",
    r"\bbet\b": ""
}

def apply_compliance_scrubbing(text: str) -> str:
    """
    Scrubs prohibited industry phrases and replaces with compliant terminology.
    """
    if text is None:
        return None
    if not text:
        return ""

    scrubbed = text
    for prohibited, replacement in PROHIBITED_TERM_MAP.items():
        # Match case-insensitively but preserve case of input roughly
        pattern = re.compile(prohibited, re.IGNORECASE)
        scrubbed = pattern.sub(replacement, scrubbed)

    # Clean double spaces that might occur from stripping 'yo' or 'bet'
    scrubbed = re.sub(r"\s+", " ", scrubbed).strip()
    return scrubbed

def check_escalation_triggers(text: str) -> bool:
    """
    Checks if message matches high-priority triggers.
    """
    if not text:
        return False
    clean_text = text.lower()
    triggers = ["scam", "fraud", "reporting you", "refund", "sue", "lawsuit"]
    return any(t in clean_text for t in triggers)

def scrub_unapproved_urls(text: str) -> str:
    """
    Replaces any URLs not in our verified whitelist with a safety warning.
    """
    if not text:
        return ""

    # Regex to find links starting with http or https
    url_pattern = re.compile(r"https?://[^\s]+")
    matches = url_pattern.findall(text)

    scrubbed = text
    for url in matches:
        is_approved = False
        for approved in APPROVED_DOMAINS:
            if approved in url:
                is_approved = True
                break
        
        if not is_approved:
            scrubbed = scrubbed.replace(url, "[Link Removed for Security Compliance]")

    # Check for raw domains without http/https
    domain_pattern = re.compile(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b")
    domain_matches = domain_pattern.findall(scrubbed)
    for dom in domain_matches:
        # Ignore approved raw domains
        is_approved = False
        for approved in APPROVED_DOMAINS:
            if approved.split("/")[0] in dom:
                is_approved = True
                break
        if not is_approved and "skool.com" not in dom and "angelsolutionsatl.com" not in dom:
            # Avoid replacing standard sentence text that ends in a period (e.g. "now.")
            if dom.split(".")[-1] in ["com", "org", "net", "gov", "edu", "io"]:
                scrubbed = scrubbed.replace(dom, "[Link Removed for Security Compliance]")

    return scrubbed
