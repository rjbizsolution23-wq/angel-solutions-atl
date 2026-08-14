import urllib.request
import json

# Dynamically fetched active Page Access Token
page_tok = 'EAAOveZAknGUgBSDZCbqMKjKXEZBr2NUmuhAZAJCdfonOJyoWnJUvepI3hEUqSezehmO7r5NdjKdZA9z63d4yNm7jJv4m2wbU9w5HVkIOKDzA38UrjfFuPr9HbNiLoWMzGObPkImcZA6TN649wM9ZAxllIQZAewwiDlqDhteOay7MjojNpGAPMXVLPlMY4M4567lMoD0ZD'
target_psid = '28348939328024251' # Ricky's active Facebook PSID

send_url = f"https://graph.facebook.com/v19.0/me/messages?access_token={page_tok}"
payload = {
    "recipient": {"id": target_psid},
    "message": {"text": "Yo Ricky! This is a test message from your live Angel Solutions assistant. If you see this, the dynamically generated page access token is fully authorized and working!"}
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    send_url,
    data=data,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
)

print("--- SENDING DIRECT INSTAGRAM/FACEBOOK MESSAGE ---")
try:
    with urllib.request.urlopen(req) as r:
        print("[SUCCESS] Response:", json.loads(r.read().decode("utf-8")))
except urllib.error.HTTPError as e:
    print("[HTTP ERROR]:", e.read().decode("utf-8"))
except Exception as e:
    print("[ERROR]:", e)
