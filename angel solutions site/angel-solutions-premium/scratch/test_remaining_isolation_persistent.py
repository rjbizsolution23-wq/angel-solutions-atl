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

results = []

for name, imp in sections:
    test_content = f"{imp}\nexport default function Page() {{ return <{name} />; }}\n"
    open(file_path, "w").write(test_content)
    
    subprocess.run(["pkill", "-9", "-f", "next"])
    subprocess.run(["pkill", "-9", "-f", "node"])
    
    res = subprocess.run(["pnpm", "build"], capture_output=True, text=True)
    if res.returncode == 0:
        results.append(f"{name}: PASS")
    else:
        results.append(f"{name}: FAIL")

# Restore original
if original_content:
    open(file_path, "w").write(original_content)

open("scratch/results.txt", "w").write("\n".join(results))
print("RESULTS SAVED.")
