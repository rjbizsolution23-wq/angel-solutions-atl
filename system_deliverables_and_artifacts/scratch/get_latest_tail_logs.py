log_path = "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log"

try:
    with open(log_path, "r", errors="ignore") as f:
        lines = f.readlines()
        print(f"--- LATEST 100 LINES OF WRANGLER TAIL ({len(lines)} lines total) ---")
        for line in lines[-100:]:
            print(line.rstrip())
except Exception as e:
    print(f"Error: {e}")
