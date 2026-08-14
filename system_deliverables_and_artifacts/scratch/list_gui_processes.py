import subprocess

applescript = """
tell application "System Events"
    set nameList to name of every process whose background only is false
    return nameList
end tell
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    print(proc.stdout.strip())
except Exception as e:
    print(f"Error: {e}")
