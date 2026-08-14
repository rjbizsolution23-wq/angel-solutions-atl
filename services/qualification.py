# =====================================================================
# ANGEL SOLUTIONS ATL - AUTOMATED LEAD QUALIFICATION ENGINE
# =====================================================================
# Determines target service routing paths based on credit profile metrics.
# Pre-screens for child support, bankruptcy, collections, and timeline.
# =====================================================================

def evaluate_lead_qualification(credit_profile: dict) -> dict:
    """
    Evaluates credit profile details against whitelisted DQ rules.
    Outputs the target state, recommended offer, and redirect reasons.
    """
    # 1. Critical Disqualifications (DQ Gates)
    if credit_profile.get("has_active_bankruptcy", False):
        return {
            "eligible": False,
            "target_state": "DQ",
            "recommended_offer": None,
            "action": "disqualify_to_manual",
            "reason": "Active bankruptcy is currently unresolved. We require discharge papers before standard disputing can begin.",
            "next_step": "Refer to credit counseling or place thread on manual follow-up."
        }

    if credit_profile.get("has_active_child_support_arrears", False):
        return {
            "eligible": False,
            "target_state": "DQ",
            "recommended_offer": None,
            "action": "disqualify_to_manual",
            "reason": "Active state child support arrears must be caught up or settled first, as they block legal credit deletions.",
            "next_step": "Guide to local child support clearing agencies before resuming program."
        }

    # 2. Advanced Credit Restoral Pre-qualification Gate (from $795)
    # Triggers: Urgent timeline (<= 60 days) OR wants business funding OR high collection items count
    collections_count = credit_profile.get("collections_count", 0)
    timeline_days = credit_profile.get("timeline_days", 90)
    needs_business_funding = credit_profile.get("needs_business_funding", False)

    if collections_count >= 10 or timeline_days <= 60 or needs_business_funding:
        return {
            "eligible": True,
            "target_state": "QUALIFIED",
            "recommended_offer": "Advanced Credit Restoral ($795)",
            "action": "route_to_advanced",
            "reason": "Urgent timeline, high collection count, or business funding aspiration require rapid legal team intervention.",
            "next_step": "Guide to book 1-on-1 strategy call: https://angelsolutionsatl.com/book-online"
        }

    # 3. Monthly Credit Repair Community Gate ($67/mo)
    return {
        "eligible": True,
        "target_state": "QUALIFIED",
        "recommended_offer": "Credit Repair Monthly ($67/mo)",
        "action": "route_to_monthly",
        "reason": "Standard DIY pace with low negative count is a perfect fit for our interactive Skool community program.",
        "next_step": "Guide to join monthly community: https://www.skool.com/creditsolution/about"
    }
