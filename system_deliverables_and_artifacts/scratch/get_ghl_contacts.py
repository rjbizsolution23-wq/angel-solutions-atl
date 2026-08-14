import requests
import json

url = "https://services.leadconnectorhq.com/contacts/"
headers = {
    "Authorization": "Bearer pit-c612b415-89da-40c4-85ee-60247ef49777",
    "Version": "2021-04-15"
}

def search_query(query):
    params = {
        "locationId": "Sfvt5kBZ3EUOws7MDWa3",
        "query": query,
        "limit": 20
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        contacts = data.get("contacts", [])
        print(f"\nFOUND {len(contacts)} CONTACTS FOR QUERY '{query}':")
        for c in contacts:
            c_id = c.get("id")
            name = c.get("contactName", "N/A")
            email = c.get("email", "None") or "None"
            phone = c.get("phone", "None") or "None"
            print(f"{c_id} | {name} | {email} | {phone}")
    except Exception as e:
        print(f"Error for '{query}': {e}")

if __name__ == "__main__":
    search_query("Jefferson")
    search_query("solutions")
