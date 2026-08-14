import subprocess

applescript = """
tell application "Google Chrome"
    set winList to every window
    repeat with w in winList
        set tabIndex to 1
        repeat with t in every tab of w
            if URL of t contains "developers.facebook.com" then
                try
                    set res to execute t javascript "document.title"
                    return "JS_OK:" & res
                on error e
                    return "JS_ERROR:" & e
                end try
            end if
            set tabIndex to tabIndex + 1
        end repeat
    end repeat
    return "TAB_NOT_FOUND"
end tell
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    print(proc.stdout.strip())
except Exception as e:
    print(f"Error: {e}")
