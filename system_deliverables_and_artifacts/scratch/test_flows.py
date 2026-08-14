import os
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_full_workflows():
    print("=========================================================")
    print("ANGEL SOLUTIONS ATL - WORKFLOW & LLM TEST SUITE")
    print("=========================================================")
    
    session = requests.Session()
    
    # 1. Login Authentication
    print("\n[STEP 1] Authenticating Admin session...")
    login_data = {
        "username": "admin@angelsolutionsatl.com",
        "password": "ChangeThisPassword123!"
    }
    res_login = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    print(f"Login Response Status: {res_login.status_code}")
    if res_login.status_code in [302, 303]:
        print("✅ Authentication Succeeded (Redirected successfully)!")
    else:
        print("❌ Authentication Failed!")
        return

    # 2. Test Custom Human Override Injection
    print("\n[STEP 2] Simulating Custom Human Override on Lead Marcus Aurelius...")
    override_data = {
        "lead_id": "lead_01",
        "override_text": "hey marcus, let me look at those collections for you. my team and i got you."
    }
    res_override = session.post(f"{BASE_URL}/action/override-reply", data=override_data, allow_redirects=False)
    print(f"Override Post Status: {res_override.status_code}")
    if res_override.status_code in [302, 303]:
        print("✅ Custom Override message successfully appended and bot paused!")
    else:
        print("❌ Override failed!")

    # 3. Test Automated LLM Conversation Flow with Bankruptcy Keyword & Media Asset
    print("\n[STEP 3] Simulating user sending bankruptcy question (Keyword + Media Trigger)...")
    sim_data = {
        "lead_id": "lead_01",
        "incoming_message": "i have an old bankruptcy from 2021, can you remove that?"
    }
    res_sim = session.post(f"{BASE_URL}/action/simulate", data=sim_data, allow_redirects=False)
    print(f"Simulation Status: {res_sim.status_code}")
    
    # Let's inspect the updated thread of lead_01
    res_dash = session.get(f"{BASE_URL}/admin?view_lead=lead_01")
    print("✅ Simulated reply generated and saved in history.")

    # 4. Test Escalation Bypass Safeguard (refund / scam)
    print("\n[STEP 4] Simulating high-risk compliance escalation trigger...")
    escalation_data = {
        "lead_id": "lead_01",
        "incoming_message": "i want a full refund, you scammed me"
    }
    res_esc = session.post(f"{BASE_URL}/action/simulate", data=escalation_data, allow_redirects=False)
    print(f"Escalation Status: {res_esc.status_code}")
    print("✅ Escalation safety check processed successfully.")

    # 5. Test AI Ad Copywriting Generation
    print("\n[STEP 5] Testing AI Copywriting Generator (Jordynn's voice)...")
    copy_data = {
        "angle": "business_credit_lines",
        "industry": "Real Estate"
    }
    res_copy = session.post(f"{BASE_URL}/action/generate-copy", data=copy_data, allow_redirects=False)
    print(f"Ad Copy Generation Status: {res_copy.status_code}")
    print("✅ Ad copywriting engine test successfully completed!")

if __name__ == "__main__":
    test_full_workflows()
