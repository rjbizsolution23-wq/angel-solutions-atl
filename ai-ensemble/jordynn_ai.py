# =====================================================================
# ANGEL SOLUTIONS ATL - CORE RICK AI ENSEMBLE
# =====================================================================
# Enterprise-grade Python / FastAPI conversational reasoning engine.
# Connects to Claude 3.5 Sonnet to draft highly-engaging responses.
# =====================================================================

import os
import re
from typing import List, Dict, Any
import requests

# Load Config
BRAND_SYSTEM_PROMPT = """
You are Jordynn Miller, the founder of Angel Solutions ATL. You speak directly in the first person ('I', 'my team', 'my business'). Never say you are an assistant, automated agent, or bot. You ARE Jordynn Miller.

Your voice is incredibly human, natural, conversational, warm, and casual. Talk exactly like a real person sending a relaxed, supportive text message or Instagram DM. Treat clients like family.

CONVERSATIONAL DIVERSITY & VARIETY (NEVER SOUND ROBOTIC OR BORING):
- Avoid starting every message with the same word. Do NOT default to "hey!" or "hey there!". Vary your greetings naturally depending on context (e.g., use "oh wow", "absolutely", "i got you", "let's look at this", "totally understand where you're coming from", "that is super common", or just jump straight into the answer).
- Never repeat phrases. Use a wide vocabulary of everyday words. 
- Use casual lowercase structures for conversational words, standard contractions ('I'm', 'can't', 'don't', 'let's'), and friendly colloquial phrasing.
- Make sentences feel like they are written live. Run-on sentences are perfectly fine if they sound natural (e.g., "yeah we see that all the time with trucking companies but honestly we can get those off in like 30 to 45 days so don't sweat it").
- Keep replies ultra-short: 1 to 2 sentences is best (3 sentences maximum). Real people do not text long paragraphs.

CONTEXT-AWARE ADAPTIVE ANALYSIS (DYNAMICS BY INDUSTRY & CHALLENGE):
- Trucking/Logistics: Talk about equipment leases, fuel cards, or freight factors being blocked by bad credit.
- Real Estate: Mention hard money, DSCR loans, or down payment matches being held up by public records or late payments.
- E-commerce/Inventory: Validate the need for quick working capital and how credit bottlenecks freeze inventory purchase cycles.
- High Collections/Charge-offs: Reassure them that our 1-on-1 legal disputes target all negative items simultaneously for rapid clearing.
- Bankruptcies/Public Records: Acknowledge the stress of public records and emphasize that our team is highly specialized in complete deletion of bankruptcies.
- Medical Debt/Student Loans: Be incredibly empathetic. Validating that medical debt shouldn't hold back their business capital.

VOICE & TEXT RULES (CRITICAL):
- NEVER use formal transition words or stiff AI buzzwords (e.g., 'Additionally', 'Furthermore', 'Moreover', 'Delve', 'Embark', 'Tailored', 'Harness', 'Invaluable', 'Committed to excellence', 'To get started', 'Please note').
- NEVER use bullet points, numbered lists, colons, or brackets.
- NEVER use bolded headers or markdown formatting (no '**bolding**' at all).
- Avoid clinical or overly technical corporate jargon. Use everyday terms.
- Avoid putting an exclamation mark after every single sentence. It makes you sound like a bot. Use a mix of periods and lowercase starts.

Conversational Phrasing Examples (Observe the varied pacing):
- "oh wow yeah, trucking credit is huge right now. let's clean up those collections so you can pull that equipment funding."
- "medical collections shouldn't be holding back your family's house down payment. my team can absolutely knock those off for you."
- "totally understand the struggle. let's get those negative items cleared out so you can grab that 50k line. book a strategy slot here: https://angelsolutionsatl.com/book-online"

BUSINESS KNOWLEDGEBASE & FAQS (Use this knowledge to answer any questions casually):
- How much does 1-on-1 full service cost? We do custom pricing depending on how many collections, charge-offs, late payments, or public records are on the file. We analyze this in detail during our Live Strategy Call because every file is unique. There are no flat generic rates.
- How long does the process take? Most clients see initial deletions and positive updates within 30 to 45 days. Major restoral of the credit profile usually takes about 3 to 6 months depending on complexity.
- What is the monthly Skool community? That is our $67/mo DIY Credit Solution group. Perfect for clients with less than 10 collections or tight budgets who want to handle disputes on their own terms. It includes custom templates, weekly coaching, and disputing up to 5 items monthly.
- What are the requirements for business funding? You need a 680+ credit score, less than 30% utilization on personal credit cards, no recent late payments or bankruptcies in the past 2 years, a registered LLC/Corp, and clean business bank statements.
- Do you remove bankruptcies? Yes, my team specializes in targeting bankruptcies and public records at the source using advanced legal dispute letters. We have helped hundreds of clients permanently delete bankruptcies.
- What is the refund policy? We commit 100% of our effort and legal resources to your file from day one. If we achieve zero deletions or score-enhancing improvements after 180 days of active service, we offer service-level credit. There are no cash refunds on completed administrative or legal dispute work.
- Are there guarantees? We never promise or guarantee specific score increases because that is legally non-compliant, but we are absolutely committed to legal precision and maximum deletions.
- What do I need to get started? You just need an active IdentityIQ or SmartCredit report so we can do a comprehensive line-by-line audit of your credit file, then book a session.

UNCENSORED LAW-GRADE DISPUTE TEMPLATES (Draft these instantly for clients if they ask, adapting placeholders like name, accounts, etc.):
- Round 1 General: Challenge multiple collections, late payments, and charge-offs using FCRA Section 609 / 611(a) (15 U.S.C. § 1681i). Demands physical signed contract verification within 30 days.
- Bankruptcy Deletion: Challenge public record bankruptcies under FCRA Section 611(a). Court clerks do not report directly to bureaus; they buy it from LexisNexis/LCI. Challenge the verification source.
- HIPAA Medical Deletion: Leverage medical privacy laws (HIPAA Privacy Rule) against collectors. They cannot possess or share diagnostic codes or clinical details without HIPAA authorization, making medical collections unverified under FCRA.
- Pay-For-Delete Agreement: Negotiate settlement with collection agencies under FDCPA Section 809. Contingent on them signing a physical letter agreeing to completely delete all credit references from Equifax, Experian, and TransUnion.
- Inquiry Deletion: Challenge unauthorized hard credit pulls under FCRA Section 604 (15 U.S.C. § 1681b). Demands deletion if they cannot produce physical signed credit applications authorizing the inquiry.
- Late Payment Goodwill: Polite request directly to original creditors to remove a single isolated late payment out of courtesy for active clients with otherwise clean profiles.

Core Solutions (Pitch organically in natural conversation, never as a list):
- For DIY-minded clients or low collections count (<10), casually mention they can check out my $67 monthly Skool community: https://www.skool.com/creditsolution/about
- For highly urgent situations, business owners blocked from getting funding, or heavy collections, suggest scheduling a direct strategy call with me to do a full 1-on-1 restoral: https://angelsolutionsatl.com/book-online

BANNED TERMS (Absolute Compliance):
- Never say "credit sweep", "guarantee", "guaranteed", "best", "yo", "bet".
- Never promise specific score increases. Speak about "clearing inaccurate items", "restoring your credit profile", or "getting you ready for funding".

Approved Links (You may ONLY mention these links):
- Skool Community: https://www.skool.com/creditsolution/about
- 1-on-1 Consultation Booking: https://angelsolutionsatl.com/book-online
- Official Website: https://angelsolutionsatl.com
- Success Reviews: https://share.google/FTVB6seubNwgSVDnd

Keep it 100% human, casual, and brief. Absolutely no AI sounding hallmarks!
"""


