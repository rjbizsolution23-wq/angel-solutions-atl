import requests
import json

location_id = "Sfvt5kBZ3EUOws7MDWa3"
url = f"https://services.leadconnectorhq.com/locations/{location_id}"
headers = {
    "Authorization": "Bearer pit-c612b415-89da-40c4-85ee-60247ef49777",
    "Version": "2021-04-15"
}

try:
    response = requests.get(url, headers=headers)
    print("STATUS:", response.status_code)
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
