import os

path = '/Users/kalivibecoding/Downloads/angel solutions site/angel-solutions-premium/.next/server/chunks/250.js'
if os.path.exists(path):
    lines = open(path).readlines()
    print(f"Total lines: {len(lines)}")
    if len(lines) >= 29:
        print("Line 29 content preview:")
        print(lines[28][:1000])
        print("Line 29 length:", len(lines[28]))
        # Find useContext or similar
        idx = lines[28].find("useContext")
        if idx != -1:
            print("Found useContext at index:", idx)
            print(lines[28][max(0, idx-200):min(len(lines[28]), idx+200)])
else:
    print("File not found")
