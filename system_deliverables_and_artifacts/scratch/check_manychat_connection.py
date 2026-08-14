import urllib.request
import json

def verify_manychat():
    token = "4762116:ebcba757acecde41bbacaae8a41a2387"
    url = "https://api.manychat.com/fb/page/getInfo"
    
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("status") == "success":
                print(f"[SUCCESS] ManyChat API Token Verified!")
                page_info = data.get("data", {})
                print(f"Page Name: {page_info.get('name')}")
                print(f"Page ID: {page_info.get('id')}")
                print(f"Currency: {page_info.get('currency')}")
            else:
                print(f"[ERROR] ManyChat returned unsuccessful status: {data}")
    except Exception as e:
        print(f"[CONNECTION ERROR] Failed to connect to ManyChat API: {e}")

if __name__ == "__main__":
    verify_manychat()
