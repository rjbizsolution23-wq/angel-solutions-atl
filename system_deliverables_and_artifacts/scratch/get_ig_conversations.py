import urllib.request
import urllib.error
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"
ig_id = "17841417063408906"

print("--- FETCHING PAGE ACCESS TOKEN ---")
page_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"

try:
    req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode("utf-8"))
        page_access_token = res.get("access_token")
        
        print("\n--- FETCHING INSTAGRAM CONVERSATIONS ---")
        url_conv = f"https://graph.facebook.com/v19.0/{ig_id}/conversations?fields=participants,updated_time,messages.limit(1){{message,from,to}}&access_token={page_access_token}"
        req_conv = urllib.request.Request(url_conv, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_conv) as r_conv:
            conv_data = json.loads(r_conv.read().decode("utf-8"))
            print("Conversations list:")
            print(json.dumps(conv_data, indent=2))
            
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
