import type { Metadata } from 'next'
import { ContactHero } from '@/components/sections/contact/contact-hero'
import { ContactContainer } from '@/components/sections/contact/contact-container'
import { ContactInfo } from '@/components/sections/contact/contact-info'

export const metadata: Metadata = {
  title: 'Contact Us | Angel Solutions ATL',
  description: 'Schedule your free consultation with Angel Solutions ATL. Get expert guidance on business formation, tax resolution, and financial solutions.',
}

export default function ContactPage() {
  return (
    <>
      <ContactHero />
      <div className="container mx-auto px-4 py-24">
        <div className="grid lg:grid-cols-3 gap-12 max-w-7xl mx-auto">
          <div className="lg:col-span-2">
            <ContactContainer />
          </div>
          <div>
            <ContactInfo />
          </div>
        </div>
      </div>
    </>
  )
}
