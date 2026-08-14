log_paths = [
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log",
    "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9181.log"
]

print("--- SCANNING FOR ALL LOGGED ERRORS AND FAILURES ---")
for log_path in log_paths:
    print(f"\nScanning: {log_path}...")
    try:
        content = open(log_path, "r", errors="ignore").read()
        import re
        # Find lines with error, fail, or warn in a case-insensitive manner
        lines = content.split("\n")
        err_lines = []
        for idx, line in enumerate(lines, 1):
            if any(k in line.lower() for k in ["error", "fail", "warn", "exception"]):
                err_lines.append((idx, line))
        
        print(f"Found {len(err_lines)} error/warning lines.")
        for idx, line in err_lines[-30:]: # Print last 30 errors/warnings
            print(f"Line {idx}: {line.strip()[:200]}")
    except Exception as e:
        print(f"Error reading {log_path}: {e}")
