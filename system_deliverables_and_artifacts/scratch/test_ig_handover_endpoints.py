import urllib.request
import urllib.error
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"
ig_id = "17841417063408906"

# Fetch page access token first
page_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"

try:
    req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        page_data = json.loads(response.read().decode("utf-8"))
        page_token = page_data.get("access_token")
        
        # Test 1: Query secondary_receivers on IG Business Account
        print("\n--- TEST 1: secondary_receivers connection on IG Business Account ---")
        url1 = f"https://graph.facebook.com/v19.0/{ig_id}/secondary_receivers?access_token={page_token}"
        try:
            req1 = urllib.request.Request(url1, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req1) as resp1:
                print("Test 1 Success:")
                print(json.dumps(json.loads(resp1.read().decode("utf-8")), indent=2))
        except urllib.error.HTTPError as e:
            print(f"Test 1 HTTP Error {e.code}: {e.read().decode('utf-8')}")
            
        # Test 2: Query roles connection on Page
        print("\n--- TEST 2: roles connection on Page ---")
        url2 = f"https://graph.facebook.com/v19.0/{page_id}/roles?access_token={page_token}"
        try:
            req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req2) as resp2:
                print("Test 2 Success:")
                print(json.dumps(json.loads(resp2.read().decode("utf-8")), indent=2))
        except urllib.error.HTTPError as e:
            print(f"Test 2 HTTP Error {e.code}: {e.read().decode('utf-8')}")

        # Test 3: Query roles connection on IG Business Account
        print("\n--- TEST 3: roles connection on IG Business Account ---")
        url3 = f"https://graph.facebook.com/v19.0/{ig_id}/roles?access_token={page_token}"
        try:
            req3 = urllib.request.Request(url3, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req3) as resp3:
                print("Test 3 Success:")
                print(json.dumps(json.loads(resp3.read().decode("utf-8")), indent=2))
        except urllib.error.HTTPError as e:
            print(f"Test 3 HTTP Error {e.code}: {e.read().decode('utf-8')}")

except Exception as e:
    print(f"General Error: {e}")
