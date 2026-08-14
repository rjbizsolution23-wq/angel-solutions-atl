import urllib.request
import urllib.error
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"

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
            
        print("Page Access Token successfully fetched.\n")
        
        # Endpoints to test
        endpoints = [
            f"{page_id}/instagram_secondary_receivers",
            f"{page_id}/secondary_receivers",
            f"{page_id}/roles"
        ]
        
        for ep in endpoints:
            print(f"Querying: https://graph.facebook.com/v19.0/{ep}...")
            url = f"https://graph.facebook.com/v19.0/{ep}?access_token={page_token}"
            try:
                ep_req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(ep_req) as ep_response:
                    data = json.loads(ep_response.read().decode("utf-8"))
                    print(f"Success:")
                    print(json.dumps(data, indent=2))
            except urllib.error.HTTPError as e:
                print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
            except Exception as e:
                print(f"Error: {e}")
            print("-" * 50)
            
except Exception as e:
    print(f"Error: {e}")