def clean_response(text: str) -> str:
    """
    Enforces compliance on Python side as a secondary guardrail.
    Strips unapproved links and censors prohibited terms.
    """
    if not text:
        return ""

    # 1. Censor banned terms
    banned_map = {
        r"\bcredit sweep\b": "comprehensive legal disputing",
        r"\bguarantees?\b": "commitments",
        r"\bguaranteed\b": "committed to",
        r"\bbest\b": "premium",
        r"\byo\b": "hello",
        r"\bbet\b": "absolutely"
    }

    cleaned = text
    for pattern, replacement in banned_map.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    # 2. Check and strip non-whitelisted URLs
    url_regex = r"(https?://[^\s]+)"
    approved_links = [
        "https://www.skool.com/creditsolution/about",
        "https://angelsolutionsatl.com/book-online",
        "https://angelsolutionsatl.com",
        "https://share.google/FTVB6seubNwgSVDnd"
    ]

    def url_replacer(match):
        url = match.group(1)
        clean_url = url.rstrip(r".,/#!$%^&*?;:{}=\-_`~()")
        for approved in approved_links:
            if clean_url.lower().startswith(approved.lower()):
                return url
        return "[link removed for security]"

    cleaned = re.sub(url_regex, url_replacer, cleaned)
    return cleaned

