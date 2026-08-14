import os
import sys

# Import our Rick AI core ensemble directly
sys.path.append(os.path.join(os.path.dirname(__file__), "../ai-ensemble"))
from jordynn_ai import generate_rick_response

def test_conversational_variety_direct():
    test_scenarios = [
        {
            "niche": "Trucking / Logistics",
            "message": "i'm trying to get funding for two semi trucks but my personal credit has late payments on a credit card from last year. can you help?"
        },
        {
            "niche": "Real Estate / DSCR",
            "message": "Hey Rick, me and my husband are looking to qualify for a hard money DSCR loan to flip a house but we have an old tax lien on our report. can this be cleared?"
        },
        {
            "niche": "Bankruptcy Roadblock",
            "message": "i got a chapter 7 bankruptcy that was discharged in 2022. it's killing my score and i can't get any business lines of credit. can you guys remove a bankruptcy?"
        },
        {
            "niche": "High Collections count (DIY Skool Pitch)",
            "message": "hi, i only have 2 collections of like $150 each, and i want to try to fix it myself if possible. do you have anything cheap?"
        },
        {
            "niche": "Stressed & Frustrated Lead (Escalation Path)",
            "message": "your automated system is annoying, let me speak to a human or refund my money now. I am tired of bots."
        },
        {
            "niche": "Pricing Inquiry",
            "message": "how much does it cost to work with you guys 1-on-1? what are your prices?"
        }
    ]
    
    print("======================================================================")
    print("🧪 EVALUATING OFFLINE DYNAMIC VARIETY & ADAPTIVE CONTEXT-AWARE ANALYSIS")
    print("======================================================================")
    
    for item in test_scenarios:
        niche = item["niche"]
        msg = item["message"]
        
        # Invoke our updated Rick AI Ensemble
        history = [{"role": "user", "content": msg}]
        result = generate_rick_response(history)
        reply = result.get("reply", "")
        
        print(f"\n📂 CATEGORY: [ {niche} ]")
        print(f"📥 USER SENT: '{msg}'")
        print(f"🤖 RICK AI REPLY: \"{reply}\"")
        print("—" * 70)

if __name__ == "__main__":
    test_conversational_variety_direct()
