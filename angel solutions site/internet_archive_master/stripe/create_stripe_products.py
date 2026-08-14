import stripe
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Use live key as requested
api_key = os.getenv("STRIPE_SECRET_KEY_LIVE")
print(f"Using API Key: {api_key[:10]}...")
stripe.api_key = api_key

products_data = [
    {
        "id": "lead_engine",
        "name": "AI Motivated Seller Lead Engine",
        "description": "Pre-foreclosure, tax-delinquent, absentee owner leads with AI motivation scoring 0-100.",
        "unit_amount": 9700,
        "interval": "month",
        "badge": "Most Popular"
    },
    {
        "id": "deal_analyzer",
        "name": "AI Deal Analyzer & ARV Calculator",
        "description": "Instant ARV, MAO, repair estimates, flip P&L, AI-written deal narrative.",
        "unit_amount": 4700,
        "interval": "month",
        "badge": "Best ROI"
    },
    {
        "id": "crm",
        "name": "Wholesaler CRM & Pipeline System",
        "description": "Full-stack CRM with lead import, AI scoring, SMS/email automation.",
        "unit_amount": 14900,
        "interval": "month",
        "badge": "Scale Killer"
    },
    {
        "id": "market_dashboard",
        "name": "Neighborhood Intelligence Dashboard",
        "description": "ZIP-code level market intelligence with 40+ data points.",
        "unit_amount": 5900,
        "interval": "month",
        "badge": "Agent Favorite"
    },
    {
        "id": "alerts",
        "name": "Distressed Property Alert System",
        "description": "Real-time notifications for lis pendens, tax delinquency, bankruptcy.",
        "unit_amount": 7900,
        "interval": "month",
        "badge": "First Mover"
    },
    {
        "id": "copy_generator",
        "name": "AI Listing Copy & Marketing Generator",
        "description": "Professional MLS descriptions, social media, email sequences in seconds.",
        "unit_amount": 2900,
        "interval": "month",
        "badge": "Time Saver"
    },
    {
        "id": "cash_buyers",
        "name": "Cash Buyers Network Database",
        "description": "National cash buyer database from public deed records.",
        "unit_amount": 9700,
        "interval": "month",
        "badge": "Flip Faster"
    },
    {
        "id": "website",
        "name": "Agent Website + Lead Funnel",
        "description": "SEO-optimized website with lead capture and built-in CRM.",
        "unit_amount": 19700,
        "interval": "month",
        "badge": "24/7 Sales"
    },
    {
        "id": "starter",
        "name": "Starter",
        "description": "Single tool. Single market. Get moving today.",
        "unit_amount": 49700,
        "interval": None,
        "badge": None
    },
    {
        "id": "scale",
        "name": "Scale",
        "description": "Full lead-to-close pipeline. This is the one.",
        "unit_amount": 149700,
        "interval": None,
        "badge": "MOST POPULAR"
    }
]

results = {}

for p in products_data:
    try:
        print(f"Creating product: {p['name']}...")
        # Create product
        product = stripe.Product.create(
            name=p["name"],
            description=p["description"],
            metadata={"product_id": p["id"]}
        )
        
        # Create price
        price_params = {
            "product": product.id,
            "unit_amount": p["unit_amount"],
            "currency": "usd",
        }
        if p["interval"]:
            price_params["recurring"] = {"interval": p["interval"]}
            
        price = stripe.Price.create(**price_params)
        
        # Create payment link
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            metadata={"package_id": p["id"]}
        )
        
        results[p["id"]] = {
            "url": payment_link.url,
            "amount": p["unit_amount"],
            "badge": p["badge"]
        }
        print(f"SUCCESS: {p['id']} -> {payment_link.url}")
        
    except Exception as e:
        print(f"ERROR: Failed to create {p['id']}: {e}")

with open("stripe_links.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nDone! Links saved to stripe_links.json")
