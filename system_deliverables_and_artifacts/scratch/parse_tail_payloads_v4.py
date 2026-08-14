import json

log_files = [
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log",
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9181.log"
]

def parse_json_objects(text):
    """
    Decodes consecutive JSON objects from a text.
    """
    decoder = json.JSONDecoder()
    pos = 0
    text = text.strip()
    while pos < len(text):
        try:
            # Skip any whitespace or weird characters between JSON objects
            while pos < len(text) and text[pos] in " \t\r\n,":
                pos += 1
            if pos >= len(text):
                break
            obj, r = decoder.raw_decode(text[pos:])
            yield obj
            pos += r
        except json.JSONDecodeError as e:
            # Skip one character and try again to find the next valid JSON
            pos += 1

for log_file in log_files:
    print(f"\n=======================================================")
    print(f"PARSING LOG FILE: {log_file}")
    print(f"=======================================================")
    try:
        with open(log_file, "r") as f:
            content = f.read()
            
        count = 0
        for obj in parse_json_objects(content):
            # Check if this object represents a tail event with logs
            logs = obj.get("logs", [])
            for entry in logs:
                msg = entry.get("message", [])
                if len(msg) > 1 and msg[0] == "Inbound raw webhook payload:":
                    count += 1
                    print(f"\n[Inbound Payload #{count}]")
                    payload_data = msg[1]
                    if isinstance(payload_data, str):
                        try:
                            # Let's see if the string itself is a JSON
                            payload_json = json.loads(payload_data)
                            print(json.dumps(payload_json, indent=2))
                        except Exception:
                            print(payload_data)
                    else:
                        print(json.dumps(payload_data, indent=2))
        print(f"\nTotal payloads extracted: {count}")
    except Exception as e:
        print(f"Error parsing file: {e}")
