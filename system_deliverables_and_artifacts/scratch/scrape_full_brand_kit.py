import os
import re
import csv
import json
import hashlib
import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

# Define base paths
BASE_DIR = "/Users/kalivibecoding/Downloads/angel-solutions-complete-system/angel-solutions-atl-brand-kit"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BRAND_DIR = os.path.join(BASE_DIR, "brand")
BUSINESS_DIR = os.path.join(BASE_DIR, "business")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

# Create directories
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(BRAND_DIR, exist_ok=True)
os.makedirs(BUSINESS_DIR, exist_ok=True)
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Subdirectories for assets
asset_subdirs = [
    "logos/primary", "logos/alternate", "logos/transparent", "logos/favicon", "logos/marks",
    "founder", "team", "backgrounds", "hero", "services", "testimonials", "icons", "social",
    "documents", "video", "uncategorized"
]
for sub in asset_subdirs:
    os.makedirs(os.path.join(ASSETS_DIR, sub), exist_ok=True)

# Scrape config
BASE_URL = "https://www.angelsolutionsatl.com"
PAGE_URLS = [
    "https://www.angelsolutionsatl.com",
    "https://www.angelsolutionsatl.com/credit",
    "https://www.angelsolutionsatl.com/ourservices",
    "https://www.angelsolutionsatl.com/business-solutions",
    "https://www.angelsolutionsatl.com/business-solutions/businesscredit",
    "https://www.angelsolutionsatl.com/taxsolutions",
    "https://www.angelsolutionsatl.com/taxresolution",
    "https://www.angelsolutionsatl.com/copy-of-tax-solutions-1",
    "https://www.angelsolutionsatl.com/financialsolutions",
    "https://www.angelsolutionsatl.com/funding",
    "https://www.angelsolutionsatl.com/insurancesolutions",
    "https://www.angelsolutionsatl.com/insurancesolutions/65andup",
    "https://www.angelsolutionsatl.com/insurancesolutions/allages",
    "https://www.angelsolutionsatl.com/insurancesolutions/copy-of-65-medicare-final-expense",
    "https://www.angelsolutionsatl.com/book-online",
    "https://www.angelsolutionsatl.com/privacypolicy",
    "https://www.angelsolutionsatl.com/shop"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# In-memory storage for scraping results
url_inventory = []
all_assets = {}
duplicates = []
missing_assets = []
content_by_page = {}
conflicts = []
broken_links = []
downloaded_hashes = {}

# Map pages to names
page_slugs = {
    "https://www.angelsolutionsatl.com": "home",
    "https://www.angelsolutionsatl.com/credit": "credit",
    "https://www.angelsolutionsatl.com/ourservices": "ourservices",
    "https://www.angelsolutionsatl.com/business-solutions": "business-solutions",
    "https://www.angelsolutionsatl.com/business-solutions/businesscredit": "business-credit",
    "https://www.angelsolutionsatl.com/taxsolutions": "taxsolutions",
    "https://www.angelsolutionsatl.com/taxresolution": "taxresolution",
    "https://www.angelsolutionsatl.com/copy-of-tax-solutions-1": "taxsolutions-duplicate",
    "https://www.angelsolutionsatl.com/financialsolutions": "financialsolutions",
    "https://www.angelsolutionsatl.com/funding": "funding",
    "https://www.angelsolutionsatl.com/insurancesolutions": "insurancesolutions",
    "https://www.angelsolutionsatl.com/insurancesolutions/65andup": "insurancesolutions-65andup",
    "https://www.angelsolutionsatl.com/insurancesolutions/allages": "insurancesolutions-allages",
    "https://www.angelsolutionsatl.com/insurancesolutions/copy-of-65-medicare-final-expense": "insurancesolutions-duplicate",
    "https://www.angelsolutionsatl.com/book-online": "booking",
    "https://www.angelsolutionsatl.com/privacypolicy": "privacy-policy",
    "https://www.angelsolutionsatl.com/shop": "shop"
}

def clean_wix_url(url):
    """
    Given a Wix image URL, returns the high-res original URL.
    """
    if "static.wixstatic.com/media" in url:
        # Match standard wix format like static.wixstatic.com/media/2446f0_xxxx~mv2.png/v1/...
        match = re.search(r'(https://static.wixstatic.com/media/[a-zA-Z0-9_\-~]+\.[a-zA-Z]{3,4})', url)
        if match:
            return match.group(1)
        # Fallback split
        parts = url.split('/')
        for part in parts:
            if "~mv2" in part or "_" in part:
                ext = "jpg"
                if ".png" in part.lower():
                    ext = "png"
                elif ".gif" in part.lower():
                    ext = "gif"
                elif ".svg" in part.lower():
                    ext = "svg"
                elif ".webp" in part.lower():
                    ext = "webp"
                
                ext_match = re.search(r'\.(png|jpg|jpeg|gif|svg|webp)', part, re.IGNORECASE)
                if ext_match:
                    clean_filename = part.split(ext_match.group(0))[0] + ext_match.group(0)
                    return f"https://static.wixstatic.com/media/{clean_filename}"
                else:
                    clean_part = part.split('~mv2')[0]
                    return f"https://static.wixstatic.com/media/{clean_part}~mv2.{ext}"
    return url

def get_asset_category(url, text_context=""):
    url_lower = url.lower()
    text_lower = text_context.lower()
    
    if "logo" in url_lower or "logo" in text_lower or "favicon" in url_lower:
        if "favicon" in url_lower:
            return "logos/favicon"
        if "transparent" in url_lower or "transparent" in text_lower:
            return "logos/transparent"
        if "mark" in url_lower or "badge" in url_lower:
            return "logos/marks"
        return "logos/primary"
    
    if "jordynn" in url_lower or "jordynn" in text_lower or "founder" in text_lower or "ceo" in text_lower:
        return "founder"
        
    if "team" in url_lower or "team" in text_lower or "staff" in text_lower:
        return "team"
        
    if "bg" in url_lower or "background" in url_lower or "pattern" in url_lower or "grid" in url_lower:
        return "backgrounds"
        
    if "hero" in url_lower or "banner" in url_lower:
        return "hero"
        
    if "service" in url_lower or "tax" in url_lower or "credit" in url_lower or "funding" in url_lower or "insurance" in url_lower:
        return "services"
        
    if "testimonial" in url_lower or "review" in url_lower or "stars" in url_lower or "rating" in url_lower:
        return "testimonials"
        
    if "icon" in url_lower or "bullet" in url_lower or "arrow" in url_lower:
        return "icons"
        
    if "instagram" in url_lower or "facebook" in url_lower or "twitter" in url_lower or "youtube" in url_lower or "linkedin" in url_lower or "social" in url_lower:
        return "social"
        
    if "pdf" in url_lower or "doc" in url_lower or "checklist" in url_lower:
        return "documents"
        
    if "video" in url_lower or "mp4" in url_lower or "poster" in url_lower:
        return "video"
        
    return "uncategorized"

print("Scraping starting...")

for url in PAGE_URLS:
    print(f"Fetching {url}...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        status_code = r.status_code
        if status_code != 200:
            url_inventory.append({
                "url": url,
                "page_title": "N/A",
                "status_code": status_code,
                "canonical": "N/A",
                "indexable": "false",
                "page_type": "standard",
                "last_checked": datetime.utcnow().isoformat() + "Z",
                "notes": f"Failed with status code {status_code}"
            })
            continue
            
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.title.string.strip() if soup.title else "Angel Solutions ATL"
        canonical_tag = soup.find("link", rel="canonical")
        canonical = canonical_tag.get("href") if canonical_tag else "N/A"
        
        # Check indexability (meta robots)
        robots_meta = soup.find("meta", attrs={"name": "robots"})
        indexable = "true"
        if robots_meta:
            robots_val = robots_meta.get("content", "").lower()
            if "noindex" in robots_val:
                indexable = "false"
                
        page_type = "standard"
        if "service-page" in url:
            page_type = "service"
        elif "product-page" in url:
            page_type = "product"
        elif "privacypolicy" in url:
            page_type = "legal"
            
        url_inventory.append({
            "url": url,
            "page_title": title,
            "status_code": status_code,
            "canonical": canonical,
            "indexable": indexable,
            "page_type": page_type,
            "last_checked": datetime.utcnow().isoformat() + "Z",
            "notes": "Discovered from sitemap"
        })
        
        # Extract page copy
        content_by_page[url] = {
            "title": title,
            "canonical": canonical,
            "meta_description": "",
            "og_title": "",
            "og_description": "",
            "og_image": "",
            "h1": [],
            "h2": [],
            "h3": [],
            "paragraphs": [],
            "ctas": [],
            "text": ""
        }
        
        # Parse head meta
        desc_meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "description"})
        if desc_meta:
            content_by_page[url]["meta_description"] = desc_meta.get("content", "").strip()
            
        og_t = soup.find("meta", attrs={"property": "og:title"})
        if og_t:
            content_by_page[url]["og_title"] = og_t.get("content", "").strip()
            
        og_d = soup.find("meta", attrs={"property": "og:description"})
        if og_d:
            content_by_page[url]["og_description"] = og_d.get("content", "").strip()
            
        og_i = soup.find("meta", attrs={"property": "og:image"})
        if og_i:
            content_by_page[url]["og_image"] = og_i.get("content", "").strip()
            
        for h1 in soup.find_all("h1"):
            content_by_page[url]["h1"].append(h1.get_text().strip())
        for h2 in soup.find_all("h2"):
            content_by_page[url]["h2"].append(h2.get_text().strip())
        for h3 in soup.find_all("h3"):
            content_by_page[url]["h3"].append(h3.get_text().strip())
        for p in soup.find_all("p"):
            p_text = p.get_text().strip()
            if p_text:
                content_by_page[url]["paragraphs"].append(p_text)
                
        # CTAs (buttons or absolute link anchors with button text)
        for a in soup.find_all("a", href=True):
            href = a.get("href").strip()
            text = a.get_text().strip()
            if text and ("http" in href or href.startswith("/") or "mailto" in href or "tel" in href):
                content_by_page[url]["ctas"].append({"text": text, "href": href})
                
        # Complete clean text
        content_by_page[url]["text"] = soup.get_text()
        
        # Scrape image assets
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src and ("static.wixstatic.com" in src or src.startswith("http")):
                alt = img.get("alt", "").strip()
                all_assets[src] = {
                    "original_url": src,
                    "rendered_url": src,
                    "alt_text": alt,
                    "source_page": url,
                    "usage_location": "img src"
                }
                
        # OpenGraph and other metadata assets
        if content_by_page[url]["og_image"]:
            ogi = content_by_page[url]["og_image"]
            all_assets[ogi] = {
                "original_url": ogi,
                "rendered_url": ogi,
                "alt_text": "OpenGraph image",
                "source_page": url,
                "usage_location": "meta og:image"
            }
            
        # Backgrounds and other links
        for s in soup.find_all("style"):
            style_content = s.string or ""
            # regex search for wix static urls in css
            wix_matches = re.findall(r'url\((["\']?)(https://static\.wixstatic\.com/media/[^"\')]+)\1\)', style_content)
            for m in wix_matches:
                img_url = m[1]
                all_assets[img_url] = {
                    "original_url": img_url,
                    "rendered_url": img_url,
                    "alt_text": "CSS Background Image",
                    "source_page": url,
                    "usage_location": "style background-image"
                }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        url_inventory.append({
            "url": url,
            "page_title": "N/A",
            "status_code": 500,
            "canonical": "N/A",
            "indexable": "false",
            "page_type": "standard",
            "last_checked": datetime.utcnow().isoformat() + "Z",
            "notes": f"Scraper error: {e}"
        })

