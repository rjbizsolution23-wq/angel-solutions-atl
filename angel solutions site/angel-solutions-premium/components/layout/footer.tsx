'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Facebook, Twitter, Instagram, Linkedin, Mail, Phone, MapPin } from 'lucide-react'
import { SITE_CONFIG, NAV_LINKS } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function Footer() {
  const currentYear = new Date().getFullYear()

  const [newsEmail, setNewsEmail] = useState('')
  const [newsSubmitted, setNewsSubmitted] = useState(false)
  const [newsSubmitting, setNewsSubmitting] = useState(false)

  const handleNewsSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!newsEmail) return
    setNewsSubmitting(true)
    try {
      const response = await fetch('https://angel-solutions-webhook.rickjefferson.workers.dev/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          firstName: 'Newsletter',
          lastName: 'Subscriber',
          email: newsEmail,
          phone: '',
          service: 'consultation',
          message: 'Subscribed to newsletter from website footer.',
          platform: 'website',
          intake_id: '6a46c0696b95e7dc9dd6251c',
        }),
      })
      if (response.ok) {
        setNewsSubmitted(true)
        setNewsEmail('')
      } else {
        alert('Failed to subscribe. Please try again.')
      }
    } catch (err) {
      console.error(err)
    } finally {
      setNewsSubmitting(false)
      setTimeout(() => setNewsSubmitted(false), 4000)
    }
  }

  return (
    <footer className="relative border-t border-border/40 bg-gradient-to-b from-background to-muted/30">
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
          {/* Company Info */}
          <div className="space-y-6">
            <Link href="/" className="inline-flex items-center gap-3 group">
              <div className="relative w-12 h-12 flex items-center justify-center transition-all duration-300 group-hover:scale-110">
                <Image
                  src="/assets/logos/primary/logos-primary-2446f0_364e0a9712d24cc39d9b1ab72f9212a8.png"
                  alt="Angel Solutions ATL Logo"
                  fill
                  className="object-contain"
                />
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold text-foreground">
                  Angel Solutions ATL
                </span>
                <span className="text-xs text-muted-foreground">ATL</span>
              </div>
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Empowering business growth through elite business formation, tax resolution, and financial solutions. Your success is our mission.
            </p>
            <div className="flex gap-3">
              {[
                { icon: Facebook, href: SITE_CONFIG.social.facebook, label: 'Facebook' },
                { icon: Twitter, href: SITE_CONFIG.social.twitter, label: 'Twitter' },
                { icon: Instagram, href: SITE_CONFIG.social.instagram, label: 'Instagram' },
                { icon: Linkedin, href: SITE_CONFIG.social.linkedin, label: 'LinkedIn' },
              ].map(({ icon: Icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-full bg-muted hover:bg-brand-gold-500 flex items-center justify-center transition-all duration-300 hover:scale-110 hover:shadow-lg group"
                  aria-label={label}
                >
                  <Icon className="h-5 w-5 text-muted-foreground group-hover:text-white transition-colors" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-bold mb-6 text-foreground">Quick Links</h3>
            <ul className="space-y-3">
              {NAV_LINKS.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-muted-foreground hover:text-brand-gold-600 transition-colors inline-flex items-center gap-2 group"
                  >
                    <span className="w-0 h-px bg-brand-gold-500 group-hover:w-4 transition-all duration-300" />
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-lg font-bold mb-6 text-foreground">Our Services</h3>
            <ul className="space-y-3">
              {[
                { label: 'Business Formation', href: '/business-solutions' },
                { label: 'LLC Registration', href: '/business-solutions' },
                { label: 'Tax Preparation', href: '/tax-solutions' },
                { label: 'Tax Debt Resolution', href: '/tax-solutions' },
                { label: 'Credit Optimization', href: '/financial-solutions' },
                { label: 'Business Funding', href: '/financial-solutions' },
              ].map((service) => (
                <li key={service.label}>
                  <Link
                    href={service.href}
                    className="text-sm text-muted-foreground hover:text-brand-gold-600 transition-colors inline-flex items-center gap-2 group"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-brand-gold-500 group-hover:scale-125 transition-transform" />
                    {service.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact & Newsletter */}
          <div>
            <h3 className="text-lg font-bold mb-6 text-foreground">Get in Touch</h3>
            <div className="space-y-4 mb-6">
              <a
                href={`mailto:${SITE_CONFIG.email}`}
                className="flex items-start gap-3 text-sm text-muted-foreground hover:text-brand-gold-600 transition-colors group"
              >
                <Mail className="h-5 w-5 mt-0.5 flex-shrink-0 group-hover:text-brand-gold-600" />
                <span>{SITE_CONFIG.email}</span>
              </a>
              <a
                href={`tel:${SITE_CONFIG.phone}`}
                className="flex items-start gap-3 text-sm text-muted-foreground hover:text-brand-gold-600 transition-colors group"
              >
                <Phone className="h-5 w-5 mt-0.5 flex-shrink-0 group-hover:text-brand-gold-600" />
                <span>{SITE_CONFIG.phone}</span>
              </a>
              <div className="flex items-start gap-3 text-sm text-muted-foreground">
                <MapPin className="h-5 w-5 mt-0.5 flex-shrink-0" />
                <span>{SITE_CONFIG.address.street}<br />{SITE_CONFIG.address.city}, {SITE_CONFIG.address.state}</span>
              </div>
            </div>

            {/* Newsletter Signup */}
            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-foreground">Stay Updated</h4>
              <form onSubmit={handleNewsSubmit} className="flex gap-2">
                <Input
                  type="email"
                  placeholder="Your email"
                  className="h-10 text-sm"
                  value={newsEmail}
                  onChange={(e) => setNewsEmail(e.target.value)}
                  disabled={newsSubmitting || newsSubmitted}
                  required
                />
                <Button type="submit" size="sm" className="px-4" disabled={newsSubmitting || newsSubmitted}>
                  {newsSubmitting ? '...' : newsSubmitted ? '✓' : 'Subscribe'}
                </Button>
              </form>
              <p className="text-xs text-muted-foreground">
                {newsSubmitted ? 'Successfully subscribed!' : 'Get the latest updates and exclusive offers.'}
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-border/40">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex flex-col md:flex-row items-center gap-2 md:gap-4 text-sm text-muted-foreground text-center md:text-left">
              <span>© {currentYear} {SITE_CONFIG.name} Ltd Co. All rights reserved.</span>
              <span className="hidden md:inline text-white/10">|</span>
              <span>
                Made by{' '}
                <a
                  href="https://angelsolutionsatl.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-brand-gold-400 font-semibold transition-colors underline decoration-brand-gold-500/30 underline-offset-4"
                >
                  Jordynn Miller | Angel Solutions ATL
                </a>
              </span>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-6 text-sm">
              <Link href="/privacy" className="text-muted-foreground hover:text-brand-gold-600 transition-colors">
                Privacy Policy
              </Link>
              <Link href="/terms" className="text-muted-foreground hover:text-brand-gold-600 transition-colors">
                Terms of Service
              </Link>
              <Link href="/disclaimers" className="text-muted-foreground hover:text-brand-gold-600 transition-colors">
                Disclaimers
              </Link>
              <Link href="/sitemap" className="text-muted-foreground hover:text-brand-gold-600 transition-colors">
                Sitemap
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Decorative elements */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-brand-gold-500/50 to-transparent" />
    </footer>
  )
}
