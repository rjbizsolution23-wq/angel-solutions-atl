import urllib.request
import urllib.parse
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"
target_psid = "28348939328024251"

print("--- FETCHING PAGE ACCESS TOKEN ---")
page_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"

try:
    req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode("utf-8"))
        page_access_token = res.get("access_token")
        print(f"Retrieved Page Access Token (starts with {page_access_token[:10]}...)")
        
        # Now try to send a message using the page access token
        send_url = f"https://graph.facebook.com/v19.0/me/messages?access_token={page_access_token}"
        payload = {
            "recipient": {"id": target_psid},
            "message": {"text": "Hello! This is a test message from your Angel Solutions Assistant to verify delivery."}
        }
        
        data = json.dumps(payload).encode("utf-8")
        send_req = urllib.request.Request(
            send_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
        )
        
        print("\n--- SENDING MESSAGE TO META GRAPH API ---")
        with urllib.request.urlopen(send_req) as send_r:
            send_res = json.loads(send_r.read().decode("utf-8"))
            print("Response from Meta:")
            print(json.dumps(send_res, indent=2))

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
