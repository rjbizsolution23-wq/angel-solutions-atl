import json

log_path = "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log"

print("--- ALL RAW INBOUND WEBHOOK PAYLOADS ---")
try:
    content = open(log_path, "r", errors="ignore").read()
    # Find all occurrences of "Inbound raw webhook payload:"
    import re
    matches = re.findall(r'Inbound raw webhook payload:\s*(.*?)(?=\n\s*\}\s*,\s*\"level\"|\Z)', content, re.DOTALL)
    print(f"Found {len(matches)} payloads.")
    for i, m in enumerate(matches):
        print(f"\nPayload #{i+1}:")
        # Clean up escapes if it is a string inside JSON
        cleaned = m.strip()
        if cleaned.startswith('"') and cleaned.endswith('"'):
            # It's a quoted string, let's unquote it
            try:
                cleaned = json.loads(cleaned)
            except:
                pass
        try:
            parsed = json.loads(cleaned)
            print(json.dumps(parsed, indent=2))
        except Exception as e:
            print(f"Raw: {cleaned}")
            print(f"(Error parsing: {e})")
except Exception as e:
    print(f"Error: {e}")
