import type { Metadata } from 'next'
import Link from 'next/link'
import { Shield, Lock, Eye, CheckCircle2, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'Privacy Policy | Angel Solutions ATL',
  description: 'Learn how Angel Solutions ATL collects, protects, and syncs your business and personal data. Full TCPA, CCPA, and CAN-SPAM compliance guidelines.',
  alternates: {
    canonical: '/privacy',
  },
}

export default function PrivacyPage() {
  const lastUpdated = 'April 18, 2026'

  return (
    <div className="pt-20">
      {/* Page Title Hero */}
      <section className="relative py-20 bg-muted/30 border-b border-border/40">
        <div className="container mx-auto px-4 max-w-4xl text-center space-y-4">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <Shield className="h-4 w-4 text-brand-gold-600" />
            <span className="text-foreground font-semibold">Legal & Security Operations</span>
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            Privacy Policy
          </h1>
          <p className="text-sm text-muted-foreground">
            Last Updated: {lastUpdated} | Active Version 9.0
          </p>
        </div>
      </section>

      {/* Policy Content */}
      <section className="py-20 bg-background text-foreground">
        <div className="container mx-auto px-4 max-w-4xl prose dark:prose-invert prose-brand-gold prose-sm">
          <div className="glass-card rounded-2xl p-6 bg-brand-gold-500/5 border border-brand-gold-500/20 mb-10 flex gap-4 items-start">
            <Lock className="h-6 w-6 text-brand-gold-600 mt-1 flex-shrink-0" />
            <div>
              <h4 className="font-bold text-foreground mb-1">Our Data Protection Promise</h4>
              <p className="text-xs text-muted-foreground leading-relaxed m-0">
                Angel Solutions ATL is fully committed to absolute privacy. All lead captures, virtual office registrations, and client interaction records are secured using enterprise-grade V8 execution isolates, protected Cloudflare D1 databases, and 256-bit SSL encryption. We never rent, sell, or lease your private information to third parties.
              </p>
            </div>
          </div>

          <h2 className="text-xl font-bold mt-8 mb-4">1. Information We Collect</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            When you visit our website, schedule a consultation, or purchase our business, tax, or financial packages, we collect the following types of information:
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li><strong>Personal Identifiers:</strong> Name, physical address, business address, email, telephone number, and company name.</li>
            <li><strong>Business Entity Identifiers:</strong> Employer Identification Number (EIN), state filing status, and Dun & Bradstreet registry profiles.</li>
            <li><strong>Financial and Billing Information:</strong> Payments are processed securely via Stripe. We do not store full credit card numbers on our servers.</li>
            <li><strong>Technical and Analytics Metadata:</strong> IP address, device type, browser, referring page, and session data collected via cookies to optimize performance.</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">2. CRM and Database Synchronizations</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            In compliance with our dual-retention systems, any information you submit through our web forms is stored on our secure Cloudflare D1 remote database and simultaneously routed via HTTPS webhooks directly into our **GoHighLevel CRM (GHL)**. 
          </p>
          <p className="text-sm text-muted-foreground leading-relaxed">
            This synchronization enables us to immediately tag your profile with marketing and attribution tracking tags (specifically tracking that you originated from our premium website) to monitor conversions, automate response workflows, and deliver professional SMS notifications without human delay.
          </p>

          <h2 className="text-xl font-bold mt-10 mb-4">3. Explicit SMS and Text Messaging Terms (TCPA Compliance)</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            We adhere strictly to the Fair Debt Collection Practices Act (FDCPA) and the Telephone Consumer Protection Act (TCPA). By providing your mobile telephone number on any form or button on our site, you grant Angel Solutions ATL explicit written consent to send informational, transaction-related, and promotional SMS notifications.
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li>SMS delivery is automated through our integrated GHL webhook configurations.</li>
            <li>Consent is not a prerequisite to purchasing any service or package.</li>
            <li>You can opt-out at any time by replying <strong>STOP</strong> to any message. Reply <strong>HELP</strong> for customer support. Message and data rates may apply.</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">4. Compliance with CCPA & CAN-SPAM</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Under the California Consumer Privacy Act (CCPA), California residents have the right to request access to, deletion of, or details about the processing of their personal data. Furthermore, our marketing email communications comply with CAN-SPAM mandates, containing clear unsubscribe mechanisms in every footer.
          </p>

          <h2 className="text-xl font-bold mt-10 mb-4">5. Contacting Our Privacy Officer</h2>
          <p className="text-sm text-muted-foreground leading-relaxed mb-10">
            If you have any questions about this Privacy Policy, your data rights, or the storage mechanisms on our D1 databases, please contact our legal compliance team at <a href="mailto:info@angelsolutionsatl.com" className="text-brand-gold-600 font-bold hover:underline">info@angelsolutionsatl.com</a>.
          </p>

          <div className="pt-8 border-t border-border/40 text-center">
            <Button asChild size="lg" className="shadow-lg">
              <Link href="/contact">
                Review Our Secure Consultation Portal
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
