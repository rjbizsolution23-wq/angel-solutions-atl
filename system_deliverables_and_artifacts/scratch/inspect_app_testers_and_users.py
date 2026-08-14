import urllib.request
import urllib.error
import json

app_id = "1037361725512008"
app_secret = "8291323937b56cec3edab60fc9f72a9a"
app_access_token = f"{app_id}|{app_secret}"

endpoints = [
    f"{app_id}/instagram_testers",
    f"{app_id}/instagram_accounts",
    f"{app_id}/testers",
    f"{app_id}/developers",
    f"{app_id}/users"
]

print("--- SEARCHING FOR VALID ROLES/TESTERS ENDPOINTS ---")
for ep in endpoints:
    url = f"https://graph.facebook.com/v19.0/{ep}?access_token={app_access_token}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(f"\n[SUCCESS] Querying: {ep}")
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f"\n[HTTP Error {e.code}] Querying: {ep}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"\n[Error] Querying: {ep}: {e}")
