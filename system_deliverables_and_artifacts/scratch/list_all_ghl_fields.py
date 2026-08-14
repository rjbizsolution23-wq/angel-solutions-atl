import requests

location_id = "Sfvt5kBZ3EUOws7MDWa3"
url = f"https://services.leadconnectorhq.com/locations/{location_id}/customFields"
headers = {
    "Authorization": "Bearer pit-c612b415-89da-40c4-85ee-60247ef49777",
    "Version": "2021-04-15"
}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    fields = data.get("customFields", [])
    print(f"Total custom fields: {len(fields)}")
    for f in fields:
        print(f"ID: {f['id']} | Name: {f['name']} | Key: {f['fieldKey']}")
except Exception as e:
    print("Error:", e)
