# =====================================================================
# ANGEL SOLUTIONS ATL - INTERACTIVE PAYDEX SCORE SIMULATOR (V9.0)
# =====================================================================
# An elite interactive terminal tool designed to educate and qualify 
# business owners for top-tier corporate credit and unsecured funding.
# Simulates Dun & Bradstreet Paydex Score calculations based on vendor reporting.
# =====================================================================

import os
import sys
import time

# Terminal Colors
GOLD = "\033[93m"
AMBER = "\033[33m"
DARK_AMBER = "\033[31m"
GREEN = "\033[92m"
BLUE = "\033[94m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_paydex_status(score):
    if score >= 80:
        return f"{GREEN}EXCELLENT (Low Risk) - Fully Funding Ready!{RESET}"
    elif score >= 50:
        return f"{AMBER}MEDIUM (Moderate Risk) - Needs more reporting trade lines.{RESET}"
    else:
        return f"{DARK_AMBER}HIGH RISK - Action Required! Your business will likely face funding declines.{RESET}"

def run_simulator():
    clear_screen()
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"{BOLD}{GOLD}🌟    ANGEL SOLUTIONS ATL - INTERACTIVE PAYDEX SCORE SIMULATOR    🌟{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"Welcome! Let's calculate your Dun & Bradstreet Paydex Score and map out\nyour path to securing up to $150,000 in unsecured corporate funding.\n")

    vendors = {
        "1": {"name": "Quill Net-30", "reporting_days": 30, "tier": 1},
        "2": {"name": "Uline Net-30", "reporting_days": 30, "tier": 1},
        "3": {"name": "Grainger Net-30", "reporting_days": 30, "tier": 1},
        "4": {"name": "Home Depot Pro Revolving", "reporting_days": 30, "tier": 2},
        "5": {"name": "Amazon Business Revolving", "reporting_days": 30, "tier": 2},
        "6": {"name": "Divvy Corporate Card", "reporting_days": 30, "tier": 3},
        "7": {"name": "Stripe Corporate Card", "reporting_days": 30, "tier": 3}
    }

    selected_vendors = []
    
    print(f"{BOLD}{AMBER}Step 1: Select which Tier-1, Tier-2, and Tier-3 trade lines you have reporting:{RESET}")
    for key, value in vendors.items():
        print(f"  [{key}] {value['name']} (Tier {value['tier']})")
    
    print(f"  [D] Done selecting")

    while True:
        choice = input("\nEnter vendor number to toggle (or 'D' to continue): ").strip().upper()
        if choice == 'D':
            break
        if choice in vendors:
            v = vendors[choice]
            if v in selected_vendors:
                selected_vendors.remove(v)
                print(f"Removed: {v['name']}")
            else:
                selected_vendors.append(v)
                print(f"Added: {v['name']}")
        else:
            print("Invalid choice, try again.")

    clear_screen()
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"{BOLD}{GOLD}🌟               STEP 2: CHOOSE YOUR PAYMENT BEHAVIOR                🌟{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print("How many days before/after the net-30 invoice due date do you pay your bills?\n")
    print("  [1] 30 Days Early (Highly Proactive)")
    print("  [2] 20 Days Early")
    print("  [3] 10 Days Early")
    print("  [4] Exactly on the Due Date")
    print("  [5] 1-15 Days Late")
    print("  [6] 16-30 Days Late")

    behavior = input("\nEnter your choice [1-6]: ").strip()

    # Calculate Paydex Score based on payment behavior & vendor counts
    base_score = 30
    if behavior == "1":
        base_score = 100
    elif behavior == "2":
        base_score = 90
    elif behavior == "3":
        base_score = 85
    elif behavior == "4":
        base_score = 80
    elif behavior == "5":
        base_score = 50
    elif behavior == "6":
        base_score = 30

    # Adjust score slightly based on the number of reporting trade lines
    trade_count = len(selected_vendors)
    if trade_count == 0:
        final_score = 0
    elif trade_count < 3:
        final_score = max(0, base_score - 15)  # D&B requires at least 3 trade lines to compute a real score
    elif trade_count < 5:
        final_score = base_score
    else:
        final_score = min(100, base_score + 5)

    clear_screen()
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"{BOLD}{GOLD}🌟                    YOUR SIMULATED PAYDEX REPORT                   🌟{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"🏢 Business Profile: {BOLD}{os.getenv('BUSINESS_NAME', 'Angel Solutions ATL')}{RESET}")
    print(f"📊 Active reporting trade lines: {BOLD}{trade_count}{RESET}")
    print(f"⭐ Computed Paydex Score: {BOLD}{GOLD}{final_score}/100{RESET}")
    print(f"🛑 Status: {get_paydex_status(final_score)}")
    print(f"---------------------------------------------------------------------")

    # Tailored recommendations
    print(f"{BOLD}{AMBER}RECOMMENDED NEXT STEPS FOR YOUR FUNDING SUITE:{RESET}")
    if final_score >= 80:
        print(f"  ✅ You are in the elite tier! You are immediately eligible to apply")
        print(f"     for up to $100K in unsecured credit lines and corporate vehicle leases.")
        print(f"     Book your funding strategy call: https://angelsolutionsatl.com/book-online")
    elif final_score >= 50:
        print(f"  ⚠️ Action Needed: You have trade lines but need to scale to at least 5")
        print(f"     active trade lines reporting. Add Tier-2 revolving cards like Amazon Business.")
        print(f"     Let us help you structure this: https://angelsolutionsatl.com/book-online")
    else:
        print(f"  ❌ Action Required: D&B requires at least 3 active reporting trade lines")
        print(f"     and proactive payment histories to establish your Paydex score.")
        print(f"     We can build this out for you with our Step-by-Step Corporate Builder.")
        print(f"     Get started now: https://angelsolutionsatl.com/book-online")

    print(f"{BOLD}{GOLD}====================================================================={RESET}\n")

if __name__ == "__main__":
    run_simulator()
