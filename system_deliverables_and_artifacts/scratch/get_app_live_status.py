import urllib.request
import json

app_id = "1037361725512008"
app_secret = "8291323937b56cec3edab60fc9f72a9a"
app_access_token = f"{app_id}|{app_secret}"

# We can query fields like 'name', 'category', 'link', 'logo_url', 'privacy_policy_url', 'terms_of_service_url'
url = f"https://graph.facebook.com/v19.0/{app_id}?fields=name,category,link,privacy_policy_url,terms_of_service_url&access_token={app_access_token}"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("App Settings:")
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
