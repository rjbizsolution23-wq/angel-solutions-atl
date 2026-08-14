import urllib.request
import urllib.parse
import json

token = "4762116:ebcba757acecde41bbacaae8a41a2387"

def search_subscribers(name):
    print(f"\nSearching ManyChat subscribers for: '{name}'...")
    encoded_name = urllib.parse.quote(name)
    url = f"https://api.manychat.com/fb/subscriber/findByName?name={encoded_name}"
    
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("status") == "success":
                print("Results:")
                print(json.dumps(data, indent=2))
            else:
                print(f"Error: {data}")
    except Exception as e:
        print(f"Failed to query ManyChat: {e}")

if __name__ == "__main__":
    search_subscribers("Rick")
    search_subscribers("rickjeffsolutions")
