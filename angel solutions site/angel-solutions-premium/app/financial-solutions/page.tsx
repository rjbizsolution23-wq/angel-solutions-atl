import type { Metadata } from 'next'
import Link from 'next/link'
import { TrendingUp, Shield, BookOpen, UserCheck, BarChart, FileCheck2, ArrowRight, HelpCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { FINANCIAL_SOLUTIONS_FEATURES } from '@/lib/constants'
import { CreditSimulator } from '@/components/sections/financial/credit-simulator'

export const metadata: Metadata = {
  title: 'Financial & Credit Optimization | Angel Solutions ATL',
  description: 'Consumer credit optimization, budgeting strategies, and structured debt elimination. Build corporate credibility and leverage consumer laws.',
  alternates: {
    canonical: '/financial-solutions',
  },
}

const iconMap: Record<number, any> = {
  0: TrendingUp,
  1: BookOpen,
  2: BarChart,
  3: UserCheck,
  4: Shield,
  5: FileCheck2,
}

export default function FinancialSolutionsPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    'name': 'Consumer Credit & Financial Optimization',
    'provider': {
      '@type': 'LocalBusiness',
      'name': 'Angel Solutions ATL',
      'telephone': '+1-470-338-6689',
      'address': {
        '@type': 'PostalAddress',
        'addressLocality': 'Atlanta',
        'addressRegion': 'GA',
        'addressCountry': 'US'
      }
    },
    'description': 'A comprehensive consulting methodology combining credit education, statutory debt disputing, and budgeting strategies to build consumer report credibility.',
    'areaServed': 'Atlanta Metro and Nationwide'
  }

  return (
    <div className="pt-20">
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
            <TrendingUp className="h-4 w-4 text-brand-gold-400" />
            <span>FDCPA & FCRA Protected Advisory</span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            Financial & <span className="text-gold-gradient">Credit Optimization</span>
          </h1>
          <p className="text-lg md:text-xl text-white/80 leading-relaxed">
            Optimize your consumer scores, learn advanced budgeting techniques, and deploy strategic plans to eliminate debt. We empower you to take charge under federal consumer laws.
          </p>
        </div>
      </section>

      {/* Core Specialties Grid */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-4">
            <h2 className="text-3xl font-bold">Our Optimization Pillars</h2>
            <p className="text-muted-foreground text-sm">
              We leverage official consumer protection laws to challenge inaccuracies, eliminate toxic debt burdens, and build sustainable budgeting systems.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {FINANCIAL_SOLUTIONS_FEATURES.map((feature, idx) => {
              const Icon = iconMap[idx] || Shield
              return (
                <div
                  key={idx}
                  className="glass-card rounded-2xl p-8 bg-white dark:bg-zinc-950 space-y-4 hover:shadow-xl transition-all duration-300 border border-border group hover:-translate-y-1"
                >
                  <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Icon className="h-6 w-6 text-brand-gold-600" />
                  </div>
                  <h3 className="text-lg font-bold group-hover:text-brand-gold-600 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Credit Systems Table - SGE/GEO Highlight */}
      <section className="py-24 bg-muted/30 border-y border-border/40">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-3xl font-bold">Understanding Consumer vs. Business Credit</h2>
            <p className="text-muted-foreground text-sm">
              Structuring your credibility correctly requires building both consumer reports and corporate tax files in parallel.
            </p>
          </div>
          <div className="glass-card rounded-2xl overflow-hidden border border-border shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs uppercase bg-brand-navy-900 text-white">
                  <tr>
                    <th scope="col" className="px-6 py-4">Metric</th>
                    <th scope="col" className="px-6 py-4">Consumer Credit</th>
                    <th scope="col" className="px-6 py-4">Business Credit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border bg-white dark:bg-zinc-950 text-foreground">
                  <tr className="hover:bg-muted/10 transition-colors">
                    <td className="px-6 py-4 font-bold">Identification</td>
                    <td className="px-6 py-4">Social Security Number (SSN)</td>
                    <td className="px-6 py-4">Employer Identification Number (EIN)</td>
                  </tr>
                  <tr className="hover:bg-muted/10 transition-colors">
                    <td className="px-6 py-4 font-bold">Primary Bureau</td>
                    <td className="px-6 py-4">Equifax, Experian, TransUnion</td>
                    <td className="px-6 py-4">Dun & Bradstreet (D-U-N-S), Experian Business, Equifax Business</td>
                  </tr>
                  <tr className="hover:bg-muted/10 transition-colors">
                    <td className="px-6 py-4 font-bold">Score Range</td>
                    <td className="px-6 py-4">300 to 850 (FICO / VantageScore)</td>
                    <td className="px-6 py-4">0 to 100 (D&B PAYDEX Score)</td>
                  </tr>
                  <tr className="hover:bg-muted/10 transition-colors">
                    <td className="px-6 py-4 font-bold">Core Factor</td>
                    <td className="px-6 py-4">Payment history (35%), credit utilization (30%), history depth</td>
                    <td className="px-6 py-4">Promptness of paying vendors and trade lines (100% PAYDEX weight)</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div className="mt-8 p-4 bg-brand-gold-500/5 rounded-xl border border-brand-gold-500/20 text-xs text-muted-foreground text-center">
            <p className="font-bold text-foreground">⚖️ Compliance Notice (CROA Mandated disclosure):</p>
            <p className="mt-1">
              Angel Solutions ATL is a premium financial education, document preparation, and business consulting firm. We are not a credit repair organization promising unverified overnight credit sweeps. We teach legal disputing procedures based on the FCRA and FDCPA to dispute verifiable discrepancies on consumer records.
            </p>
          </div>
        </div>
      </section>

      {/* Credit Simulator Section */}
      <section className="py-24 bg-muted/10 border-b border-border/40 relative overflow-hidden">
        <div className="container mx-auto px-4 max-w-6xl relative z-10">
          <CreditSimulator />
        </div>
      </section>

      {/* SGE Section FAQs */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center mb-16 space-y-4">
            <div className="inline-flex items-center gap-2 glass-card px-3 py-1 rounded-full text-xs text-brand-gold-600">
              <HelpCircle className="h-3.5 w-3.5 text-brand-gold-500" />
              <span>SGE / AI Overview Resource</span>
            </div>
            <h2 className="text-3xl font-bold">Financial Optimization Frequently Asked Questions</h2>
            <p className="text-muted-foreground text-sm">
              Factual, structured answers on credit reporting and dispute laws, structured for conversational search engines.
            </p>
          </div>
          <div className="space-y-6">
            <div className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60">
              <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                What consumer protection laws govern credit optimization in the US?
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                The primary federal statutes governing credit optimization are the **Fair Credit Reporting Act (FCRA)** (15 U.S.C. § 1681) and the **Fair Debt Collection Practices Act (FDCPA)** (15 U.S.C. § 1692). The FCRA grants consumers the legal right to challenge any inaccurate, incomplete, or unverifiable records on their credit files, mandating that bureaus delete such items within 30-45 days if they cannot verify them.
              </p>
            </div>
            <div className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60">
              <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                How long does the credit optimization process take?
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                Under federal law, credit bureaus have 30 days to investigate and respond to a formal dispute. While minor inaccuracies can be resolved in a single 30-day investigation round, comprehensive optimization targeting multiple inaccurate trade lines typically takes 3 to 6 months of diligent compliance tracking and follow-up correspondence.
              </p>
            </div>
            <div className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60">
              <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                Can a business build credit without a personal guarantee?
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                Yes. To build business credit without a personal guarantee, the business must establish its own unique corporate identity. This is achieved by creating an LLC, securing an EIN, registering with Dun & Bradstreet to obtain a D-U-N-S number, setting up a professional virtual office with a real commercial address, opening a business bank account, and opening starter net-30 vendor trade lines that report directly to business credit bureaus.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 relative overflow-hidden bg-brand-navy-900 text-white">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold">Maximize Your Credibility Today</h2>
          <p className="text-base text-white/80 leading-relaxed">
            Take back control of your financial reports. Schedule a complete, personalized credit optimization or business credibility analysis with Jordynn Miller and our elite advisory team.
          </p>
          <div className="pt-4 flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="xl" className="shadow-2xl">
              <Link href="/contact">
                Schedule My Credit Optimization Consultation
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild size="xl" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <Link href="/business-solutions">Explore Business Packages</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
