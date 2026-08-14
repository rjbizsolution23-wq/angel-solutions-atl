# =====================================================================
# ANGEL SOLUTIONS ATL - SYSTEM PERFORMANCE & KPI ANALYTICS
# =====================================================================
# Analyzes interaction metrics and generates lightweight, premium SVG
# data visualizations and conversion statistics.
# Expanded to dynamically calculate CTR, CPC, CPL, and ROAS using
# direct Meta Marketing API insights.
# =====================================================================

from meta_ads_client import MetaAdsClient

def compute_conversion_kpis(db_env) -> dict:
    """
    Computes key performance metrics and outputs high-fidelity SVG graphics,
    integrating live Meta Ads insights.
    """
    # 1. Base counts & ratios
    total_leads = 120
    qualified_leads = 90
    booked_leads = 45
    dq_leads = 30

    if hasattr(db_env, "DB"):
        try:
            total_res = db_env.DB.prepare("SELECT count(*) as count FROM leads").first()
            total_leads = total_res["count"] if total_res else total_leads

            qual_res = db_env.DB.prepare("SELECT count(*) as count FROM leads WHERE lead_state = 'QUALIFIED'").first()
            qualified_leads = qual_res["count"] if qual_res else qualified_leads

            booked_res = db_env.DB.prepare("SELECT count(*) as count FROM leads WHERE lead_state = 'BOOKED'").first()
            booked_leads = booked_res["count"] if booked_res else booked_leads

            dq_res = db_env.DB.prepare("SELECT count(*) as count FROM leads WHERE lead_state = 'DQ'").first()
            dq_leads = dq_res["count"] if dq_res else dq_leads
        except Exception as e:
            print(f"Error reading counts from database: {e}")

    conversion_rate = (booked_leads / total_leads * 100) if total_leads > 0 else 0.0
    qualification_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0.0

    # 2. Integrate Meta Ads Campaign Analytics
    ads_client = MetaAdsClient()
    campaigns = ads_client.fetch_campaigns()

    total_spend = sum(camp.get("spend", 0.0) for camp in campaigns)
    total_impressions = sum(camp.get("impressions", 0) for camp in campaigns)
    total_clicks = sum(camp.get("clicks", 0) for camp in campaigns)
    total_conversions = sum(camp.get("conversions", 0) for camp in campaigns)

    # Derived Ads Metrics
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0.0
    cpc = (total_spend / total_clicks) if total_clicks > 0 else 0.0
    cpl = (total_spend / total_conversions) if total_conversions > 0 else 0.0

    # Business ROAS (Based on $1,022.50 median contract value per closed call)
    estimated_revenue = booked_leads * 1022.50
    roas = (estimated_revenue / total_spend) if total_spend > 0 else 0.0

    return {
        "metrics": {
            "total_leads": total_leads,
            "qualified_leads": qualified_leads,
            "booked_leads": booked_leads,
            "dq_leads": dq_leads,
            "conversion_rate_percentage": round(conversion_rate, 1),
            "qualification_rate_percentage": round(qualification_rate, 1),
            
            # Ad Specific metrics
            "ad_spend": round(total_spend, 2),
            "ad_impressions": total_impressions,
            "ad_clicks": total_clicks,
            "ad_conversions": total_conversions,
            "ctr_percentage": round(ctr, 2),
            "cpc": round(cpc, 2),
            "cpl": round(cpl, 2),
            "estimated_revenue": round(estimated_revenue, 2),
            "roas": round(roas, 2)
        },
        "campaigns": campaigns,
        "charts": {
            "funnel_svg": generate_funnel_svg(total_leads, qualified_leads, booked_leads)
        }
    }

def generate_funnel_svg(total: int, qual: int, booked: int) -> str:
    """
    Programmatically builds a gorgeous, responsive vector SVG funnel diagram
    using Jordynn's warm amber aesthetic.
    """
    # Safeguard divisions by zero
    t_w = 400
    q_w = int((qual / total) * 400) if total > 0 else 200
    b_w = int((booked / total) * 400) if total > 0 else 100

    svg = f"""
    <svg viewBox="0 0 500 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <!-- Definitions for soft drop-shadow filters -->
        <defs>
            <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
                <feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity="0.04" />
            </filter>
        </defs>
        
        <!-- Total Ingestion Level -->
        <rect x="50" y="20" width="{t_w}" height="60" rx="8" fill="#f1ede6" stroke="#e7e2d9" filter="url(#shadow)" />
        <text x="70" y="55" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#1c1917">Total Ingested Leads ({total})</text>
        <text x="350" y="55" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#78716c">100%</text>

        <!-- Qualified Filter Level -->
        <rect x="50" y="110" width="{q_w}" height="60" rx="8" fill="#fde68a" stroke="#fcd34d" filter="url(#shadow)" />
        <text x="70" y="145" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#78350f">Qualified ({qual})</text>
        <text x="350" y="145" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#b45309">
            {int((qual/total*100) if total > 0 else 0)}%
        </text>

        <!-- Converted Booking Level -->
        <rect x="50" y="200" width="{b_w}" height="60" rx="8" fill="#b45309" stroke="#92400e" filter="url(#shadow)" />
        <text x="70" y="235" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#ffffff">Strategy Calls Booked ({booked})</text>
        <text x="350" y="235" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#ffffff">
            {int((booked/total*100) if total > 0 else 0)}%
        </text>

        <!-- Dynamic indicators -->
        <line x1="250" y1="80" x2="250" y2="110" stroke="#b45309" stroke-width="2" stroke-dasharray="4" />
        <line x1="250" y1="170" x2="250" y2="200" stroke="#b45309" stroke-width="2" stroke-dasharray="4" />
    </svg>
    """
    return svg
