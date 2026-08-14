import subprocess

applescript = """
tell application "System Events"
    set chromeProcesses to every process whose name is "Google Chrome"
    set resultList to {}
    set procIndex to 1
    repeat with p in chromeProcesses
        set pid to unix id of p
        copy ("Process " & procIndex & " (PID: " & pid & ")") to end of resultList
        try
            -- Let's try to list windows/tabs using UI Scripting for this process
            tell p
                set winList to every window
                repeat with w in winList
                    set winTitle to title of w
                    copy ("  Window: " & winTitle) to end of resultList
                end repeat
            end tell
        end try
        set procIndex to procIndex + 1
    end repeat
    return resultList
end tell
"""

try:
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=True)
    print(proc.stdout.strip())
except Exception as e:
    print(f"Error: {e}")
