import os
import subprocess

sections = [
    ("HeroSection", "import { HeroSection } from '@/components/sections/hero-section'\nexport default function Page() { return <HeroSection />; }"),
    ("StatsSection", "import { StatsSection } from '@/components/sections/stats-section'\nexport default function Page() { return <StatsSection />; }"),
    ("AboutPreview", "import { AboutPreview } from '@/components/sections/about-preview'\nexport default function Page() { return <AboutPreview />; }"),
    ("ServicesOverview", "import { ServicesOverview } from '@/components/sections/services-overview'\nexport default function Page() { return <ServicesOverview />; }"),
    ("FeaturesSection", "import { FeaturesSection } from '@/components/sections/features-section'\nexport default function Page() { return <FeaturesSection />; }"),
    ("TestimonialsSection", "import { TestimonialsSection } from '@/components/sections/testimonials-section'\nexport default function Page() { return <TestimonialsSection />; }"),
    ("CTASection", "import { CTASection } from '@/components/sections/cta-section'\nexport default function Page() { return <CTASection />; }")
]

# Ensure we have clean directories first (not disabled)
# (They should have been restored by test_all_isolation.py but let's double check)
for d in ["about", "business-solutions", "contact", "disclaimers", "financial-solutions", "funding-eligibility", "privacy", "resources", "tax-solutions", "terms", "sitemap"]:
    src = f"app/{d}.disabled"
    dst = f"app/{d}"
    if os.path.exists(src):
        os.rename(src, dst)

# Back up real page
if not os.path.exists("app/page.tsx.real_backup"):
    os.rename("app/page.tsx", "app/page.tsx.real_backup")

results = {}

for name, template in sections:
    print(f"\n=====================================")
    print(f"Testing section: {name}")
    print(f"=====================================")
    
    # Kill next
    subprocess.run(["pkill", "-9", "-f", "next"])
    
    open("app/page.tsx", "w").write(template)
    
    res = subprocess.run(["pnpm", "build"], capture_output=True, text=True)
    print(f"Return code for {name}:", res.returncode)
    results[name] = res.returncode
    
    if res.returncode != 0:
        print(f"FAILED: {name}")
        print("STDERR:")
        print(res.stderr[-1000:] if len(res.stderr) > 1000 else res.stderr)

# Restore real page
if os.path.exists("app/page.tsx.real_backup"):
    if os.path.exists("app/page.tsx"):
        os.remove("app/page.tsx")
    os.rename("app/page.tsx.real_backup", "app/page.tsx")

print("\nFinal results:")
for k, v in results.items():
    print(f"  {k}: {'PASS' if v == 0 else 'FAIL'}")