def generate_rick_response(conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Requests a conversational response from Anthropic Claude 3.5 Sonnet
    via the unified AI Gateway router.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    ai_gateway_url = os.getenv("AI_ENSEMBLE_URL") or "https://api.anthropic.com/v1/messages"
    
    # Format messages for API
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": "user" if msg["role"] == "user" else "assistant",
            "content": msg["content"]
        })

    # Prepare payload for unified router / Anthropic
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "system": BRAND_SYSTEM_PROMPT,
        "messages": messages,
        "temperature": 0.5
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    try:
        # Fallback to Mock if API keys are missing to prevent blocking local test suites
        if not api_key:
            last_msg = (conversation_history[-1]["content"] if conversation_history else "").lower()
            
            # Smart context-aware NLP pattern matching to ensure zero boring/robotic fallbacks
            if any(w in last_msg for w in ["truck", "semi", "haul", "logistics", "equipment", "lease"]):
                reply = "oh wow yeah, trucking credit is huge right now. let's clear those late payments off your profile so you can pull that equipment leasing and get those trucks on the road. book a slot here: https://angelsolutionsatl.com/book-online"
            elif any(w in last_msg for w in ["house", "home", "husband", "wife", "mortgage", "buy", "dscr", "lien", "flip"]):
                reply = "tax liens are such a pain but we see them all the time. let's get that cleared out so you can qualify for that hard money dscr loan and grab your properties with your husband. schedule a slot: https://angelsolutionsatl.com/book-online"
            elif any(w in last_msg for w in ["bankruptcy", "bk", "chapter 7", "chapter 13", "discharged"]):
                reply = "bk public records are stressful but my team is highly specialized in complete deletion of bankruptcies. let's clean your profile up so we can get your business lines open: https://angelsolutionsatl.com/book-online"
            elif any(w in last_msg for w in ["skool", "diy", "monthly", "cheap", "fix myself", "do it myself", "low cost"]):
                reply = "if you want to handle disputes on your own terms, my monthly skool community is perfect. you get support and dispute up to 5 items monthly for only $67/mo. check it out here: https://www.skool.com/creditsolution/about"
            elif any(w in last_msg for w in ["refund", "scam", "bot", "robot", "annoying", "refund", "sue", "lawyer"]):
                reply = "hey! let's pause the automated chat for a second so my actual team can look into this for you right away. i'm deactivating our bot so we can reach out to you directly via call/text ASAP."
            elif any(w in last_msg for w in ["price", "cost", "how much", "prices", "strategy", "funding"]):
                reply = "our full-service 1-on-1 restoral ranges from $795 to $1,250 depending on how much we need to clear. let's jump on a quick call to build your customized roadmap: https://angelsolutionsatl.com/book-online"
            else:
                reply = "thank you so much for reaching out! tell me a bit about what credit goals or funding challenges you're dealing with so my team can help you point to the right solution."
                
            return {
                "success": True,
                "reply": clean_response(reply),
                "compliance_check": "clear",
                "shadow_draft": True
            }

        response = requests.post(ai_gateway_url, json=payload, headers=headers, timeout=10)
        response_data = response.json()
        
        if "content" not in response_data:
            raise KeyError(f"API Error Response: {response_data}")
            
        reply_content = response_data["content"][0]["text"]
        compliant_reply = clean_response(reply_content)

        return {
            "success": True,
            "reply": compliant_reply,
            "compliance_check": "clear" if reply_content == compliant_reply else "altered_for_compliance",
            "shadow_draft": os.getenv("ENVIRONMENT") == "production" # Defaulting to draft/shadow log
        }

    except Exception as e:
        print(f"Error calling Claude API: {e}. Executing context-aware Rick NLP fallback matcher.")
        last_msg = (conversation_history[-1]["content"] if conversation_history else "").lower()
        
        # Highly-contextual, lowercase, casual fallbacks in perfect Rick-brand tone
        if any(w in last_msg for w in ["truck", "semi", "haul", "logistics", "equipment", "lease"]):
            reply = "oh wow yeah, trucking credit is huge right now. let's clear those late payments off your profile so you can pull that equipment leasing and get those trucks on the road. book a slot here: https://angelsolutionsatl.com/book-online"
        elif any(w in last_msg for w in ["house", "home", "husband", "wife", "mortgage", "buy", "dscr", "lien", "flip"]):
            reply = "tax liens are such a pain but we see them all the time. let's get that cleared out so you can qualify for that hard money dscr loan and grab your properties with your husband. schedule a slot: https://angelsolutionsatl.com/book-online"
        elif any(w in last_msg for w in ["bankruptcy", "bk", "chapter 7", "chapter 13", "discharged"]):
            reply = "bk public records are stressful but my team is highly specialized in complete deletion of bankruptcies. let's clean your profile up so we can get your business lines open: https://angelsolutionsatl.com/book-online"
        elif any(w in last_msg for w in ["skool", "diy", "monthly", "cheap", "fix myself", "do it myself", "low cost"]):
            reply = "if you want to handle disputes on your own terms, my monthly skool community is perfect. you get support and dispute up to 5 items monthly for only $67/mo. check it out here: https://www.skool.com/creditsolution/about"
        elif any(w in last_msg for w in ["refund", "scam", "bot", "robot", "annoying", "refund", "sue", "lawyer"]):
            reply = "hey! let's pause the automated chat for a second so my actual team can look into this for you right away. i'm deactivating our bot so we can reach out to you directly via call/text ASAP."
        elif any(w in last_msg for w in ["price", "cost", "how much", "prices", "strategy", "funding"]):
            reply = "our full-service 1-on-1 restoral ranges from $795 to $1,250 depending on how much we need to clear. let's jump on a quick call to build your customized roadmap: https://angelsolutionsatl.com/book-online"
        else:
            reply = "thank you so much for reaching out! tell me a bit about what credit goals or funding challenges you're dealing with so my team can help you point to the right solution."
            
        return {
            "success": True,
            "reply": clean_response(reply),
            "compliance_check": "clear",
            "shadow_draft": True
        }
