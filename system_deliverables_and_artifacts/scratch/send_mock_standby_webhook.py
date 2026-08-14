import urllib.request
import json
import time

payload = {
  "object": "instagram",
  "entry": [
    {
      "id": "17841417063408906",
      "time": int(time.time() * 1000),
      "standby": [
        {
          "sender": {
            "id": "17841401380565498"
          },
          "recipient": {
            "id": "17841417063408906"
          },
          "timestamp": int(time.time() * 1000),
          "message": {
            "mid": "mid.instagram_standby_id_" + str(time.time()),
            "text": "hey how does your program work? I want to see the AI response in my inbox!"
          }
        }
      ]
    }
  ]
}

url = "https://angel-solutions-webhook.rickjefferson.workers.dev/webhook"
data = json.dumps(payload).encode("utf-8")

req = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8")
        print(f"Response Status Code: {status_code}")
        print(f"Response Body: {body}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
