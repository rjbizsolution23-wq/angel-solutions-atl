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

# Disable the 4 major new pages
rename_if_exists("app/funding-eligibility", "app/funding-eligibility.disabled")
rename_if_exists("app/resources", "app/resources.disabled")
rename_if_exists("app/financial-solutions", "app/financial-solutions.disabled")
rename_if_exists("app/contact", "app/contact.disabled")

success = run_build()

# Restore them
rename_if_exists("app/funding-eligibility.disabled", "app/funding-eligibility")
rename_if_exists("app/resources.disabled", "app/resources")
rename_if_exists("app/financial-solutions.disabled", "app/financial-solutions")
rename_if_exists("app/contact.disabled", "app/contact")

print("Done restoring. Success status:", success)
