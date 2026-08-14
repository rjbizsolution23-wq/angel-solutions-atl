import json
import urllib.request
import urllib.error

TOKEN = "4762116:ebcba757acecde41bbacaae8a41a2387"
BASE_URL = "https://api.manychat.com"

endpoints = {
    "page_info": "/fb/page/getInfo",
    "custom_fields": "/fb/page/getCustomFields",
    "tags": "/fb/page/getTags",
    "flows": "/fb/page/getFlows"
}

results = {}

for name, endpoint in endpoints.items():
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            results[name] = data
            print(f"Success fetching {name}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e else ""
        results[name] = {"error": f"HTTPError {e.code}", "body": error_body}
        print(f"Error fetching {name}: {e.code} - {error_body}")
    except Exception as e:
        results[name] = {"error": str(e)}
        print(f"Error fetching {name}: {e}")

# Save the raw dump as an artifact so we can analyze it
with open("/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/scratch/manychat_dump.json", "w") as f:
    json.dump(results, f, indent=2)

print("Dump completed.")
