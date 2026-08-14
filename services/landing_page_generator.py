# =====================================================================
# ANGEL SOLUTIONS ATL - DYNAMIC DOCK FUNNEL LANDING PAGES
# =====================================================================
# Programmatic HTML builder that compiles personalized landing pages with
# custom progress loaders and integrated Stripe payments.
# =====================================================================

import os

def generate_personalized_landing_page(lead_name: str, recommended_offer: str, payment_url: str) -> str:
    """
    Compiles a robust, beautiful landing page for a targeted qualified lead.
    Highlights custom progress states and embeds Stripe actions.
    """
    is_advanced = "advanced" in recommended_offer.lower()
    
    price_tag = "$795.00 (One-Time)" if is_advanced else "$67.00 (Monthly)"
    bullet_items = ""
    
    if is_advanced:
        bullet_items = """
            <li>Premium 1-on-1 legal disputes representing your entire profile</li>
            <li>Direct strategy sessions with Jordynn Miller</li>
            <li>Simultaneous removal sequences of all collection items</li>
            <li>Targeted business funding alignment sequences</li>
        """
    else:
        bullet_items = """
            <li>Disputes of up to 5 negative items every month</li>
            <li>Full entry to the active Credit Solution Skool community</li>
            <li>Comprehensive dispute letter generation wizardry</li>
            <li>Ongoing weekly mastermind Q&As</li>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Angel Solutions ATL — Your Financial Restoral Strategy</title>
    <style>
        :root {{
            --bg: #faf8f4; --card: #ffffff; --fg: #1c1917;
            --muted-fg: #78716c; --border: #e7e2d9; --primary: #b45309;
            --primary-hover: #92400e;
        }}
        body {{
            background: var(--bg); color: var(--fg); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 2rem 1rem; display: flex; align-items: center; justify-content: center; min-height: 100vh;
        }}
        .container {{
            max-width: 580px; width: 100%; background: var(--card); border: 1px solid var(--border); border-radius: 1rem;
            padding: 2.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }}
        .header h1 {{ font-size: 1.6rem; margin: 0 0 0.5rem; color: var(--primary); }}
        .header p {{ color: var(--muted-fg); margin: 0 0 1.5rem; font-size: 0.95rem; }}
        .progress-container {{ background: #f1ede6; border-radius: 99px; height: 10px; margin-bottom: 2rem; overflow: hidden; }}
        .progress-bar {{ background: var(--primary); height: 100%; width: 75%; border-radius: 99px; }}
        .benefit-card {{ background: #faf8f4; border: 1px solid var(--border); border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem; }}
        .benefit-card h3 {{ margin: 0 0 0.75rem; font-size: 1.05rem; }}
        ul {{ padding-left: 1.25rem; margin: 0; font-size: 0.9rem; line-height: 1.6; }}
        li {{ margin-bottom: 0.5rem; }}
        .pricing {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 1.5rem; color: var(--fg); text-align: center; }}
        .btn {{
            display: block; width: 100%; text-align: center; background: var(--primary); color: #fff; text-decoration: none;
            padding: 1rem; border-radius: 0.5rem; font-weight: 600; transition: background 0.2s; font-size: 1rem;
        }}
        .btn:hover {{ background: var(--primary-hover); }}
        .footer {{ text-align: center; font-size: 0.75rem; color: var(--muted-fg); margin-top: 2rem; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Ready to Clear Your Roadblocks, {lead_name}?</h1>
            <p>We've analyzed your credit profile metrics. Here is your custom restoral roadmap!</p>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        
        <div class="benefit-card">
            <h3>Your Recommended Plan: {recommended_offer}</h3>
            <ul>
                {bullet_items}
            </ul>
        </div>
        
        <div class="pricing">
            Plan Price: {price_tag}
        </div>
        
        <a href="{payment_url}" class="btn">Proceed to Secure Stripe Checkout</a>
        
        <div class="footer">
            Angel Solutions ATL &copy; 2026. All transactions are securely processed via SSL using Stripe.
        </div>
    </div>
</body>
</html>"""

    return html_template
