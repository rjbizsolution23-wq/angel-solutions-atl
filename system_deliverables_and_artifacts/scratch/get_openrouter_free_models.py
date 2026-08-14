import urllib.request
import json

url = "https://openrouter.ai/api/v1/models"
print("--- FETCHING ACTIVE OPENROUTER FREE MODELS ---")

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        models = data.get("data", [])
        free_models = []
        for model in models:
            pricing = model.get("pricing", {})
            prompt_price = float(pricing.get("prompt", 0))
            completion_price = float(pricing.get("completion", 0))
            if prompt_price == 0.0 and completion_price == 0.0:
                free_models.append(model)
        
        print(f"\nFound {len(free_models)} free models:")
        for fm in sorted(free_models, key=lambda x: x.get("id", "")):
            print(f"- {fm.get('id')} (Name: {fm.get('name')})")
except Exception as e:
    print(f"FAILED: {e}")
