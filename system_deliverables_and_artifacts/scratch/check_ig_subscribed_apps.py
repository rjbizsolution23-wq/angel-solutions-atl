import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"
ig_id = "17841417063408906"

print("--- FETCHING PAGE ACCESS TOKEN ---")
page_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"

try:
    req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        page_data = json.loads(response.read().decode("utf-8"))
        page_token = page_data.get("access_token")
        
        if not page_token:
            print("Failed to get Page Access Token.")
            exit(1)
            
        print("Page Access Token successfully fetched.")
        
        # Query IG Subscribed Apps
        print(f"\nChecking Subscribed Apps for Instagram Account {ig_id}...")
        url = f"https://graph.facebook.com/v19.0/{ig_id}/subscribed_apps?access_token={page_token}"
        sub_req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(sub_req) as sub_response:
            sub_data = json.loads(sub_response.read().decode("utf-8"))
            print("Instagram Subscribed Apps:")
            print(json.dumps(sub_data, indent=2))
            
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
