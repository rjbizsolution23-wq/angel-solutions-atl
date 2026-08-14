import urllib.request
import json
import urllib.parse

app_id = "1037361725512008"
app_secret = "8291323937b56cec3edab60fc9f72a9a"
app_access_token = f"{app_id}|{app_secret}"

callback_url = "https://angel-solutions-webhook.rickjefferson.workers.dev/webhook"
verify_token = "ANGEL_SOLUTIONS_VERIFY_TOKEN_2026"

print(f"--- SUBSCRIBING APP {app_id} TO INSTAGRAM WEBHOOKS WITH STANDBY ---")

url = f"https://graph.facebook.com/v19.0/{app_id}/subscriptions"

# Let's try adding standby and checking if it's supported
post_data = urllib.parse.urlencode({
    "object": "instagram",
    "callback_url": callback_url,
    "verify_token": verify_token,
    "fields": "messages,messaging_postbacks,comments,mentions,standby,messaging_handover,message_reactions",
    "access_token": app_access_token
}).encode("utf-8")

try:
    req = urllib.request.Request(url, data=post_data, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("Success! App Subscribed to Instagram Webhooks:")
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
