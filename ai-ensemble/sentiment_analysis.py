# =====================================================================
# ANGEL SOLUTIONS ATL - SENTIMENT ANALYSIS & FRUSTRATION ENGINE
# =====================================================================
# Analyzes inbound user messaging to calculate satisfaction scores
# and flag threads showing intense frustration for human assistance.
# =====================================================================

import re

# High weight negative keywords indicating immediate anger/frustration
ANGER_KEYWORDS = [
    r"\bscam\b", r"\bfraud\b", r"\bliar\b", r"\bcheat\b", r"\bsuck\b", 
    r"\bgarbage\b", r"\btrash\b", r"\bshitty\b", r"\bbullshit\b", r"\bworst\b",
    r"\brip off\b", r"\brefund\b", r"\bchargeback\b", r"\bsue\b", r"\blawsuit\b",
    r"\battorney\b", r"\blawyer\b", r"\breport you\b", r"\bftc\b", r"\bcfpb\b"
]

# Medium weight negative keywords indicating mild frustration/concern
FRUSTRATION_KEYWORDS = [
    r"\bnot working\b", r"\bdelayed\b", r"\bslow\b", r"\bconfused\b", 
    r"\bdisappointed\b", r"\bwhere is my\b", r"\bstill waiting\b", 
    r"\bno response\b", r"\bignore\b", r"\bignoring\b"
]

# Positive keywords indicating happy engagement
POSITIVE_KEYWORDS = [
    r"\bthank you\b", r"\bthanks\b", r"\bawesome\b", r"\bgreat\b", 
    r"\bamazing\b", r"\blove\b", r"\bexcited\b", r"\bperfect\b", 
    r"\bhelpful\b", r"\bappreciate\b"
]

def analyze_sentiment(text: str) -> dict:
    """
    Computes a deterministic sentiment score between -1.0 and 1.0.
    Flags threads for immediate handoff if score drops below -0.6.
    """
    if not text:
        return {"sentiment_score": 0.0, "flag_escalation": False, "category": "neutral"}

    clean_text = text.lower().strip()
    score = 0.0

    # Count positive signals
    pos_count = 0
    for kw in POSITIVE_KEYWORDS:
        if re.search(kw, clean_text):
            pos_count += 1

    # Count high negative signals
    anger_count = 0
    for kw in ANGER_KEYWORDS:
        if re.search(kw, clean_text):
            anger_count += 1

    # Count medium negative signals
    frust_count = 0
    for kw in FRUSTRATION_KEYWORDS:
        if re.search(kw, clean_text):
            frust_count += 1

    # Calculate overall score
    if anger_count > 0:
        # Immediate severe dip
        score = -0.7 - (0.1 * (anger_count - 1)) - (0.05 * frust_count)
    elif frust_count > 0:
        # Moderate dip
        score = -0.3 - (0.1 * (frust_count - 1)) + (0.1 * pos_count)
    else:
        # Neutral or positive
        score = 0.0 + (0.2 * pos_count)

    # Bound score between -1.0 and 1.0
    score = max(-1.0, min(1.0, score))

    # Determine escalation trigger
    flag_escalation = score <= -0.6 or anger_count >= 1

    category = "neutral"
    if score >= 0.25:
        category = "positive"
    elif score <= -0.25:
        category = "negative"

    return {
        "sentiment_score": round(score, 2),
        "flag_escalation": flag_escalation,
        "category": category,
        "indicators": {
            "positives_found": pos_count,
            "frustrations_found": frust_count,
            "anger_triggers_found": anger_count
        }
    }
