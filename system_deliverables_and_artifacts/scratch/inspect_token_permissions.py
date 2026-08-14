import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"

print("--- DEBAGING SYSTEM USER TOKEN PERMISSIONS ---")

url = f"https://graph.facebook.com/v19.0/me/permissions?access_token={system_token}"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("Permissions:")
        for perm in data.get("data", []):
            if perm.get("status") == "granted":
                print(f"✅ {perm.get('permission')}")
            else:
                print(f"❌ {perm.get('permission')} ({perm.get('status')})")
except Exception as e:
    print(f"Error: {e}")
