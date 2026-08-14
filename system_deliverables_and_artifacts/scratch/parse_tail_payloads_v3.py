import re
import json

log_files = [
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log",
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9181.log"
]

for log_file in log_files:
    print(f"\n=======================================================")
    print(f"PARSING LOG FILE: {log_file}")
    print(f"=======================================================")
    try:
        with open(log_file, "r") as f:
            content = f.read()
            
        # Let's search for "Inbound raw webhook payload:" in the file and capture what comes next in the message list
        # In a JSON array, it looks like:
        # "message": [
        #     "Inbound raw webhook payload:",
        #     "{\"object\":\"instagram\",\"entry\":...}"
        # ]
        matches = re.findall(r'"Inbound raw webhook payload:",\s*"([^"]+)"', content)
        for i, m in enumerate(matches):
            print(f"\nMatch #{i+1}:")
            # Unescape backslashes and quotes
            try:
                # The string 'm' has escaped characters (like \", \n, \\)
                # Let's decode it as a JSON string to get the actual string value
                decoded = json.loads(f'"{m}"')
                # Now decoded is the raw JSON string payload. Let's parse and pretty print it.
                payload_json = json.loads(decoded)
                print(json.dumps(payload_json, indent=2))
            except Exception as e:
                # Fallback to direct replacement
                print(f"Failed decoding as JSON string: {e}")
                clean = m.replace('\\"', '"').replace('\\\\', '\\')
                try:
                    print(json.dumps(json.loads(clean), indent=2))
                except Exception:
                    print(clean[:1000])
                    
    except Exception as e:
        print(f"Error parsing {log_file}: {e}")
