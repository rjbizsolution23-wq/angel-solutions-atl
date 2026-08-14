import urllib.request
import json

system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_id = "107318795356062"
ig_id = "17841417063408906"

# 1. Fetch Page Token
page_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={system_token}"
try:
    req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        page_data = json.loads(response.read().decode("utf-8"))
        page_token = page_data.get("access_token")
        
        if not page_token:
            print("Failed to get Page Access Token.")
            exit(1)
            
        print("Page Access Token successfully fetched.")
        
        # 2. Check current subscriptions for Instagram Business Account
        ig_sub_url = f"https://graph.facebook.com/v19.0/{ig_id}/subscribed_apps?access_token={page_token}"
        print(f"\nChecking active subscribed apps for Instagram Business Account: {ig_id}...")
        try:
            ig_req = urllib.request.Request(ig_sub_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(ig_req) as ig_response:
                ig_data = json.loads(ig_response.read().decode("utf-8"))
                print("Current Instagram Subscriptions:")
                print(json.dumps(ig_data, indent=2))
        except urllib.error.HTTPError as e_ig:
            err_body = e_ig.read().decode("utf-8")
            print(f"Failed to check IG subscriptions (HTTP {e_ig.code}): {err_body}")
        except Exception as e_ig:
            print(f"Failed to check IG subscriptions (generic): {e_ig}")
            
        # 3. Try using different subscription fields or endpoints if needed
        # Often, we also need to subscribe the app to the IG ID using user access token or page token.
        print("\nSubscribing Instagram Business Account to the App...")
        sub_post_url = f"https://graph.facebook.com/v19.0/{ig_id}/subscribed_apps?access_token={page_token}"
        post_data = urllib.parse.urlencode({
            "subscribed_fields": "messages,messaging_postbacks,messaging_seen,comments"
        }).encode("utf-8")
        
        try:
            post_req = urllib.request.Request(sub_post_url, data=post_data, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(post_req) as post_response:
                res = json.loads(post_response.read().decode("utf-8"))
                print(f"Subscription POST Result: {res}")
        except urllib.error.HTTPError as e_post:
            err_body = e_post.read().decode("utf-8")
            print(f"Failed to subscribe IG Account (HTTP {e_post.code}): {err_body}")
        except Exception as e_post:
            print(f"Failed to subscribe IG Account (generic): {e_post}")

except Exception as e:
    print(f"Error fetching page token: {e}")
