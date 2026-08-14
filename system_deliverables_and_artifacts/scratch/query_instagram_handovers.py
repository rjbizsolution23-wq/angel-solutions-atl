import urllib.request
import urllib.error
import json

page_id = "107318795356062"
system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"

url_page_token = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"

try:
    req = urllib.request.Request(url_page_token, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode("utf-8"))
        page_access_token = res.get("access_token")
        
        # Query instagram_messaging_handovers
        print("--- QUERYING INSTAGRAM MESSAGING HANDOVERS ---")
        url_handovers = f"https://graph.facebook.com/v19.0/{page_id}/instagram_messaging_handovers?access_token={page_access_token}"
        req_handover = urllib.request.Request(url_handovers, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_handover) as r_hand:
            handovers_res = json.loads(r_hand.read().decode("utf-8"))
            print("Instagram Messaging Handovers:")
            print(json.dumps(handovers_res, indent=2))
            
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
