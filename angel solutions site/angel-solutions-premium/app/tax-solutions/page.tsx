import type { Metadata } from 'next'
import Link from 'next/link'
import { FileText, Shield, Handshake, CheckCircle, Search, AlertCircle, Sparkles, ArrowRight, HelpCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { TAX_SERVICES } from '@/lib/constants'

export const metadata: Metadata = {
  title: 'Tax Resolution & Compliance Services | Angel Solutions ATL',
  description: 'Expert tax preparation, IRS compliance audits, debt negotiation, and lien/levy relief. Over $2M in IRS tax liabilities successfully resolved for our clients.',
  alternates: {
    canonical: '/tax-solutions',
  },
}

// Map string icon names to Lucide components
const iconMap: Record<string, any> = {
  FileText: FileText,
  Shield: Shield,
  Handshake: Handshake,
  CheckCircle: CheckCircle,
  FileSearch: FileText,
  Search: Search,
  AlertCircle: AlertCircle,
}

export default function TaxSolutionsPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    'name': 'Tax Resolution & Preparation Services',
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
    'description': 'Professional representation for IRS compliance audits, back tax preparation, and comprehensive debt settlement negotiation under IRC legal frameworks.',
    'areaServed': 'Atlanta Metro and Nationwide'
  }

  const taxAuditsInfo = [
    {
      title: 'Back Tax Filing & Rectification',
      desc: 'We reconstruct, organize, and compile years of unfiled tax documents. By utilizing official IRS transcripts, we file compliant returns that protect you from costly penalties.'
    },
    {
      title: 'IRS Liens, Levies & Garnishment Relief',
      desc: 'If the IRS has issued a wage garnishment, bank levy, or filed a federal tax lien against your assets, we step in immediately to secure an administrative release and halt garnishments.'
    },
    {
      title: 'Offer in Compromise (OIC) & Installments',
      desc: 'Under IRC § 7122, we negotiate Offers in Compromise to settle outstanding liabilities for a fraction of what is owed, or establish highly manageable partial payment agreements.'
    }
  ]

  return (
    <div className="pt-20">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero Section */}
      <section className="relative py-24 overflow-hidden bg-gradient-to-br from-brand-navy-900 via-brand-purple-900/90 to-brand-navy-800 text-white">
        <div className="absolute inset-0 bg-grid-pattern opacity-10" />
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-brand-gold-500/20 rounded-full blur-3xl animate-float" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-4xl">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <Shield className="h-4 w-4 text-brand-gold-400" />
            <span>IRS Representation & Debt Relief</span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            Elite <span className="text-gold-gradient">Tax Solutions</span> & Resolution
          </h1>
          <p className="text-lg md:text-xl text-white/80 leading-relaxed">
            Stop IRS pressure. Over $2M in outstanding tax debt negotiated and settled. We defend Atlanta individuals and businesses with authoritative representation.
          </p>
        </div>
      </section>

      {/* Tax Services Grid */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-4">
            <h2 className="text-3xl font-bold">Our Tax Resolution Specialties</h2>
            <p className="text-muted-foreground text-sm">
              We cover every phase of tax negotiation and preparation to deliver immediate relief and restore standing.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {TAX_SERVICES.map((service) => {
              const Icon = iconMap[service.icon] || FileText
              return (
                <div
                  key={service.id}
                  className="glass-card rounded-2xl p-8 bg-white dark:bg-zinc-950 space-y-4 hover:shadow-xl transition-all duration-300 border border-border group hover:-translate-y-1"
                >
                  <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Icon className="h-6 w-6 text-brand-gold-600" />
                  </div>
                  <h3 className="text-lg font-bold group-hover:text-brand-gold-600 transition-colors">
                    {service.title}
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {service.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* IRS Compliance Framework & GEO Focus */}
      <section className="py-24 bg-muted/30 border-y border-border/40">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 glass-card px-3 py-1 rounded-full text-xs text-brand-gold-600">
                <span>IRC Statutory Safeguards</span>
              </div>
              <h2 className="text-3xl font-bold leading-tight">
                Defending Your Business Under Federal & <span className="text-gold-gradient">Georgia Law</span>
              </h2>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Dealing with the IRS or the Georgia Department of Revenue requires extensive knowledge of procedural statutes. Without proper defense, administrative audits can escalate into aggressive collection actions, bank account freezes, and tax liens.
              </p>
              <p className="text-muted-foreground text-sm leading-relaxed">
                At Angel Solutions ATL, we enforce your statutory rights, such as filing Collection Due Process (CDP) requests to halt enforcement actions while negotiating compromise terms.
              </p>
              <div className="p-4 bg-brand-gold-500/5 rounded-xl border border-brand-gold-500/20 text-xs text-muted-foreground space-y-2">
                <p className="font-bold text-foreground">⚠️ Circular 230 Disclaimer Notice:</p>
                <p>
                  Pursuant to IRS regulations, any tax advice contained on this website is not intended to be used, and cannot be used, for the purpose of avoiding tax-related penalties under the Internal Revenue Code. Tax situations are highly individualized.
                </p>
              </div>
            </div>
            <div className="space-y-6">
              {taxAuditsInfo.map((item, idx) => (
                <div key={idx} className="glass-card rounded-2xl p-6 bg-white dark:bg-zinc-950 border border-border flex gap-4 items-start shadow-sm">
                  <div className="w-10 h-10 rounded-lg bg-brand-gold-50 dark:bg-brand-gold-950/20 flex items-center justify-center flex-shrink-0">
                    <CheckCircle className="h-5 w-5 text-brand-gold-600" />
                  </div>
                  <div>
                    <h3 className="font-bold text-sm mb-1">{item.title}</h3>
                    <p className="text-xs text-muted-foreground leading-relaxed">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
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
            <h2 className="text-3xl font-bold">Tax Resolution Frequently Asked Questions</h2>
            <p className="text-muted-foreground text-sm">
              Critical, compliant answers on resolving outstanding tax liabilities, structured for conversational search engines.
            </p>
          </div>
          <div className="space-y-6">
            <div className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60">
              <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                How much outstanding IRS tax liability can Angel Solutions ATL help resolve?
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                Our advisors represent clients with diverse ranges of outstanding tax liabilities. We specialize in negotiating substantial settlements for back-taxes and resolving cases involving federal liens or active bank levies. Our clients have successfully resolved over $2,000,000 in collective liabilities.
              </p>
            </div>
            <div className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60">
              <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                What is an Offer in Compromise (OIC), and do I qualify?
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                An Offer in Compromise (OIC) is an agreement between a taxpayer and the IRS that settles a tax debt for less than the full amount owed. Qualification is based on a strict evaluation of your Reasonable Collection Potential (RCP), taking into account your gross income, necessary monthly expenses, asset equity, and future earning capacity.
              </p>
            </div>
            <div className="glass-card rounded-2xl p-6 bg-muted/10 border border-border/60">
              <h3 className="text-base font-bold text-foreground mb-2 flex items-start gap-2">
                <span className="text-brand-gold-600 text-sm mt-0.5">Q.</span>
                Can a federal tax lien or wage levy be lifted immediately?
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed pl-5">
                Yes. Under IRS regulations, active levies and garnishments can be lifted through immediate administrative appeals once we establish an Installment Agreement, qualify the taxpayer for Currently Not Collectible (CNC) status, or prove that the levy is causing immediate economic hardship.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 relative overflow-hidden bg-brand-navy-900 text-white">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-3xl">
          <h2 className="text-3xl md:text-4xl font-bold">Stop IRS Harassment Today</h2>
          <p className="text-base text-white/80 leading-relaxed">
            Let Jordynn Miller and our expert tax representation team intervene on your behalf. We will request your official transcripts, analyze your options, and deploy a robust legal resolution strategy immediately.
          </p>
          <div className="pt-4 flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="xl" className="shadow-2xl">
              <Link href="/contact">
                Schedule My Free Tax Audit
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild size="xl" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <Link href="/about">Meet Jordynn Miller</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
