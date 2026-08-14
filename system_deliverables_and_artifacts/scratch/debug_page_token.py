import urllib.request
import json
import urllib.error

app_id = "1037361725512008"
app_secret = "8291323937b56cec3edab60fc9f72a9a"
app_access_token = f"{app_id}|{app_secret}"
page_token = "EAAOveZAknGUgBSDZCbqMKjKXEZBr2NUmuhAZAJCdfonOJyoWnJUvepI3hEUqSezehmO7r5NdjKdZA9z63d4yNm7jJv4m2wbU9w5HVkIOKDzA38UrjfFuPr9HbNiLoWMzGObPkImcZA6TN649wM9ZAxllIQZAewwiDlqDhteOay7MjojNpGAPMXVLPlMY4M4567lMoD0ZD"

url = f"https://graph.facebook.com/v19.0/debug_token?input_token={page_token}&access_token={app_access_token}"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("Token Debug Information:")
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
