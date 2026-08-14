import urllib.request, urllib.parse, json

page_id = "107318795356062"
page_token = "EAAOveZAknGUgBSFv0kabDbEJksvwmZCG5KX3LZBPNKwptPeReCKvaWoB1U8HvoHbOuttWblH2D0YDRAawE5UBHx2sYBGDxLH6cVuEbMXREBe4tS02tuaBiW2Wot4RnhusaY7RBoQL7l0bUAlrYzjiIu2Gx9MNwBppupca4ZBHeMZAMfETHo9mx8uOlyQKf9BolvwvbEwZD"

# List of all fields including Instagram fields
fields = [
    "messages",
    "messaging_postbacks",
    "message_reads",
    "message_deliveries",
    "message_edits",
    "message_reactions",
    "instagram_messages",
    "instagram_messaging_postbacks",
    "instagram_message_reads",
    "instagram_message_deliveries"
]

fields_str = ",".join(fields)
url = f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps"

data = urllib.parse.urlencode({
    "access_token": page_token,
    "subscribed_fields": fields_str
}).encode("utf-8")

req = urllib.request.Request(url, data=data, method="POST", headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        print("[SUCCESS] Subscription response:", json.dumps(res_data, indent=2))
except urllib.error.HTTPError as e:
    print("[ERROR] HTTP Error:", e.read().decode("utf-8"))
except Exception as e:
    print("[ERROR] Exception:", e)
