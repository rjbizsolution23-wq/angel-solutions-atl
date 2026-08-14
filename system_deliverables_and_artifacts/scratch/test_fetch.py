import requests
from bs4 import BeautifulSoup
import json
import urllib.parse

def test_fetch():
    url = "https://www.angelsolutionsatl.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code: {r.status_code}")
        print(f"Length of response: {len(r.text)}")
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.title.string if soup.title else "No Title"
        print(f"Title: {title}")
        
        # Look for wix data scripts
        scripts = soup.find_all("script")
        print(f"Found {len(scripts)} scripts")
        for s in scripts:
            if s.get("id"):
                print(f"Script with ID: {s.get('id')}")
            if s.get("type"):
                print(f"Script with Type: {s.get('type')}")
    except Exception as e:
        print(f"Error fetching URL: {e}")

if __name__ == "__main__":
    test_fetch()
