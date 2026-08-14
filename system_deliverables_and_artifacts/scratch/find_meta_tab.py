import subprocess
import sys

applescript = """
tell application "Google Chrome"
    set winList to every window
    set found to false
    repeat with w in winList
        set tabIndex to 1
        repeat with t in every tab of w
            if URL of t contains "developers.facebook.com" then
                set active tab index of w to tabIndex
                set index of w to 1
                activate
                set found to true
                return "FOUND:" & (URL of t) & "|" & (title of t)
            end if
            set tabIndex to tabIndex + 1
        end repeat
    end repeat
    if not found then
        return "NOT_FOUND"
    end if
end tell
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    res = proc.stdout.strip()
    print(res)
except Exception as e:
    print(f"Error: {e}")
