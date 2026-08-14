import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime

BASE_DIR = "/Users/kalivibecoding/Downloads/angel-solutions-complete-system/angel-solutions-atl-brand-kit"
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OTHER_DIR = os.path.join(CONTENT_DIR, "other-pages")
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(OTHER_DIR, exist_ok=True)

PAGE_URLS = {
    "https://www.angelsolutionsatl.com": "home.md",
    "https://www.angelsolutionsatl.com/credit": "credit.md",
    "https://www.angelsolutionsatl.com/ourservices": "ourservices.md",
    "https://www.angelsolutionsatl.com/business-solutions": "business-solutions.md",
    "https://www.angelsolutionsatl.com/business-solutions/businesscredit": "other-pages/business-credit.md",
    "https://www.angelsolutionsatl.com/taxsolutions": "taxsolutions.md",
    "https://www.angelsolutionsatl.com/taxresolution": "other-pages/taxresolution.md",
    "https://www.angelsolutionsatl.com/copy-of-tax-solutions-1": "other-pages/taxsolutions-duplicate.md",
    "https://www.angelsolutionsatl.com/financialsolutions": "financialsolutions.md",
    "https://www.angelsolutionsatl.com/funding": "other-pages/funding.md",
    "https://www.angelsolutionsatl.com/insurancesolutions": "other-pages/insurancesolutions.md",
    "https://www.angelsolutionsatl.com/insurancesolutions/65andup": "other-pages/insurancesolutions-65andup.md",
    "https://www.angelsolutionsatl.com/insurancesolutions/allages": "other-pages/insurancesolutions-allages.md",
    "https://www.angelsolutionsatl.com/insurancesolutions/copy-of-65-medicare-final-expense": "other-pages/insurancesolutions-duplicate.md",
    "https://www.angelsolutionsatl.com/book-online": "booking.md",
    "https://www.angelsolutionsatl.com/privacypolicy": "privacy-policy.md",
    "https://www.angelsolutionsatl.com/shop": "other-pages/shop.md"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def generate_content():
    print("Generating page markdown content...")
    for url, filename in PAGE_URLS.items():
        print(f"Converting {url}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                
                # Title
                title = soup.title.string.strip() if soup.title else "Angel Solutions ATL"
                
                # Clean up header and footer or layout boilerplate if possible, but keep main content
                # For Wix, main page content is usually inside #SITE_PAGES or main
                main_content = soup.find(id="SITE_PAGES") or soup.find("main") or soup.find("body")
                
                # Convert HTML to Markdown
                if main_content:
                    markdown_text = md(str(main_content), heading_style="ATX")
                else:
                    markdown_text = md(r.text, heading_style="ATX")
                
                # Parse metadata
                desc_meta = soup.find("meta", attrs={"name": "description"})
                description = desc_meta.get("content", "").strip() if desc_meta else "N/A"
                
                canonical_tag = soup.find("link", rel="canonical")
                canonical = canonical_tag.get("href") if canonical_tag else "N/A"
                
                # Extract CTAs in page
                ctas = []
                for a in soup.find_all("a", href=True):
                    href = a.get("href").strip()
                    text = a.get_text().strip()
                    if text and (href.startswith("http") or href.startswith("/") or "mailto" in href or "tel" in href):
                        ctas.append(f"- [{text}]({href})")
                ctas_str = "\n".join(ctas[:10]) if ctas else "None"
                
                # Construct final file structure
                full_path = os.path.join(CONTENT_DIR, filename)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(f"""---
source_url: {url}
retrieved_timestamp: {datetime.utcnow().isoformat()}Z
page_title: {title}
canonical_url: {canonical}
meta_description: {description}
---

# {title}

## Extracted Page Metadata
- **Source URL**: {url}
- **Canonical**: {canonical}
- **Description**: {description}

## Extracted CTA Links
{ctas_str}

## Page Content
{markdown_text}
""")
                print(f"Saved {full_path}")
            else:
                print(f"Skipping {url} - status {r.status_code}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    generate_content()
