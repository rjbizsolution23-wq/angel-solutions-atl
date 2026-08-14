import stripe
import json
import time

stripe.api_key = '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'

def get_all_products():
    print("Fetching all products...")
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
    print(f"Total products fetched: {len(products)}")
    return products

def get_all_prices():
    print("Fetching all prices...")
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
    print(f"Total prices fetched: {len(prices)}")
    return prices

def get_all_payment_links():
    print("Fetching all payment links...")
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
    print(f"Total payment links fetched: {len(payment_links)}")
    return payment_links

def main():
    products = get_all_products()
    prices = get_all_prices()
    payment_links = get_all_payment_links()
    
    # Map product ID to product object
    product_map = {p.id: p for p in products}
    # Map price ID to price object
    price_map = {pr.id: pr for pr in prices}
    
    print("Mapping payment links to products...")
    # Map payment link URL to product/price details
    mapped_inventory = []
    
    for idx, pl in enumerate(payment_links):
        if not pl.active:
            continue
        try:
            # Fetch line items to get the price and product ID
            line_items = stripe.PaymentLink.list_line_items(pl.id, limit=10).data
            for li in line_items:
                price_id = li.price.id
                price_obj = price_map.get(price_id)
                product_obj = None
                if price_obj:
                    product_obj = product_map.get(price_obj.product)
                
                amount = li.price.unit_amount
                currency = li.price.currency
                interval = None
                if price_obj and price_obj.recurring:
                    interval = price_obj.recurring.interval
                
                mapped_inventory.append({
                    "payment_link_id": pl.id,
                    "url": pl.url,
                    "product_id": product_obj.id if product_obj else "Unknown",
                    "product_name": product_obj.name if product_obj else "Unknown",
                    "product_description": product_obj.description if product_obj else "",
                    "price_id": price_id,
                    "amount": amount,
                    "currency": currency,
                    "interval": interval,
                    "active": pl.active
                })
            # Respect rate limit
            time.sleep(0.05)
        except Exception as e:
            print(f"Error mapping payment link {pl.id}: {e}")
            
    # Sort inventory by product name
    mapped_inventory.sort(key=lambda x: x["product_name"])
    
    # Build markdown table
    md_content = """# Complete Live Stripe Product & Payment Link Inventory

This is a complete, auto-generated inventory of all active products, payment links, prices, and descriptions retrieved directly from the live Stripe account.

---

## Active Product & Link Inventory

| Product Name | Description | Price | Billing | Stripe Product ID | Payment Link URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for item in mapped_inventory:
        price_val = f"${item['amount']/100:.2f}" if item['amount'] is not None else "Custom"
        billing_val = f"per {item['interval']}" if item['interval'] else "one-time"
        desc = item['product_description'].replace("\n", " ").strip() if item['product_description'] else "No description provided."
        md_content += f"| **{item['product_name']}** | {desc} | {price_val} | {billing_val} | `{item['product_id']}` | [Stripe Link]({item['url']}) |\n"
        
    # Write to target inventory file
    target_path = "/Users/kalivibecoding/.gemini/antigravity/brain/cb2045c1-a701-43e6-8e4b-d61ff05509cc/product_inventory.md"
    with open(target_path, "w") as f:
        f.write(md_content)
        
    print(f"Successfully generated inventory containing {len(mapped_inventory)} entries at {target_path}")

if __name__ == "__main__":
    main()
