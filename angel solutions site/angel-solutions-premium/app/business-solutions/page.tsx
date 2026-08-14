import type { Metadata } from 'next'
import { BusinessHero } from '@/components/sections/business/business-hero'
import { PackagesSection } from '@/components/sections/business/packages-section'
import { ProcessSection } from '@/components/sections/business/process-section'
import { BusinessFeaturesSection } from '@/components/sections/business/business-features'
import { CTASection } from '@/components/sections/cta-section'

export const metadata: Metadata = {
  title: 'Business Solutions | Angel Solutions ATL',
  description: 'Professional business formation packages starting at $450. LLC registration, business branding, virtual office, and funding programs.',
}

export default function BusinessSolutionsPage() {
  return (
    <>
      <BusinessHero />
      <PackagesSection />
      <BusinessFeaturesSection />
      <ProcessSection />
      <CTASection />
    </>
  )
}
