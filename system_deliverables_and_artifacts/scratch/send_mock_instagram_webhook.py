import urllib.request
import json
import time

payload = {
  "object": "instagram",
  "entry": [
    {
      "id": "17841417063408906",
      "time": 1721583018414,
      "messaging": [
        {
          "sender": {
            "id": "test_instagram_user_id"
          },
          "recipient": {
            "id": "17841417063408906"
          },
          "timestamp": 1721583018414,
          "message": {
            "mid": "mid.instagram_test_message_id_" + str(time.time()),
            "text": "hey how does your program work?"
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
