import re

logs = [
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9181.log",
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log"
]

print("--- PARSING WRANGLER TAIL LOGS FOR WEBHOOK PAYLOADS ---")

for log_path in logs:
    print(f"\nScanning: {log_path}...")
    try:
        content = open(log_path, "r", errors="ignore").read()
        
        # Look for any JSON-like payload or message structures
        # Let's find patterns like "entry" or "sender" or "instagram"
        lines = content.split("\n")
        matched_lines = []
        for i, line in enumerate(lines):
            if "sender" in line or "skool" in line.lower() or "recipient" in line or "object" in line:
                # print snippet of surrounding lines
                start = max(0, i-5)
                end = min(len(lines), i+6)
                matched_lines.append((i, "\n".join(lines[start:end])))
        
        print(f"Found {len(matched_lines)} matches.")
        for idx, snip in matched_lines[:15]: # Show first 15 matches
            print(f"\n[Line {idx}]")
            print(snip)
            print("-" * 40)
            
    except Exception as e:
        print(f"Error reading {log_path}: {e}")
