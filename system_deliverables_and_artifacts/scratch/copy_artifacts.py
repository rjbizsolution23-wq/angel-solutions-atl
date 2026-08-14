import os
import shutil

src_dir = "/Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503"
dest_dir = "/Users/kalivibecoding/Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/system_deliverables_and_artifacts"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

copied_count = 0
ignored_count = 0

for item in os.listdir(src_dir):
    src_item = os.path.join(src_dir, item)
    dest_item = os.path.join(dest_dir, item)
    
    # Exclude metadata, git, system files, and browser logs
    if item.endswith(".metadata.json") or item.startswith(".") or item == "browser":
        ignored_count += 1
        continue
        
    if os.path.isdir(src_item):
        if os.path.exists(dest_item):
            shutil.rmtree(dest_item)
        shutil.copytree(src_item, dest_item)
        copied_count += 1
    else:
        shutil.copy2(src_item, dest_item)
        copied_count += 1

print(f"COPY_COMPLETE: Copied {copied_count} items to {dest_dir}, ignored {ignored_count} system/metadata items.")
