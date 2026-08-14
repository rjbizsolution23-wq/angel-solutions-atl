# =====================================================================
# ANGEL SOLUTIONS ATL - MULTI-VARIANT CONVERSATIONAL A/B TESTING
# =====================================================================
# Coordinates randomized assignment between message variants and tracks
# conversion rates to optimize outreach performance.
# =====================================================================

import random

# Core active copy variants
VARIANTS = {
    "welcome_greeting": {
        "A": "Hey there! Jordynn Miller here. Ready to clear those credit bottlenecks and secure your business funding? Let's get started! 📈",
        "B": "Hello! Jordynn Miller here. Let's look at your credit profile and see exactly what's blocking your path to funding. What's your goal? ✨"
    },
    "booking_nudge": {
        "A": "Your custom strategy roadmap is ready! Book your 1-on-1 session with our team here to begin: https://angelsolutionsatl.com/book-online 🚀",
        "B": "Let's clear those collection accounts together. Reserve your private strategy call here: https://angelsolutionsatl.com/book-online 📊"
    }
}

def get_assigned_variant(lead_id: str, campaign_id: str) -> dict:
    """
    Deterministically assigns a lead to Variant A or B based on ID hash
    to ensure consistency across reconnects.
    """
    if not lead_id or campaign_id not in VARIANTS:
        # Fallback to random choice
        v_name = random.choice(["A", "B"])
        return {
            "variant": v_name,
            "text": VARIANTS.get(campaign_id, {}).get(v_name, "")
        }

    # Deterministic hash mapping
    hash_val = sum(ord(char) for char in lead_id)
    variant_name = "A" if hash_val % 2 == 0 else "B"

    return {
        "variant": variant_name,
        "text": VARIANTS[campaign_id][variant_name]
    }

def log_variant_impression_or_conversion(campaign_id: str, variant_name: str, event_type: str, db_env) -> bool:
    """
    Increments metrics in the D1 ab_test_runs tracking table.
    """
    if not hasattr(db_env, "DB"):
        print(f"[MOCK A/B] Logged {event_type} event for campaign '{campaign_id}' variant '{variant_name}'")
        return True

    now = datetime.utcnow().isoformat()
    try:
        # Check if record exists
        check_query = "SELECT id, impressions, conversions FROM ab_test_runs WHERE campaign_id = ? AND variant = ?"
        record = db_env.DB.prepare(check_query).bind(campaign_id, variant_name).first()

        if record:
            # Update counts
            if event_type == "impression":
                update_query = "UPDATE ab_test_runs SET impressions = impressions + 1, updated_at = ? WHERE id = ?"
            else:
                update_query = "UPDATE ab_test_runs SET conversions = conversions + 1, updated_at = ? WHERE id = ?"
            db_env.DB.prepare(update_query).bind(now, record["id"]).run()
        else:
            # Create new tracker
            insert_query = """
                INSERT INTO ab_test_runs (id, campaign_id, variant, impressions, conversions, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            imp = 1 if event_type == "impression" else 0
            conv = 1 if event_type == "conversion" else 0
            db_env.DB.prepare(insert_query).bind(crypto.randomUUID(), campaign_id, variant_name, imp, conv, now, now).run()

        return True
    except Exception as e:
        print(f"Error logging A/B metrics to database: {e}")
        return False
