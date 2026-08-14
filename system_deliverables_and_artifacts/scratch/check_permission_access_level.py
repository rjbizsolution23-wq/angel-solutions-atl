import urllib.request
import json
import urllib.error

app_id = "1037361725512008"
system_token = "EAAOveZAknGUgBSKPZA72ZAS0ZAg6xigTkzkmy9c3HWBsZAOfDmZC5uyPrmTxy9HF1VfbyHpgVVUGq3bu7BnnlAf18PsumaRRLtFpEuZAM7zTzSOsD6JroZAB509ZBn550K5eR0KG2TpKvxhSKXHl9PC6jh1jkXLrzo4K3BqehdIMSReBnNSyZCI6FzSXM8X5O4NgZDZD"
page_token = "EAAOveZAknGUgBSDZCbqMKjKXEZBr2NUmuhAZAJCdfonOJyoWnJUvepI3hEUqSezehmO7r5NdjKdZA9z63d4yNm7jJv4m2wbU9w5HVkIOKDzA38UrjfFuPr9HbNiLoWMzGObPkImcZA6TN649wM9ZAxllIQZAewwiDlqDhteOay7MjojNpGAPMXVLPlMY4M4567lMoD0ZD"

for token_name, token in [("System Token", system_token), ("Page Token", page_token)]:
    print(f"\n--- QUERYING WITH {token_name} ---")
    url = f"https://graph.facebook.com/v19.0/{app_id}/permissions?access_token={token}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")
