import type { Metadata } from 'next'
import Link from 'next/link'
import { Landmark, Briefcase, FileText, Compass, ArrowRight, ShieldCheck, Mail } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'Sitemap | Angel Solutions ATL',
  description: 'Navigate the complete structured index of Angel Solutions ATL. Discover business formation packages, tax resolution systems, and financial optimization models.',
  alternates: {
    canonical: '/sitemap',
  },
}

export default function SitemapPage() {
  const categories = [
    {
      title: 'Main Directory',
      icon: Compass,
      links: [
        { href: '/', label: 'Home Page' },
        { href: '/about', label: 'About Us & Founder Jordynn Miller' },
        { href: '/contact', label: 'Contact & Secure Client Portal' },
      ],
    },
    {
      title: 'Solutions & Programs',
      icon: Briefcase,
      links: [
        { href: '/business-solutions', label: 'Turnkey Business Solutions' },
        { href: '/tax-solutions', label: 'Elite Tax Resolution & Audits' },
        { href: '/financial-solutions', label: 'Financial & Credit Optimization' },
      ],
    },
    {
      title: 'Legal & Compliance',
      icon: ShieldCheck,
      links: [
        { href: '/privacy', label: 'Privacy Policy & Data Security' },
        { href: '/terms', label: 'Terms of Service & Subscription Agreements' },
        { href: '/disclaimers', label: 'FTC, CROA, & IRS Disclaimers' },
      ],
    },
  ]

  return (
    <div className="pt-20">
      {/* Page Title Hero */}
      <section className="relative py-20 bg-muted/30 border-b border-border/40">
        <div className="container mx-auto px-4 max-w-4xl text-center space-y-4">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <Compass className="h-4 w-4 text-brand-gold-600" />
            <span className="text-foreground font-semibold">Directory Navigation Map</span>
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            Sitemap
          </h1>
          <p className="text-sm text-muted-foreground">
            A comprehensive structural map of our elite business, tax, and credit advisory platform.
          </p>
        </div>
      </section>

      {/* Grid of Categories */}
      <section className="py-20 bg-background">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="grid md:grid-cols-3 gap-8">
            {categories.map((cat, idx) => {
              const Icon = cat.icon
              return (
                <div
                  key={idx}
                  className="glass-card rounded-2xl p-8 bg-white dark:bg-zinc-950 border border-border space-y-6 shadow-sm"
                >
                  <div className="flex items-center gap-3 border-b border-border/60 pb-4">
                    <div className="w-10 h-10 rounded-lg bg-brand-gold-500/10 flex items-center justify-center">
                      <Icon className="h-5 w-5 text-brand-gold-600" />
                    </div>
                    <h2 className="text-lg font-bold text-foreground">{cat.title}</h2>
                  </div>
                  <ul className="space-y-4">
                    {cat.links.map((link) => (
                      <li key={link.href}>
                        <Link
                          href={link.href}
                          className="text-sm text-muted-foreground hover:text-brand-gold-600 transition-colors inline-flex items-center gap-2 group leading-relaxed"
                        >
                          <ArrowRight className="h-3.5 w-3.5 text-brand-gold-500 group-hover:translate-x-1 transition-transform" />
                          <span>{link.label}</span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              )
            })}
          </div>

          {/* Quick Support Card */}
          <div className="mt-16 glass-card rounded-2xl p-8 bg-brand-navy-900 text-white text-center space-y-4 max-w-3xl mx-auto">
            <Mail className="h-10 w-10 text-brand-gold-400 mx-auto" />
            <h3 className="text-xl font-bold">Need Administrative Support?</h3>
            <p className="text-sm text-white/80 max-w-xl mx-auto leading-relaxed">
              If you cannot locate a specific service contract, or need assistance accessing your virtual mailbox subscription, reach out directly to our help desk.
            </p>
            <div className="pt-2">
              <Button asChild size="lg" className="shadow-lg">
                <Link href="/contact">
                  Open a Client Ticket
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
