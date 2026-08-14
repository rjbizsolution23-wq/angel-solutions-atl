import requests
import re

BASE_URL = "http://127.0.0.1:8000"

def inspect_results():
    session = requests.Session()
    
    # 1. Login
    login_data = {
        "username": "admin@angelsolutionsatl.com",
        "password": "ChangeThisPassword123!"
    }
    session.post(f"{BASE_URL}/login", data=login_data)
    
    # 2. Get Lead Marcus Aurelius Thread
    res = session.get(f"{BASE_URL}/admin?view_lead=lead_01")
    html = res.text
    
    print("=========================================================")
    print("MARCUS AURELIUS WORKFLOW HISTORY:")
    print("=========================================================")
    
    # Find all chat bubbles in the conversation thread card
    bubbles = re.findall(r'<div class="chat-bubble (.*?)">(.*?)</div>', html, re.DOTALL)
    for i, (bubble_class, content) in enumerate(bubbles, 1):
        clean_class = bubble_class.replace('"', '').strip()
        # Extract tag and text
        tag_match = re.search(r'<span class="bubble-tag"[^>]*>(.*?)</span>', content, re.DOTALL)
        p_match = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
        
        tag = tag_match.group(1).strip() if tag_match else "SENDER"
        text = p_match.group(1).strip() if p_match else content.strip()
        # Remove any span/inline tags from text
        text = re.sub(r'<[^>]+>', '', text).strip()
        
        print(f"[{tag}] ({clean_class}): {text}")
        print("-" * 50)

    print("\n=========================================================")
    print("SIMULATION PLAYGROUND HISTORY:")
    print("=========================================================")
    
    # Extract simulation playground groups
    sim_groups = re.findall(r'<div class="simulation-bubble-group">(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
    if not sim_groups:
        # Fallback search
        sim_groups = re.findall(r'<div class="simulation-bubble-group">(.*?)</div>\s*</div>\s*</div>', html + "</div></div>", re.DOTALL)
        
    # Let's search inside the HTML for the simulation bubbles directly
    sim_bubbles = re.findall(r'<div class="chat-bubble user-bubble">.*?<p>(.*?)</p>.*?<div class="chat-bubble bot-bubble">.*?<p>(.*?)</p>.*?<div class="reply-meta">(.*?)</div>', html, re.DOTALL)
    for msg_user, msg_bot, meta in sim_bubbles:
        clean_user = re.sub(r'<[^>]+>', '', msg_user).strip()
        clean_bot = re.sub(r'<[^>]+>', '', msg_bot).strip()
        clean_meta = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', meta)).strip()
        print(f"USER: {clean_user}")
        print(f"BOT (RICK'S VOICE): {clean_bot}")
        print(f"META: {clean_meta}")
        print("—" * 50)

if __name__ == "__main__":
    inspect_results()
