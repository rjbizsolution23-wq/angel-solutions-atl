import os

path = "/Users/kalivibecoding/Downloads/angel solutions site/angel-solutions-premium/.next/server/chunks/756.js"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) >= 29:
        line_29 = lines[28] # 1-indexed to 0-indexed
        print(f"Line 29 length: {len(line_29)}")
        # Print a snippet of line 29 around index 31233
        start_idx = max(0, 31233 - 300)
        end_idx = min(len(line_29), 31233 + 300)
        print("--- SNIPPET AROUND 31233 ---")
        print(line_29[start_idx:end_idx])
        print("----------------------------")
    else:
        print(f"File only has {len(lines)} lines")
else:
    print("File not found")
