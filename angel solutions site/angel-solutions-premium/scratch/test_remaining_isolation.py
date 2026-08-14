import os
import subprocess

sections = [
    ("StatsSection", "import { StatsSection } from '@/components/sections/stats-section'"),
    ("AboutPreview", "import { AboutPreview } from '@/components/sections/about-preview'"),
    ("ServicesOverview", "import { ServicesOverview } from '@/components/sections/services-overview'"),
    ("FeaturesSection", "import { FeaturesSection } from '@/components/sections/features-section'"),
    ("TestimonialsSection", "import { TestimonialsSection } from '@/components/sections/testimonials-section'"),
    ("CTASection", "import { CTASection } from '@/components/sections/cta-section'"),
]

file_path = "app/page.tsx"
if os.path.exists(file_path):
    original_content = open(file_path).read()
else:
    original_content = ""

print("Starting remaining sections isolation tests...")

for name, imp in sections:
    print(f"\n--- Testing {name} ---")
    test_content = f"{imp}\nexport default function Page() {{ return <{name} />; }}\n"
    open(file_path, "w").write(test_content)
    
    subprocess.run(["pkill", "-9", "-f", "next"])
    subprocess.run(["pkill", "-9", "-f", "node"])
    
    res = subprocess.run(["pnpm", "build"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"PASS: {name} compiled successfully!")
    else:
        print(f"FAIL: {name} failed compilation!")
        print("STDERR SNIPPET:")
        print(res.stderr[-2000:] if len(res.stderr) > 2000 else res.stderr)

# Restore original
if original_content:
    open(file_path, "w").write(original_content)
print("\nRestored original app/page.tsx.")
