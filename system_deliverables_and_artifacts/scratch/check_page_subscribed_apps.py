import urllib.request
import json

page_id = "107318795356062"
system_user_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"

url_page_token = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_user_token}"

try:
    req = urllib.request.Request(url_page_token, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode("utf-8"))
        page_access_token = res.get("access_token")
        print(f"Retrieved Page Access Token (starts with {page_access_token[:8]}...)")
        
        url_subscribed_apps = f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps?access_token={page_access_token}"
        req_sub = urllib.request.Request(url_subscribed_apps, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_sub) as r_sub:
            sub_res = json.loads(r_sub.read().decode("utf-8"))
            print("Subscribed Apps for Page:")
            print(json.dumps(sub_res, indent=2))
            
except Exception as e:
    print(f"Error: {e}")
