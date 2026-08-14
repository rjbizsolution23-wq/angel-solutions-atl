import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def discover():
    base_url = "https://www.angelsolutionsatl.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Try robots.txt first
    robots_url = base_url + "/robots.txt"
    try:
        r = requests.get(robots_url, headers=headers, timeout=10)
        print("=== ROBOTS.TXT ===")
        print(r.text)
        print("==================\n")
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")

    # Discover links from homepage
    homepage_url = base_url + "/"
    try:
        r = requests.get(homepage_url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")
        
        # Check canonical
        canonical = soup.find("link", rel="canonical")
        print(f"Homepage Canonical: {canonical.get('href') if canonical else 'None'}")
        
        # Check sitemaps
        sitemaps = []
        for s in soup.find_all("link", rel="sitemap"):
            sitemaps.append(s.get("href"))
        print(f"Found sitemaps in HTML links: {sitemaps}")
        
        # Gather all same-domain links
        links = set()
        for a in soup.find_all("a", href=True):
            href = a.get("href").strip()
            # Resolve relative URLs
            full_url = urllib.parse.urljoin(base_url, href)
            # Parse URL
            parsed = urllib.parse.urlparse(full_url)
            # Filter same domain
            if "angelsolutionsatl.com" in parsed.netloc:
                # Remove query params or fragments
                clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
                links.add(clean_url)
                
        print("=== DISCOVERED SAME-DOMAIN LINKS ===")
        for link in sorted(list(links)):
            print(link)
        print("====================================\n")
        
    except Exception as e:
        print(f"Error crawling homepage: {e}")

if __name__ == "__main__":
    discover()
