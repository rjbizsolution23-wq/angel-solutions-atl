import os
import subprocess

def rename_if_exists(src, dst):
    if os.path.exists(src):
        print(f"Renaming {src} -> {dst}")
        os.rename(src, dst)

def run_build():
    print("Running pnpm build...")
    res = subprocess.run(["pnpm", "build"], capture_output=True, text=True)
    print("Return code:", res.returncode)
    print("STDOUT:")
    print(res.stdout[-1000:] if len(res.stdout) > 1000 else res.stdout)
    print("STDERR:")
    print(res.stderr[-2000:] if len(res.stderr) > 2000 else res.stderr)
    return res.returncode == 0

# List of all page directories
all_dirs = [
    "about", "business-solutions", "contact", "disclaimers", 
    "financial-solutions", "funding-eligibility", "privacy", 
    "resources", "tax-solutions", "terms", "sitemap"
]

# Rename all to .disabled
for d in all_dirs:
    rename_if_exists(f"app/{d}", f"app/{d}.disabled")

success = run_build()

# Restore all
for d in all_dirs:
    rename_if_exists(f"app/{d}.disabled", f"app/{d}")

print("Done restoring. Success status:", success)