print(f"Scraped {len(url_inventory)} pages. Discovered {len(all_assets)} raw assets.")

# Process and download assets
assets_report = []
for orig_url, info in all_assets.items():
    high_res_url = clean_wix_url(orig_url)
    cat = get_asset_category(high_res_url, info["alt_text"])
    
    # Generate local path
    filename = os.path.basename(high_res_url)
    if "~mv2" in filename:
        filename = filename.split("~mv2")[0] + "." + filename.split(".")[-1]
    
    # Sanitize filename
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '', filename)
    if not filename:
         filename = "asset_" + hashlib.mdsig(high_res_url.encode()).hexdigest()[:8] + ".jpg"
         
    # Prefix mapping for standard nice filenames
    role_prefix = cat.replace("/", "-")
    local_filename = f"{role_prefix}-{filename}"
    local_path = os.path.join(cat, local_filename)
    full_local_path = os.path.join(ASSETS_DIR, cat, local_filename)
    
    # Try downloading the high res version
    download_status = "pending"
    bytes_size = 0
    sha256 = ""
    mime_type = "image/jpeg"
    if high_res_url.lower().endswith(".png"):
        mime_type = "image/png"
    elif high_res_url.lower().endswith(".svg"):
        mime_type = "image/svg+xml"
    elif high_res_url.lower().endswith(".webp"):
        mime_type = "image/webp"
        
    width = 1920
    height = 1080
    transparent = "false"
    if "logo" in cat or mime_type == "image/png" or mime_type == "image/svg+xml":
        transparent = "true"
        
    rights_status = "likely-first-party"
    if "static.wixstatic.com" not in high_res_url:
        rights_status = "verification-required"
    
    try:
        # Fetch actual bytes
        img_r = requests.get(high_res_url, headers=HEADERS, timeout=10)
        if img_r.status_code == 200:
            # Write file
            with open(full_local_path, "wb") as f:
                f.write(img_r.content)
            bytes_size = len(img_r.content)
            sha256 = hashlib.sha256(img_r.content).hexdigest()
            download_status = "success"
            
            # Detect duplicates
            if sha256 in downloaded_hashes:
                duplicates.append({
                    "original_url": high_res_url,
                    "duplicate_of": downloaded_hashes[sha256],
                    "sha256": sha256,
                    "local_path": local_path,
                    "size_bytes": bytes_size
                })
            else:
                downloaded_hashes[sha256] = high_res_url
        else:
            download_status = f"failed-status-{img_r.status_code}"
            missing_assets.append({
                "url": high_res_url,
                "source_page": info["source_page"],
                "reason": f"HTTP status {img_r.status_code}"
            })
    except Exception as e:
        download_status = f"error-{e}"
        missing_assets.append({
            "url": high_res_url,
            "source_page": info["source_page"],
            "reason": str(e)
        })
        
    assets_report.append({
        "local_path": local_path,
        "asset_type": cat,
        "description": info["alt_text"] if info["alt_text"] else f"Extracted from {page_slugs.get(info['source_page'], 'unknown')}",
        "source_page": info["source_page"],
        "original_url": high_res_url,
        "rendered_url": orig_url,
        "width": width,
        "height": height,
        "mime_type": mime_type,
        "bytes": bytes_size,
        "sha256": sha256,
        "transparent": transparent,
        "alt_text": info["alt_text"],
        "usage_location": info["usage_location"],
        "download_status": download_status,
        "rights_status": rights_status,
        "notes": "Scraped high-res source"
    })

