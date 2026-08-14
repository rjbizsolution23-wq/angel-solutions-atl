import subprocess

applescript = """
tell application "System Events"
    set appList to every process whose background only is false
    set resultList to {}
    repeat with a in appList
        set appName to name of a
        set winTitles to {}
        try
            tell process appName
                set winList to every window
                repeat with w in winList
                    copy title of w to end of winTitles
                end repeat
            end tell
        end try
        if count of winTitles is greater than 0 then
            copy (appName & ": " & (winTitles as string)) to end of resultList
        end if
    end repeat
    return resultList
end tell
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    print(proc.stdout.strip())
except Exception as e:
    print(f"Error: {e}")
