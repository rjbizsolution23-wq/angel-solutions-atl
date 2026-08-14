import os
import subprocess

file_path = "components/visuals/hero-interactive-dashboard.tsx"
original_content = open(file_path).read()

# Make a backup
open(file_path + ".original", "w").write(original_content)

# Simplify by removing AnimatePresence and motion from the tab container
content = original_content

# 1. Replace AnimatePresence open and close
content = content.replace('<AnimatePresence mode="wait">', '')
content = content.replace('</AnimatePresence>', '')

# 2. Replace motion.div for tabs with standard divs
content = content.replace('''          {activeTab === 'tracker' && (
            <motion.div
              key="tracker"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-4"
            >''', '''          {activeTab === 'tracker' && (
            <div className="space-y-4">''')

content = content.replace('''            </motion.div>
          )}''', '''            </div>
          )}''')

content = content.replace('''          {activeTab === 'credit' && (
            <motion.div
              key="credit"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6 text-center py-4"
            >''', '''          {activeTab === 'credit' && (
            <div className="space-y-6 text-center py-4">''')

content = content.replace('''          {activeTab === 'api' && (
            <motion.div
              key="api"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-4"
            >''', '''          {activeTab === 'api' && (
            <div className="space-y-4">''')

# Also replace <motion.circle ... /> with <circle ... />
content = content.replace('''                    <motion.circle
                      cx="80"
                      cy="80"
                      r="65"
                      className="stroke-brand-gold-500"
                      strokeWidth="10"
                      fill="transparent"
                      strokeDasharray="408.4"
                      strokeDashoffset={408.4 - (408.4 * creditScore) / 100}
                      transition={{ duration: 0.3 }}
                      strokeLinecap="round"
                    />''', '''                    <circle
                      cx="80"
                      cy="80"
                      r="65"
                      className="stroke-brand-gold-500"
                      strokeWidth="10"
                      fill="transparent"
                      strokeDasharray="408.4"
                      strokeDashoffset={408.4 - (408.4 * creditScore) / 100}
                      strokeLinecap="round"
                    />''')

open(file_path, "w").write(content)

print("Dashboard simplified. Running build...")
subprocess.run(["pkill", "-9", "-f", "next"])
subprocess.run(["pkill", "-9", "-f", "node"])
res = subprocess.run(["pnpm", "build"], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode != 0:
    print("STDERR:")
    print(res.stderr[-2000:] if len(res.stderr) > 2000 else res.stderr)
else:
    print("SUCCESS!!!")

# Restore original if failed, or keep if succeeded
if res.returncode != 0:
    print("Restoring original...")
    open(file_path, "w").write(original_content)
    if os.path.exists(file_path + ".original"):
        os.remove(file_path + ".original")
