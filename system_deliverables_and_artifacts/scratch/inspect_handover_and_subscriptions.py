import urllib.request
import urllib.error
import json

page_id = "107318795356062"
ig_business_id = "17841417063408906"
page_token = "EAAOveZAknGUgBSDZCbqMKjKXEZBr2NUmuhAZAJCdfonOJyoWnJUvepI3hEUqSezehmO7r5NdjKdZA9z63d4yNm7jJv4m2wbU9w5HVkIOKDzA38UrjfFuPr9HbNiLoWMzGObPkImcZA6TN649wM9ZAxllIQZAewwiDlqDhteOay7MjojNpGAPMXVLPlMY4M4567lMoD0ZD"
system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"

def make_request(url, method="GET", data=None):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return None, f"HTTP {e.code}: {body}"
    except Exception as e:
        return None, str(e)

print("=== 1. VERIFY PAGE AND GET DETAILS ===")
res, err = make_request(f"https://graph.facebook.com/v19.0/{page_id}?fields=id,name,username,link&access_token={page_token}")
if err:
    print("Page details error:", err)
else:
    print(json.dumps(res, indent=2))

print("\n=== 2. CHECK PAGE SUBSCRIBED APPS ===")
res, err = make_request(f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps?access_token={page_token}")
if err:
    print("Subscribed apps error:", err)
else:
    print(json.dumps(res, indent=2))

print("\n=== 3. CHECK HANDOVER PROTOCOL SETTINGS ===")
res, err = make_request(f"https://graph.facebook.com/v19.0/{page_id}?fields=primary_receiver_app_id,secondary_receiver_app_ids&access_token={page_token}")
if err:
    print("Handover settings error:", err)
else:
    print(json.dumps(res, indent=2))

print("\n=== 4. VERIFY INSTAGRAM BUSINESS ACCOUNT ===")
res, err = make_request(f"https://graph.facebook.com/v19.0/{ig_business_id}?fields=id,username,name&access_token={page_token}")
if err:
    print("Instagram business account error:", err)
else:
    print(json.dumps(res, indent=2))
