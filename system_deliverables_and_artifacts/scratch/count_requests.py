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
            post_count = 0
            get_count = 0
            other_count = 0
            for line in f:
                if '"method": "POST"' in line:
                    post_count += 1
                elif '"method": "GET"' in line:
                    get_count += 1
                elif '"method":' in line:
                    other_count += 1
            print(f"POST Requests: {post_count}")
            print(f"GET Requests: {get_count}")
            print(f"Other Requests: {other_count}")
    except Exception as e:
        print(f"Error parsing: {e}")
