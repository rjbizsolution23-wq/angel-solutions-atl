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
            for line in f:
                if '"Inbound raw webhook payload:"' in line:
                    # Let's print the line itself to see how it's formatted
                    print(line.strip()[:1000])
                    # Let's also see if we can extract the JSON of the log event
                    try:
                        # Find the start of the logs list
                        # A typical line in wrangler tail is a full JSON of the event.
                        # Let's see if the entire line can be parsed as JSON.
                        event_json = json.loads(line.strip())
                        # If the entire line is a JSON, let's extract logs
                        logs = event_json.get("logs", [])
                        for l in logs:
                            msg = l.get("message", [])
                            if len(msg) > 1 and msg[0] == "Inbound raw webhook payload:":
                                print("Extracted Payload:")
                                if isinstance(msg[1], str):
                                    try:
                                        print(json.dumps(json.loads(msg[1]), indent=2))
                                    except Exception:
                                        print(msg[1])
                                else:
                                    print(json.dumps(msg[1], indent=2))
                    except Exception as e:
                        print(f"Could not parse line as JSON: {e}")
    except Exception as e:
        print(f"Error parsing {log_file}: {e}")
