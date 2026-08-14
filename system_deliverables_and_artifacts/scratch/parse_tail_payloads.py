import json
import re

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
            
        # Wrangler tail logs are JSON objects. Let's find all logs.
        # Inside each JSON log of wrangler tail, there is:
        # "logs": [ { "message": [ "Inbound raw webhook payload:", "{...}" ], ... } ]
        # Let's find matches.
        matches = re.finditer(r'"Inbound raw webhook payload:",\s*"([^"]+)"', content)
        count = 0
        for match in matches:
            count += 1
            payload_str = match.group(1).replace('\\"', '"').replace('\\\\', '\\')
            print(f"\n[Payload #{count}]")
            try:
                payload_json = json.loads(payload_str)
                print(json.dumps(payload_json, indent=2))
            except Exception:
                # Sometimes payload string itself is escaped multiple times.
                # Let's clean up backslashes.
                clean_str = payload_str.replace('\\"', '"').replace('\\\\"', '"').replace('\\/', '/')
                try:
                    payload_json = json.loads(clean_str)
                    print(json.dumps(payload_json, indent=2))
                except Exception:
                    print(payload_str[:500] + "...")
        print(f"\nTotal payloads extracted from this file: {count}")
    except Exception as e:
        print(f"Error parsing {log_file}: {e}")
