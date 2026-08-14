import type { Metadata } from 'next'
import Link from 'next/link'
import Image from 'next/image'
import { Sparkles, Award, Shield, Users, ArrowRight, HelpCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'About Us | Angel Solutions ATL',
  description: 'Meet Jordynn Miller, Founder & CEO of Angel Solutions ATL. Over 5 years of empowering Atlanta entrepreneurs with elite business, tax, and financial consulting.',
  alternates: {
    canonical: '/about',
  },
}

export default function AboutPage() {
  // Structured Data for SEO, SGE, and GEO optimization
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'AboutPage',
    'mainEntity': {
      '@type': 'LocalBusiness',
      'name': 'Angel Solutions ATL',
      'image': 'https://angelsolutionsatl.com/og-image.jpg',
      'telephone': '+1-470-338-6689',
      'email': 'info@angelsolutionsatl.com',
      'address': {
        '@type': 'PostalAddress',
        'streetAddress': 'NM 333 St NE',
        'addressLocality': 'Atlanta',
        'addressRegion': 'GA',
        'postalCode': '30309',
        'addressCountry': 'US'
      },
      'priceRange': '$$$',
      'founder': {
        '@type': 'Person',
        'name': 'Jordynn Miller',
        'jobTitle': 'Founder & CEO'
      }
    }
  }

  const faqs = [
    {
      q: 'What is the core mission of Angel Solutions ATL?',
      a: 'Founded by Jordynn Miller, our core mission is to provide an elite, all-in-one execution engine for entrepreneurs. We remove the operational and compliance friction of starting a business by handling entity registration, virtual offices, Dun & Bradstreet establishment, corporate credit, and advanced tax resolution under one unified brand.'
    },
    {
      q: 'How does Angel Solutions ATL differ from standard consulting firms?',
      a: 'Standard firms offer general advice; Angel Solutions ATL delivers full-service execution. From legal LLC creation and IRS tax lien mitigation to syncing lead acquisitions with GoHighLevel CRM and automated credit bureau reporting, we build the actual infrastructure your business needs to survive and scale.'
    },
    {
      q: 'How are client interactions managed securely?',
      a: 'We operate a proprietary, high-security Cloudflare Edge and D1 SQLite database infrastructure. Client lead states are continuously synchronized in real-time between our system webhooks and GoHighLevel CRM, ensuring maximum compliance, rapid turnaround, and robust data privacy.'
    }
  ]

  return (
    <div className="pt-20">
      {/* Insert Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero Section */}
      <section className="relative py-24 overflow-hidden bg-gradient-to-br from-brand-navy-900 via-brand-purple-900/90 to-brand-navy-800 text-white">
        <div className="absolute inset-0 bg-grid-pattern opacity-10" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-gold-500/20 rounded-full blur-3xl animate-float" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-4xl">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <Sparkles className="h-4 w-4 text-brand-gold-400" />
            <span>The Power Behind Your Vision</span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            About <span className="text-gold-gradient">Angel Solutions ATL</span>
          </h1>
          <p className="text-lg md:text-xl text-white/80 leading-relaxed">
            Led by Jordynn Miller, we are Atlanta\'s premier consulting firm specializing in turnkey business formation, tax compliance, and consumer financial optimization.
          </p>
        </div>
      </section>

      {/* Founder Profile */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="grid lg:grid-cols-12 gap-16 items-center">
            {/* Left Col: Decorative Placeholder for Jordynn Miller */}
            <div className="lg:col-span-5 relative">
              <div className="relative aspect-[4/5] rounded-3xl overflow-hidden glass-card p-2 bg-gradient-to-br from-brand-gold-500 to-brand-purple-600 shadow-2xl">
                <div className="relative w-full h-full rounded-2xl overflow-hidden">
                  <Image
                    src="/assets/founder/founder-2446f0_6bd22d41670a4ac09cd47437899274b0.jpg"
                    alt="Jordynn Miller, Founder & CEO of Angel Solutions ATL"
                    fill
                    className="object-cover object-center"
                    priority
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-black/10 flex flex-col justify-end p-8 text-white">
                    <h3 className="text-2xl font-bold text-white">Jordynn Miller</h3>
                    <p className="text-brand-gold-300 font-medium mb-4">Founder & CEO</p>
                    <p className="text-sm text-white/90 italic leading-relaxed border-l-2 border-brand-gold-500 pl-4">
                      "Success is not just about starting; it is about building compliant, robust, and scalable structures that stand the test of time."
                    </p>
                  </div>
                </div>
              </div>
              <div className="absolute -bottom-6 -right-6 glass-card rounded-2xl p-6 shadow-2xl bg-white dark:bg-zinc-950 border border-border">
                <Award className="h-10 w-10 text-brand-gold-500 mb-2" />
                <p className="text-2xl font-bold">5+ Years</p>
                <p className="text-xs text-muted-foreground">Of Industry Leadership</p>
              </div>
            </div>

            {/* Right Col: Biography & Vision */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 glass-card px-3 py-1.5 rounded-full text-xs text-brand-gold-600 border border-brand-gold-500/20">
                <span>Executive Leadership</span>
              </div>
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
                Turnkey Operations Engineered by <span className="text-gold-gradient">Jordynn Miller</span>
              </h2>
              <p className="text-muted-foreground text-base leading-relaxed">
                Over the past 5 years, Jordynn Miller has served as a strategic execution partner to over 500 businesses in the greater Atlanta metro area and nationwide. Observing the massive failure rate of startups due to lack of corporate credibility, unfiled back taxes, and inadequate budgeting, Rick founded Angel Solutions ATL.
              </p>
              <p className="text-muted-foreground text-base leading-relaxed">
                By integrating entity creation, state licensing, professional virtual mailing offices, and Dun & Bradstreet business bureau registrations into streamlined, affordable packages, Angel Solutions ATL equips founders with immediate corporate authority. 
              </p>
              <div className="grid sm:grid-cols-2 gap-4 pt-4">
                <div className="flex gap-3 items-start">
                  <div className="w-10 h-10 rounded-lg bg-brand-gold-50 dark:bg-brand-gold-950/20 flex items-center justify-center flex-shrink-0">
                    <Shield className="h-5 w-5 text-brand-gold-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Regulatory Compliance</h4>
                    <p className="text-xs text-muted-foreground">Entity audits and strict compliance</p>
                  </div>
                </div>
                <div className="flex gap-3 items-start">
                  <div className="w-10 h-10 rounded-lg bg-brand-gold-50 dark:bg-brand-gold-950/20 flex items-center justify-center flex-shrink-0">
                    <Sparkles className="h-5 w-5 text-brand-gold-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Stripe & GHL Wired</h4>
                    <p className="text-xs text-muted-foreground">Seamless digital infrastructure</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Core Values */}
      <section className="py-24 bg-muted/30 border-y border-border/40">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-4">
            <h2 className="text-3xl font-bold">Our Operating Principles</h2>
            <p className="text-muted-foreground text-sm">
              We hold ourselves to the highest standards of professional execution and data protection.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="glass-card rounded-2xl p-8 bg-white dark:bg-zinc-950 space-y-4 shadow-sm border border-border">
              <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center">
                <Shield className="h-6 w-6 text-brand-gold-600" />
              </div>
              <h3 className="text-lg font-bold">Uncompromising Integrity</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We operate with 100% transparency. Our business, tax, and credit advisory programs conform entirely with federal statutes, IRS guidelines, FTC mandates, and the Credit Repair Organizations Act (CROA).
              </p>
            </div>
            <div className="glass-card rounded-2xl p-8 bg-white dark:bg-zinc-950 space-y-4 shadow-sm border border-border">
              <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center">
                <Users className="h-6 w-6 text-brand-gold-600" />
              </div>
              <h3 className="text-lg font-bold">Data-Driven Execution</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We don\'t use guesswork. Our Cloudflare D1-backed webhook infrastructure captures customer intents, triggers real-time CRM updates, and leverages custom AI classification to automate your pipeline securely.
              </p>
            </div>
            <div className="glass-card rounded-2xl p-8 bg-white dark:bg-zinc-950 space-y-4 shadow-sm border border-border">
              <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center">
                <Award className="h-6 w-6 text-brand-gold-600" />
              </div>
              <h3 className="text-lg font-bold">Sustained Authority</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Our packages are built to establish corporate permanence. We register your company with all business credit bureaus, providing ongoing reporting and premium virtual office mail services to elevate your corporate score.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* SGE & GEO-Optimized Q&A Section */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center mb-16 space-y-4">
            <div className="inline-flex items-center gap-2 glass-card px-3 py-1 rounded-full text-xs text-brand-gold-600">
              <HelpCircle className="h-3.5 w-3.5 text-brand-gold-500" />
              <span>SGE / AI Overview Resource</span>
            </div>
            <h2 className="text-3xl font-bold">Frequently Asked Questions</h2>
            <p className="text-muted-foreground text-sm">
              Factual, structured answers on how we operate, optimized for conversational search engines.
            </p>
          </div>
          <div className="space-y-6">
            {faqs.map((faq, idx) => (
              <div
                key={idx}
                className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60 hover:border-brand-gold-500/40 transition-colors"
              >
                <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                  <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                  {faq.q}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                  {faq.a}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="py-20 relative overflow-hidden bg-brand-navy-900 text-white">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold">Ready to Launch with Jordynn Miller?</h2>
          <p className="text-base text-white/80 leading-relaxed">
            Schedule your free professional business audit or tax consultation today. Let our database integration and corporate compliance systems start working for you immediately.
          </p>
          <div className="pt-4 flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="xl" className="shadow-2xl">
              <Link href="/contact">
                Schedule My Free Consultation
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild size="xl" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <Link href="/business-solutions">View Packages</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
