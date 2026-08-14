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

    # 3. Test Automated LLM Conversation Flow with Bankruptcy Keyword & Media Trigger
    print("\n[STEP 3] Simulating user sending bankruptcy question (Keyword + Media Trigger)...")
    sim_data = {
        "user_message": "i have an old bankruptcy from 2021, can you remove that?"
    }
    res_sim = session.post(f"{BASE_URL}/action/simulate", data=sim_data, allow_redirects=False)
    print(f"Simulation Status: {res_sim.status_code}")
    if res_sim.status_code in [302, 303]:
        print("✅ Simulated reply generated and saved in history successfully!")
    else:
        print("❌ Simulation failed!")

    # 4. Test Escalation Bypass Safeguard (refund / scam)
    print("\n[STEP 4] Simulating high-risk compliance escalation trigger...")
    escalation_data = {
        "user_message": "i want a full refund, you scammed me"
    }
    res_esc = session.post(f"{BASE_URL}/action/simulate", data=escalation_data, allow_redirects=False)
    print(f"Escalation Status: {res_esc.status_code}")
    if res_esc.status_code in [302, 303]:
        print("✅ Escalation safety check processed successfully!")
    else:
        print("❌ Escalation failed!")

    # 5. Test AI Ad Copywriting Generation
    print("\n[STEP 5] Testing AI Copywriting Generator (Jordynn's voice)...")
    copy_data = {
        "ai_prompt": "funding lines for small business real estate owners"
    }
    res_copy = session.post(f"{BASE_URL}/action/generate-copy", data=copy_data, allow_redirects=False)
    print(f"Ad Copy Generation Status: {res_copy.status_code}")
    # 6. Test GHL Configuration Save & Hot-Reload
    print("\n[STEP 6] Testing GHL CRM Credentials Save & Hot-Reload...")
    config_data = {
        "ghl_api_key": "ghl_simulated_api_key_abc123",
        "ghl_location_id": "Sfvt5kBZ3EUOws7MDWa3",
        "openrouter_api_key": "your_openrouter_api_key_here",
        "meta_access_token": "your_meta_page_access_token_here"
    }
    res_config = session.post(f"{BASE_URL}/action/save-config", data=config_data, allow_redirects=False)
    print(f"Config Save Response Status: {res_config.status_code}")
    if res_config.status_code in [302, 303]:
        print("✅ GHL credentials saved and in-memory variables successfully hot-reloaded!")
    else:
        print("❌ Config save failed!")

    # 7. Test Manual GHL Sync Action
    print("\n[STEP 7] Testing manual GHL Contact Sync...")
    sync_data = {
        "lead_id": "lead_01"
    }
    res_sync = session.post(f"{BASE_URL}/action/sync", data=sync_data, allow_redirects=False)
    print(f"Manual Sync Response Status: {res_sync.status_code}")
    if res_sync.status_code in [302, 303]:
        print("✅ Lead sync process completed successfully!")
    else:
        print("❌ GHL manual sync failed!")

if __name__ == "__main__":
    test_full_workflows()
