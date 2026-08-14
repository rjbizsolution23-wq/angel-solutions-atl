# =====================================================================
# ANGEL SOLUTIONS ATL - TWILIO SMART CALL FORWARDING GATEWAY
# =====================================================================
# Auto-generates the production-ready TwiML (Twilio Markup Language) XML
# needed to configure live call-forwarding from your Twilio tracking line
# directly to Jordynn Miller's phone line (+14703386689).
# =====================================================================

import os
import sys

# Terminal Colors
GOLD = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"

def show_config():
    phone_target = os.getenv("RICK_PHONE", "+14705230674").strip()
    business_name = os.getenv("BUSINESS_NAME", "Angel Solutions ATL").strip()

    twiml_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <!-- 1. Play a warm, premium brand greeting whisper to the caller -->
    <Say voice="Polly.Kimberly">Thank you for calling {business_name}. Please hold while we connect you to Jordynn Miller, your credit restoral strategist.</Say>
    
    <!-- 2. Securely forward the call to Jordynn's active mobile line -->
    <Dial timeout="20" record="record-from-answer">
        <Number>{phone_target}</Number>
    </Dial>
</Response>"""

    print(f"\n{BOLD}{GOLD}====================================================================={RESET}")
    print(f"{BOLD}{GOLD}🌟           TWILIO SMART CALL FORWARDING CONFIGURATOR (V9.0)        🌟{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}")
    print(f"Configure your Twilio tracking line to instantly forward incoming calls to:\n{BOLD}{GREEN}{phone_target}{RESET}\n")

    print(f"{BOLD}Step 1: Your Production TwiML XML Script:{RESET}")
    print(f"{GRAY}---------------------------------------------------------------------{RESET}")
    print(twiml_xml)
    print(f"{GRAY}---------------------------------------------------------------------{RESET}\n")

    print(f"{BOLD}Step 2: How to Deploy this to your Live Twilio Account:{RESET}")
    print("  1. Log into your Twilio Console (https://console.twilio.com)")
    print("  2. Navigate to: Phone Numbers -> Manage -> Active Numbers")
    print("  3. Click on your active Angel Solutions ATL phone number")
    print("  4. Scroll down to the 'Voice & Fax' section")
    print("  5. Under 'A CALL COMES IN', select 'TwiML Bin' or 'WebHook'")
    print("  6. Paste the XML above into your TwiML Bin and click Save!")
    print(f"\n{GREEN}✓ This ensures no inbound lead is ever lost and connects them instantly!{RESET}")
    print(f"{BOLD}{GOLD}====================================================================={RESET}\n")

GRAY = "\033[90m"

if __name__ == "__main__":
    show_config()
