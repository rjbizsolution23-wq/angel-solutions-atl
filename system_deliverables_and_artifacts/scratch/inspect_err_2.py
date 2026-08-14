import os

path = "/Users/kalivibecoding/Downloads/angel solutions site/angel-solutions-premium/.next/server/chunks/ssr/_1qr-fas._.js"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) >= 4:
        line_4 = lines[3] # 1-indexed to 0-indexed
        print(f"Line 4 length: {len(line_4)}")
        # Print a snippet of line 4 around index 20585
        start_idx = max(0, 20585 - 300)
        end_idx = min(len(line_4), 20585 + 300)
        print("--- SNIPPET AROUND 20585 ---")
        print(line_4[start_idx:end_idx])
        print("----------------------------")
    else:
        print(f"File only has {len(lines)} lines")
else:
    print("File not found")
