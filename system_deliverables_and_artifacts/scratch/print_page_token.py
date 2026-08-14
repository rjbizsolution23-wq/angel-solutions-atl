import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"

page_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"

try:
    req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        page_data = json.loads(response.read().decode("utf-8"))
        page_token = page_data.get("access_token")
        if page_token:
            print("FETCHED_TOKEN:", page_token)
            print("LENGTH:", len(page_token))
            print("PREFIX:", page_token[:10])
            print("SUFFIX:", page_token[-10:])
        else:
            print("Failed to get Page Access Token.")
except Exception as e:
    print("Error:", e)
