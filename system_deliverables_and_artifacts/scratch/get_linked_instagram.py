import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"

print("--- FETCHING LINKED INSTAGRAM BUSINESS ACCOUNT ---")
url = f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account,name&access_token={system_token}"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("Page Details:")
        print(json.dumps(data, indent=2))
        
        ig_acct = data.get("instagram_business_account")
        if ig_acct:
            ig_id = ig_acct.get("id")
            print(f"\nQuerying details for Instagram ID: {ig_id}...")
            ig_url = f"https://graph.facebook.com/v19.0/{ig_id}?fields=username,name&access_token={system_token}"
            req_ig = urllib.request.Request(ig_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_ig) as response_ig:
                ig_data = json.loads(response_ig.read().decode("utf-8"))
                print("Instagram Details:")
                print(json.dumps(ig_data, indent=2))
        else:
            print("\n❌ No linked instagram_business_account found on this Page!")
except Exception as e:
    print(f"Error: {e}")
