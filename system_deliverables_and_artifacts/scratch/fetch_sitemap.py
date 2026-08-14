import requests
from bs4 import BeautifulSoup

def fetch_sitemap():
    sub_sitemaps = [
        "https://www.angelsolutionsatl.com/booking-services-sitemap.xml",
        "https://www.angelsolutionsatl.com/pages-sitemap.xml",
        "https://www.angelsolutionsatl.com/store-products-sitemap.xml"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    all_urls = set()
    for s_url in sub_sitemaps:
        try:
            r = requests.get(s_url, headers=headers, timeout=10)
            print(f"Sub-Sitemap {s_url} status:", r.status_code)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "xml")
                urls = [loc.text for loc in soup.find_all("loc")]
                print(f"Found {len(urls)} URLs in {s_url}")
                for u in urls:
                    all_urls.add(u)
        except Exception as e:
            print(f"Error fetching {s_url}: {e}")
            
    print("\n=== ALL DISCOVERED SITEMAP URLS ===")
    for u in sorted(list(all_urls)):
        print(u)
    print("====================================")

if __name__ == "__main__":
    fetch_sitemap()