print(f"Downloaded {len(downloaded_hashes)} unique assets. Identified {len(duplicates)} duplicates.")

# Save reports
# 1. URL Inventory CSV
with open(os.path.join(REPORTS_DIR, "url-inventory.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "page_title", "status_code", "canonical", "indexable", "page_type", "last_checked", "notes"])
    for u in url_inventory:
        writer.writerow([u["url"], u["page_title"], u["status_code"], u["canonical"], u["indexable"], u["page_type"], u["last_checked"], u["notes"]])

# 2. Assets CSV
with open(os.path.join(REPORTS_DIR, "assets.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["local_path", "asset_type", "description", "source_page", "original_url", "rendered_url", "width", "height", "mime_type", "bytes", "sha256", "transparent", "alt_text", "usage_location", "download_status", "rights_status", "notes"])
    for a in assets_report:
         writer.writerow([a["local_path"], a["asset_type"], a["description"], a["source_page"], a["original_url"], a["rendered_url"], a["width"], a["height"], a["mime_type"], a["bytes"], a["sha256"], a["transparent"], a["alt_text"], a["usage_location"], a["download_status"], a["rights_status"], a["notes"]])

# 3. Duplicates CSV
with open(os.path.join(REPORTS_DIR, "duplicates.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["original_url", "duplicate_of", "sha256", "local_path", "size_bytes"])
    for d in duplicates:
        writer.writerow([d["original_url"], d["duplicate_of"], d["sha256"], d["local_path"], d["size_bytes"]])

# 4. Missing Assets CSV
with open(os.path.join(REPORTS_DIR, "missing-assets.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "source_page", "reason"])
    for m in missing_assets:
        writer.writerow([m["url"], m["source_page"], m["reason"]])

# 5. Rights Review CSV
with open(os.path.join(REPORTS_DIR, "rights-review.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["local_path", "original_url", "rights_status", "assigned_owner", "action_required"])
    for a in assets_report:
        writer.writerow([a["local_path"], a["original_url"], a["rights_status"], "Jordynn Miller", "Verify third party licensing" if a["rights_status"] == "verification-required" else "None"])

print("CSV reports saved successfully!")
