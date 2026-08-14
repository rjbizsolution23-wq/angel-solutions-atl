import urllib.request
import json

worker_url = "https://angel-solutions-webhook.rickjefferson.workers.dev/webhook"

# Mock Instagram DM webhook payload
payload = {
    "object": "instagram",
    "entry": [
        {
            "id": "17841417063408906",
            "time": 1784865796949,
            "messaging": [
                {
                    "sender": {
                        "id": "MOCK_SENDER_RJ_9999"
                    },
                    "recipient": {
                        "id": "17841417063408906"
                    },
                    "timestamp": 1784865796949,
                    "message": {
                        "mid": f"mock_mid_{int(urllib.request.time.time())}",
                        "text": "skool"
                    }
                }
            ]
        }
    ]
}

print(f"Sending mock Instagram DM to worker: {worker_url}")
try:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        worker_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    )
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode("utf-8"))
        print("\nWorker Ingestion Response:")
        print(json.dumps(res, indent=2))
except Exception as e:
    print(f"Error: {e}")
