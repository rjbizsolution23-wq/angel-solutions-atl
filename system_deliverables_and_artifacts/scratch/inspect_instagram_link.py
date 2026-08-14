import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"

print("--- INSPECTING INSTAGRAM CONNECTED ACCOUNT ---")

# 1. Query connected Instagram account
url = f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account,connected_instagram_account,name,access_token&access_token={system_token}"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("Page Details:")
        print(f"Name: {data.get('name')}")
        print(f"Instagram Business Account (fields=instagram_business_account): {data.get('instagram_business_account')}")
        print(f"Connected Instagram Account (fields=connected_instagram_account): {data.get('connected_instagram_account')}")
        page_token = data.get("access_token")
        
        # 2. Check if subscribed to webhooks
        if page_token:
            sub_url = f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps?access_token={page_token}"
            sub_req = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(sub_req) as sub_response:
                sub_data = json.loads(sub_response.read().decode("utf-8"))
                print("\nSubscribed Apps for Page:")
                print(json.dumps(sub_data, indent=2))
except Exception as e:
    print(f"Error: {e}")
