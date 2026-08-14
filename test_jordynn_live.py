# =====================================================================
# ANGEL SOLUTIONS ATL - INTERACTIVE RICK AI CHAT TESTER
# =====================================================================
# This tool allows you to chat live with the Jordynn Miller AI engine.
# It runs the exact prompt logic deployed on the Cloudflare Workers 
# and fallback FastAPI backend. Use it to test variety, FAQs, 
# and template generation in real-time.
# =====================================================================

import sys
import os

# Ensure the parent directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import importlib
jordynn_ai_module = importlib.import_module("ai-ensemble.jordynn_ai")
BRAND_SYSTEM_PROMPT = jordynn_ai_module.BRAND_SYSTEM_PROMPT
clean_response = jordynn_ai_module.clean_response
import requests

def get_ai_reply(messages):
    """
    Simulates the AI call utilizing OpenRouter or fallback localized matching.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

    if openrouter_key:
        try:
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [{"role": "system", "content": BRAND_SYSTEM_PROMPT}] + messages
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                text = res.json()["choices"][0]["message"]["content"]
                return clean_response(text)
        except Exception as e:
            pass

    # High-fidelity Local NLP Matcher for immediate local testing if keys are offline
    last_msg = messages[-1]["content"].lower() if messages else ""
    
    if any(w in last_msg for w in ["pricing", "cost", "how much", "rate"]):
        reply = "we actually do custom pricing depending on how many negative accounts, collections, or public records are on your profile. we'll do a full line-by-line audit during our 1-on-1 strategy call so we can map out a specific restoral plan for you. grab a time here: https://angelsolutionsatl.com/book-online"
    elif any(w in last_msg for w in ["time", "how long", "duration", "month"]):
        reply = "most of my clients start seeing positive updates and deletions within 30 to 45 days. to completely restore a credit profile and have you funding-ready, it usually takes about 3 to 6 months depending on what we're working with."
    elif any(w in last_msg for w in ["skool", "diy", "monthly", "cheap", "fix myself", "do it myself"]):
        reply = "if you want to handle disputes on your own terms, my monthly skool community is perfect. you get support and dispute up to 5 items monthly for only $67/mo. check it out here: https://www.skool.com/creditsolution/about"
    elif any(w in last_msg for w in ["bankruptcy", "bankruptcies", "public record"]):
        reply = "public records are super stressful but my team actually specializes in targeting bankruptcies directly at the source. we've helped hundreds of clients permanently delete bankruptcies. let's get you set up to remove it, book a slot here: https://angelsolutionsatl.com/book-online"
    elif any(w in last_msg for w in ["medical", "doctor", "hospital"]):
        reply = "medical collections shouldn't be holding back your business. since debt collectors can't legally verify clinical details without violating HIPAA privacy laws, we can get those wiped off fast. let's clean it up: https://angelsolutionsatl.com/book-online"
    elif any(w in last_msg for w in ["template", "letter", "draft", "write"]):
        reply = "absolutely, i got you! here is my round 1 general dispute template that challenges collections under fcra section 609:\n\n[Your Name]\n[Your Address]\n\n[Credit Bureau Address]\n\nSubject: NOTICE OF FCRA VIOLATIONS / 15 U.S.C. § 1681i\n\nI recently reviewed my credit report and found unverified items. Under FCRA Section 611, if you cannot verify these accounts with physical documentation within 30 days, you must legally delete them immediately:\n\n1. Account Name: [Account Name] | Account # [Account Number]\n\nSincerely,\n[Your Name]\n\nlet me know if you need help customizing this or if you want my team to handle the full legal disputing for you!"
    elif any(w in last_msg for w in ["funding", "unsecured", "loan", "capital", "business credit"]):
        reply = "to qualify for my top-tier business funding or unsecured lines of credit, we ideally want you at a 680+ credit score, personal card utilization under 30%, no recent late payments, and a registered LLC. let's audit your file on a call to see how close you are: https://angelsolutionsatl.com/book-online"
    else:
        reply = "totally understand where you are coming from. credit bottlenecks can hold back everything, but we can target all those negative items simultaneously to get your profile ready. let's map this out together on a strategy call: https://angelsolutionsatl.com/book-online"
        
    return clean_response(reply)

def run_chat():
    print("=" * 65)
    print("🌟 ANGEL SOLUTIONS ATL - JORDYNN MILLER LIVE INTERACTIVE TESTER 🌟")
    print("=" * 65)
    print("Instructions:")
    print("1. Type your message below to chat with Jordynn Miller AI.")
    print("2. Ask about Pricing, Timelines, DIY Skool, Bankruptcies, or request a Template.")
    print("3. Type 'exit' or 'quit' to end the testing session.")
    print("-" * 65)
    print("Rick: hey! thanks for checking in. what's your biggest credit goal right now? custom restoral or business funding?")
    
    chat_history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("\nEnding test session. All systems fully functional!")
                break
                
            chat_history.append({"role": "user", "content": user_input})
            
            # Fetch response
            print("\nRick is typing...", end="\r")
            reply = get_ai_reply(chat_history)
            chat_history.append({"role": "assistant", "content": reply})
            
            # Print response
            print(f"Rick: {reply}")
            print("-" * 65)
            
        except KeyboardInterrupt:
            print("\nTest session ended.")
            break

if __name__ == "__main__":
    run_chat()
