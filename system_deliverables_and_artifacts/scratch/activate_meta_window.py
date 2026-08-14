import subprocess

applescript = """
tell application "System Events"
    tell process "Google Chrome"
        set frontmost to true
        try
            set winList to every window
            repeat with w in winList
                if title of w contains "Meta for Developers" then
                    perform action "AXRaise" of w
                    return "Activated window: " & (title of w)
                end if
            end repeat
        end try
    end tell
end tell
return "Not found"
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    print(proc.stdout.strip())
except Exception as e:
    print(f"Error: {e}")
