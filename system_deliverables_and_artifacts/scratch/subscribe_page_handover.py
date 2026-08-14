import urllib.request
import urllib.parse
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
            
        print("Page Access Token successfully fetched.")
        
        print("\nSubscribing Page to standard fields + standby + messaging_handovers...")
        sub_url = f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps?access_token={page_token}"
        
        fields = [
            "message_deliveries",
            "message_edits",
            "message_reactions",
            "message_reads",
            "messages",
            "messaging_postbacks",
            "standby",
            "messaging_handovers"
        ]
        
        post_data = urllib.parse.urlencode({
            "subscribed_fields": ",".join(fields)
        }).encode("utf-8")
        
        post_req = urllib.request.Request(sub_url, data=post_data, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(post_req) as post_response:
            res = json.loads(post_response.read().decode("utf-8"))
            print(f"Subscription POST Result: {res}")
            
        # Verify subscriptions
        print("\nVerifying current subscriptions...")
        verify_req = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(verify_req) as verify_response:
            verify_data = json.loads(verify_response.read().decode("utf-8"))
            print(json.dumps(verify_data, indent=2))
            
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
