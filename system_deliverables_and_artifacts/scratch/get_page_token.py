import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"

page_ids = ["107318795356062", "903333065815207"]

print("--- EXCHANGING SYSTEM TOKEN FOR PERMANENT PAGE TOKENS ---")

for page_id in page_ids:
    url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token,name,username&access_token={system_token}"
    print(f"\nQuerying Page ID: {page_id}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(f"SUCCESS!")
            print(f"Page Name: {data.get('name')}")
            print(f"Page Username: {data.get('username')}")
            page_token = data.get("access_token")
            if page_token:
                print(f"PERMANENT PAGE ACCESS TOKEN:\n{page_token}")
            else:
                print("No access_token found in the response (the System User may not have full control assigned for this page).")
    except Exception as e:
        print(f"FAILED for Page ID {page_id}: {e}")
