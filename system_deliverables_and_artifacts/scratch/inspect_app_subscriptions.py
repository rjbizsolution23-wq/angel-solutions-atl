import urllib.request
import json

app_id = "509205838275077"
app_secret = "e2c19bbebf79eb4f017ba02fb30d16ff"
app_access_token = f"{app_id}|{app_secret}"

print("--- INSPECTING INSTAGRAM APP WEBHOOK SUBSCRIPTIONS ONLY ---")
url = f"https://graph.facebook.com/v19.0/{app_id}/subscriptions?access_token={app_access_token}"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        ig_subs = [s for s in data.get("data", []) if s.get("object") == "instagram"]
        if ig_subs:
            print(json.dumps(ig_subs, indent=2))
        else:
            print("No instagram object subscriptions found!")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
