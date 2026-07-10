# 👼 Angel Solutions ATL - Migration-Ready Brand Kit & Asset Repository

This structured repository contains the complete, evidence-backed forensic brand audit, packaged assets, business information, and design system extracted from Jordynn Miller's live Wix site (`https://www.angelsolutionsatl.com/`). 

It is structured specifically for a zero-defect migration and deployment onto **Cloudflare (Next.js 16 App Router Frontend + Hono Workers Backend with D1/KV storage)**.

---

## 📂 Repository Directory Layout

```
angel-solutions-atl-brand-kit/
├── README.md                     # Master migration guide & project briefing (This file)
├── SOURCE-MANIFEST.md            # Registry of crawled sitemaps, urls, and raw Wix domains
├── assets/                       # Downloaded high-resolution original static images
│   ├── logos/                    # Primary, transparent, favicon, and badge marks
│   ├── founder/                  # Headshots and media assets of Jordynn Miller (CEO)
│   ├── backgrounds/              # Background tiles and pattern textures
│   ├── services/                 # Service-specific graphic assets and illustrations
│   └── uncategorized/            # Fallback general images
├── brand/                        # Computed color, typography, design token mappings
│   ├── colors.json               # JSON palette mapping with RGB, HEX, and HSL tokens
│   ├── colors.css                # Raw CSS variables for global importing
│   ├── color-report.md           # WCAG 2.1 AA/AAA contrast assertion analysis
│   ├── typography.json           # Playfair Display & Inter font configurations
│   ├── design-tokens.json        # Border-radii, spacing grids, and shadow variables
│   ├── design-tokens.css         # Importable design token CSS styles
│   └── design-system.md          # Unified typography scale and layout blueprints
├── business/                     # Clean structured JSON database representations
│   ├── business-profile.json     # Brand mission, copyrights, and legal entity naming
│   ├── services.json             # Core advisory, tax prep, and credit building lines
│   ├── pricing.json              # Silver/Gold/Platinum packages & credit monitoring fees
│   ├── contact.json              # Public phone, address, and booking endpoints
│   ├── social-profiles.json      # Linked Instagram and Facebook social handles
│   └── compliance-inventory.json # Circular 230 guidelines and opt-out messaging
├── content/                      # Clean, pre-rendered page copy converted to markdown
│   ├── home.md                   # Home page body content and CTA link mapping
│   ├── credit.md                 # Primary credit monitoring subpage text copy
│   ├── ourservices.md            # Advisory offerings menu
│   ├── taxsolutions.md           # Business and corporate tax resolution text
│   ├── privacy-policy.md         # Text compliance agreements and disclosure copy
│   └── other-pages/              # Booking, duplicates, shop, and medicare-insurance subpages
└── reports/                      # Forensic audit spreadsheets and quality reviews
    ├── url-inventory.csv         # Sitemap index crawler results and indexing rules
    ├── assets.csv                # Path, original CDN link, hashes, sizes, and type mapping
    ├── duplicates.csv            # SHA-256 duplicate image asset detection report
    ├── missing-assets.csv        # Log of unresolved or protected files
    ├── broken-links.csv          # Broken links and mismatched contact destinations
    └── accessibility-colors.csv  # Computed contrast scores and hover compliance levels
```

---

## 🏛️ Forensic Core Business Intel

- **Target Business**: Angel Solutions ATL (Legal: *Angel Solutions ATL Ltd Co.*)
- **Founder / CEO**: Jordynn Miller
- **Primary Public Contact Email**: `info@AngelSolutionsATL.com`
- **Primary Domain**: `https://www.angelsolutionsatl.com/`
- **Key Subpage**: `https://www.angelsolutionsatl.com/credit`
- **Primary Pricing & Packages**:
  - **Silver Formation**: `$450.00`
  - **Gold Formation**: `$550.00`
  - **Platinum Formation**: `$650.00`
  - **Credit Monitoring**: Active accounts require a `$24.99/month` recurring subscription.
- **Accepted Payment Providers**: PayPal, Sezzle, Zip, Afterpay, Affirm.

---

## ⚡ Data Quality & Conflict Red-Flags

During our forensic scrape, we discovered critical mismatches on the live Wix platform that **must be corrected** in our new Cloudflare deployment:

1. **Email / Mailto Mismatches**:
   - The contact forms and mailto links on the core pages target `info@AngelSolutionsATL.com`.
   - However, the **Privacy Policy page contains a mailto link pointing to an external domain / mismatched address** (`info@external-advisor.com`).
   - *Remediation*: Standardize all forms and links to target `info@AngelSolutionsATL.com` globally.
2. **Duplicate Tax Solutions Pages**:
   - There are two identical page routes in the sitemap: `/taxsolutions` and `/copy-of-tax-solutions-1`.
   - *Remediation*: Deprecate the `/copy-of-tax-solutions-1` duplicate route, setting up a 301 Redirect to the clean `/taxsolutions` endpoint on Cloudflare.

---

## 🚀 Cloudflare Next-Generation Rebuild Guide

Use the design tokens, layouts, and markdown copy in this repository to assemble a high-performance Next.js 16 page matching Jordynn Miller's elite branding.

1. **Import Styles**:
   - Add `@import "../brand/colors.css";` and `@import "../brand/design-tokens.css";` in your global Tailwind CSS file (`app/globals.css`).
2. **Setup D1 Database**:
   - Initialize the Cloudflare D1 SQL schemas for business services, pricing, and contact profiles by copying fields from `business/pricing.json` and `business/services.json`.
3. **Connect GoHighLevel API**:
   - Ensure all contact forms, consultation submissions, and booking requests capture lead info and push it directly to your Hono Workers API, which forwards it immediately to GoHighLevel (GHL) with tracking tags indicating they came from the brand-new Cloudflare site.
