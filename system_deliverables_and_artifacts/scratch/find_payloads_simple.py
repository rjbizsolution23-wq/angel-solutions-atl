log_path = "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/.system_generated/tasks/task-9314.log"

lines = open(log_path, "r", errors="ignore").readlines()
for i, line in enumerate(lines):
    if "Inbound raw webhook payload:" in line:
        print(f"\nMatch at line {i+1}:")
        for offset in range(0, 10):
            if i + offset < len(lines):
                print(lines[i + offset].rstrip())
