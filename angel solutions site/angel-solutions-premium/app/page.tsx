'use client'

import { HeroSection } from '@/components/sections/hero-section'
import { StatsSection } from '@/components/sections/stats-section'
import { ServicesOverview } from '@/components/sections/services-overview'
import { AboutPreview } from '@/components/sections/about-preview'
import { FeaturesSection } from '@/components/sections/features-section'
import { TestimonialsSection } from '@/components/sections/testimonials-section'
import { CTASection } from '@/components/sections/cta-section'

export default function Home() {
  return (
    <>
      <HeroSection />
      <StatsSection />
      <ServicesOverview />
      <AboutPreview />
      <FeaturesSection />
      <TestimonialsSection />
      <CTASection />
    </>
  )
}
