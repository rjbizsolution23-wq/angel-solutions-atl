import subprocess

applescript = """
tell application "Google Chrome"
    set winList to every window
    set resultList to {}
    set winIndex to 1
    repeat with w in winList
        set tabIndex to 1
        set tabInfoList to {}
        try
            repeat with t in every tab of w
                copy (tabIndex & ": " & (title of t) & " (" & (URL of t) & ")") to end of tabInfoList
                set tabIndex to tabIndex + 1
            end repeat
        end try
        copy ("Window " & winIndex & ":\\n" & (tabInfoList as string)) to end of resultList
        set winIndex to winIndex + 1
    end repeat
    return resultList
end tell
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    print(proc.stdout.strip())
except Exception as e:
    print(f"Error: {e}")
