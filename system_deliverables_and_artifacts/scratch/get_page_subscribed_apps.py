import urllib.request
import json

page_token = "EAAOveZAknGUgBSGmHSDCPcmVFFURiynqWSwSniSvR3NfDgoCFQiwbQuHHPbk4W2LYvc6V053ebqZBgOw0qrYJxIoUCt88ZBlD7ZAtQocSn9uXpRB0z4LzR7sP5NJjcFEfJTwNobTPaNJs1aFHFMrXlgmUZCe5nsW0hmyo18SH9P33WbjVumpyYRx2xu0PaiZBOdMnHCokZD"
page_id = "107318795356062"

print(f"--- INSPECTING SUBSCRIBED APPS FOR PAGE {page_id} WITH PAGE TOKEN ---")
url = f"https://graph.facebook.com/v19.0/{page_id}/subscribed_apps?access_token={page_token}"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
