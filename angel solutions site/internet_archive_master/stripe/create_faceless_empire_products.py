import stripe
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Use live key as requested
api_key = os.getenv("STRIPE_SECRET_KEY_LIVE")
print(f"Using API Key: {api_key[:10]}...")
stripe.api_key = api_key

funnel_products = [
    {
        "id": "prometheus_upgrade",
        "name": "PROMETHEUS Upgrade",
        "description": "Unlock PROMETHEUS - Money Rick Faceless Empire 2026",
        "unit_amount": 9700,
        "interval": None,
        "success_url": "https://chatgpt.com/g/g-69b0abedaeac8191b7acf68756b74269-money-rick-faceless-empire-2026"
    },
    {
        "id": "faceless_automation_templates",
        "name": "Faceless Automation Templates",
        "description": "AI content systems, viral post templates, marketing automation flows, AI prompt packs.",
        "unit_amount": 2700,
        "interval": None
    },
    {
        "id": "faceless_business_blueprints",
        "name": "Faceless Business Blueprints",
        "description": "4 complete AI business models: YouTube, Digital Products, Affiliate Marketing, Instagram.",
        "unit_amount": 4700,
        "interval": None
    },
    {
        "id": "ai_automation_masterclass",
        "name": "AI Automation Masterclass",
        "description": "Workflow creation, automation stack, agent building, scaling AI businesses.",
        "unit_amount": 9700,
        "interval": None
    },
    {
        "id": "elite_ai_agent_pack",
        "name": "Elite AI Agent Pack",
        "description": "10 specialized money-making AI agents.",
        "unit_amount": 19700,
        "interval": None
    }
]

results = {}

for p in funnel_products:
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
        price = stripe.Price.create(**price_params)
        
        # Create payment link
        link_params = {
            "line_items": [{"price": price.id, "quantity": 1}],
            "metadata": {"package_id": p["id"]}
        }
        
        # Add success URL if provided (specifically for Prometheus)
        if p.get("success_url"):
            link_params["after_completion"] = {
                "type": "redirect",
                "redirect": {"url": p["success_url"]}
            }
            
        payment_link = stripe.PaymentLink.create(**link_params)
        
        results[p["id"]] = {
            "url": payment_link.url,
            "amount": p["unit_amount"],
            "name": p["name"]
        }
        print(f"SUCCESS: {p['id']} -> {payment_link.url}")
        
    except Exception as e:
        print(f"ERROR: Failed to create {p['id']}: {e}")

with open('faceless_empire_links.json', 'w') as f:
    json.dump(results, f, indent=2)

print('\nDone! Links saved to faceless_empire_links.json')
