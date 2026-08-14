import urllib.request
import json

url = "https://openrouter.ai/api/v1/models"
print("--- FETCHING CHEAP OPENROUTER MODELS ---")

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        models = data.get("data", [])
        cheap_models = []
        for model in models:
            pricing = model.get("pricing", {})
            prompt_price = float(pricing.get("prompt", 0)) * 1000000  # Convert to per million
            completion_price = float(pricing.get("completion", 0)) * 1000000
            
            if prompt_price <= 0.10 and completion_price <= 0.10:
                cheap_models.append((model.get("id"), model.get("name"), prompt_price, completion_price))
        
        print(f"\nFound {len(cheap_models)} models costing <= $0.10 per million tokens:")
        for cm in sorted(cheap_models, key=lambda x: x[2]):
            print(f"- {cm[0]} ({cm[1]}) | Prompt: ${cm[2]:.4f}/M, Completion: ${cm[3]:.4f}/M")
except Exception as e:
    print(f"FAILED: {e}")
