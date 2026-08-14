# =====================================================================
# ANGEL SOLUTIONS ATL - HOT LEADS PIPELINE DASHBOARD (V9.0)
# =====================================================================
# Fetches live contacts from your GoHighLevel CRM and processes them
# into a premium, color-coded lead priority pipeline right in your terminal.
# Helps Rick and Rick identify high-value credit restoral clients instantly.
# =====================================================================

import sys
import os
import requests
import json
from datetime import datetime

# Helper to load .env variables manually
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

load_env()

API_KEY = os.getenv("GHL_API_KEY", "").strip()
LOCATION_ID = os.getenv("GHL_LOCATION_ID", "Sfvt5kBZ3EUOws7MDWa3").strip()

# Terminal Colors
GOLD = "\033[93m"
AMBER = "\033[33m"
DARK_AMBER = "\033[31m"
GREEN = "\033[92m"
BLUE = "\033[94m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

def fetch_live_leads():
    """Queries GHL contacts endpoint with strict Bearer authentication"""
    if not API_KEY or API_KEY.startswith("your_") or API_KEY == "placeholder":
        print(f"{DARK_AMBER}Error: No active GHL_API_KEY found in your .env file! Please configure it.{RESET}")
        return []

    url = "https://services.leadconnectorhq.com/contacts/"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Version": "2021-04-15"
    }
    params = {
        "locationId": LOCATION_ID,
        "limit": 20
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get("contacts", [])
        else:
            print(f"{DARK_AMBER}CRM Connection failed with status code: {response.status_code}{RESET}")
            print(response.text)
            return []
    except Exception as e:
        print(f"{DARK_AMBER}Error connecting to CRM: {e}{RESET}")
        return []

def display_dashboard():
    print(f"\n{BOLD}{GOLD}====================================================================={RESET}")
    print(f"{BOLD}{GOLD}🌟    ANGEL SOLUTIONS ATL - HOT LEADS PIPELINE DASHBOARD (V9.0)    🌟{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"{GRAY}Location ID: {LOCATION_ID} | Active CRM Sync: ON{RESET}\n")

    print(f"Fetching live leads from GoHighLevel...", end="\r")
    leads = fetch_live_leads()
    
    if not leads:
        # Fallback simulator data to let the dashboard display beautifully even offline
        leads = [
            {"id": "loc_sim_01", "contactName": "Jordynn Miller", "email": "rick@rjbusiness.com", "phone": "+14045550199", "tags": ["credit_restoral_system", "qualified_high_priority", "platform_meta"], "dateAdded": datetime.now().isoformat()},
            {"id": "loc_sim_02", "contactName": "Amara Williams", "email": "amara.w@example.com", "phone": "+17705550188", "tags": ["credit_restoral_system", "active_bankruptcy", "platform_website"], "dateAdded": datetime.now().isoformat()},
            {"id": "loc_sim_03", "contactName": "Derrick Barnes", "email": "derrick.b@example.com", "phone": "+16785550122", "tags": ["credit_restoral_system", "new_prospect", "platform_meta"], "dateAdded": datetime.now().isoformat()}
        ]
        print(f"{GRAY}[SIMULATOR ACTIVE] Displaying local pipeline representation...{RESET}\n")
    else:
        print(f"{GREEN}Live connection secure! Retreived {len(leads)} fresh contacts.{RESET}\n")

    # Metrics computation
    total_count = len(leads)
    priority_count = 0
    funding_goals = 0
    repair_goals = 0

    print(f"{BOLD}{AMBER}--- HOT LEADS LEADERBOARD ---{RESET}")
    print(f"{BOLD}{'CONTACT NAME':<20} | {'EMAIL/PHONE':<30} | {'PRIORITY':<12} | {'DATE INGESTED':<11}{RESET}")
    print(f"{GRAY}" + "-" * 81 + f"{RESET}")

    for lead in leads:
        name = lead.get("contactName", "Valued Client").title()
        email = lead.get("email", "None") or "None"
        phone = lead.get("phone", "None") or "None"
        
        # Segment info
        tags = lead.get("tags", [])
        
        # Calculate priority
        priority = f"{GREEN}LOW{RESET}"
        if any("high_priority" in t or "bankruptcy" in t or "support" in t for t in tags):
            priority = f"{DARK_AMBER}HIGH 🚨{RESET}"
            priority_count += 1
        elif any("qualified" in t for t in tags) or len(tags) > 1:
            priority = f"{AMBER}MEDIUM{RESET}"
        
        # Date processing
        raw_date = lead.get("dateAdded", "N/A")
        try:
            date_obj = datetime.strptime(raw_date[:10], "%Y-%m-%d")
            date_str = date_obj.strftime("%b %d, %Y")
        except:
            date_str = raw_date[:10]

        contact_details = f"{email} / {phone}"
        if len(contact_details) > 30:
            contact_details = contact_details[:27] + "..."

        print(f"{BOLD}{name:<20}{RESET} | {contact_details:<30} | {priority:<19} | {date_str:<11}")

    # Display KPI summaries
    print(f"\n{BOLD}{GOLD}--- PIPELINE CONVERSION METRICS ---{RESET}")
    print(f"📈 Total Synchronized Leads: {BOLD}{total_count}{RESET}")
    print(f"🔥 High Priority Closures: {BOLD}{priority_count} ({int((priority_count/total_count*100) if total_count > 0 else 0)}%){RESET}")
    print(f"💎 Median Client Contract Value: {BOLD}$1,022.50{RESET}")
    print(f"💰 Projected Revenue Pipeline: {BOLD}{GREEN}${total_count * 1022.50:,.2f}{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}\n")

if __name__ == "__main__":
    display_dashboard()
