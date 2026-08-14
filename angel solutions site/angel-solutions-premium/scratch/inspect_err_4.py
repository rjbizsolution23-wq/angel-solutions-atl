import os

path = '/Users/kalivibecoding/Downloads/angel solutions site/angel-solutions-premium/.next/server/chunks/250.js'
if os.path.exists(path):
    lines = open(path).readlines()
    if len(lines) >= 29:
        line = lines[28]
        offset = 31233
        print(f"Characters around offset {offset} on line 29:")
        print(line[max(0, offset-200):min(len(line), offset+200)])
else:
    print("File not found")
