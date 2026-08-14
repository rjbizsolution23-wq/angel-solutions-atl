import stripe
import json
import time
import os

stripe.api_key = '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'

def main():
    print("Fetching products from Stripe...")
    products = []
    has_more = True
    starting_after = None
    while has_more:
        resp = stripe.Product.list(limit=100, starting_after=starting_after)
        products.extend(resp.data)
        has_more = resp.has_more
        if has_more and resp.data:
            starting_after = resp.data[-1].id
        else:
            break
            
    print("Fetching prices from Stripe...")
    prices = []
    has_more = True
    starting_after = None
    while has_more:
        resp = stripe.Price.list(limit=100, starting_after=starting_after)
        prices.extend(resp.data)
        has_more = resp.has_more
        if has_more and resp.data:
            starting_after = resp.data[-1].id
        else:
            break
            
    print("Fetching payment links from Stripe...")
    payment_links = []
    has_more = True
    starting_after = None
    while has_more:
        resp = stripe.PaymentLink.list(limit=100, starting_after=starting_after)
        payment_links.extend(resp.data)
        has_more = resp.has_more
        if has_more and resp.data:
            starting_after = resp.data[-1].id
        else:
            break
            
    product_map = {p.id: p for p in products}
    price_map = {pr.id: pr for pr in prices}
    
    mapped_inventory = {}
    
    print("Building inventory mapping...")
    for pl in payment_links:
        if not pl.active:
            continue
        try:
            line_items = stripe.PaymentLink.list_line_items(pl.id, limit=10).data
            for li in line_items:
                price_id = li.price.id
                price_obj = price_map.get(price_id)
                product_obj = None
                if price_obj:
                    product_obj = product_map.get(price_obj.product)
                
                if not product_obj:
                    continue
                    
                # Create slug from product name or ID
                slug = product_obj.name.lower().replace(" ", "-").replace("/", "-").replace("&", "and").replace("™", "").replace("®", "")
                slug = "".join([c for c in slug if c.isalnum() or c == "-"])
                # Handle duplicates
                original_slug = slug
                counter = 1
                while slug in mapped_inventory:
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                    
                mapped_inventory[slug] = {
                    "slug": slug,
                    "payment_link_id": pl.id,
                    "url": pl.url,
                    "product_id": product_obj.id,
                    "product_name": product_obj.name,
                    "product_description": product_obj.description or "",
                    "price_id": price_id,
                    "amount": li.price.unit_amount,
                    "currency": li.price.currency,
                    "interval": price_obj.recurring.interval if price_obj and price_obj.recurring else None
                }
            time.sleep(0.05)
        except Exception as e:
            print(f"Error mapping {pl.id}: {e}")
            
    # Make sure output directory exists
    os.makedirs("/Users/kalivibecoding/Downloads/skilz/stripe/frontend/lib", exist_ok=True)
    with open("/Users/kalivibecoding/Downloads/skilz/stripe/frontend/lib/products_db.json", "w") as f:
        json.dump(mapped_inventory, f, indent=2)
        
    print(f"Successfully generated JSON database with {len(mapped_inventory)} items.")

if __name__ == "__main__":
    main()
