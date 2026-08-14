import type { Metadata } from 'next'
import Link from 'next/link'
import { FileText, CheckCircle, HelpCircle, ShieldAlert, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'Terms of Service | Angel Solutions ATL',
  description: 'Review the Terms of Service for Angel Solutions ATL. Agreements governing business formation, virtual office subscriptions, and tax advisory services.',
  alternates: {
    canonical: '/terms',
  },
}

export default function TermsPage() {
  const lastUpdated = 'April 18, 2026'

  return (
    <div className="pt-20">
      {/* Page Title Hero */}
      <section className="relative py-20 bg-muted/30 border-b border-border/40">
        <div className="container mx-auto px-4 max-w-4xl text-center space-y-4">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <FileText className="h-4 w-4 text-brand-gold-600" />
            <span className="text-foreground font-semibold">User Agreements & Retainers</span>
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            Terms of Service
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
            <ShieldAlert className="h-6 w-6 text-brand-gold-600 mt-1 flex-shrink-0" />
            <div>
              <h4 className="font-bold text-foreground mb-1">Binding Legal Agreement</h4>
              <p className="text-xs text-muted-foreground leading-relaxed m-0">
                Please review these Terms of Service carefully before utilizing our website or subscribing to any of our turnkey programs. By accessing our services, submitting a form, or purchasing a package, you agree to be bound by these Terms and our Privacy Policy.
              </p>
            </div>
          </div>

          <h2 className="text-xl font-bold mt-8 mb-4">1. Scope of Services Offered</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Angel Solutions ATL provides administrative document preparation, business formation consulting, virtual office leasing, and tax audit resolution support. 
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li><strong>Business Formation:</strong> Preparation and filing of Articles of Organization with state registries, EIN applications, and operating agreements.</li>
            <li><strong>Virtual Office Subscription:</strong> Providing secure business mailing addresses, digital mail forwarding, and telephone reception configurations.</li>
            <li><strong>Tax Resolution:</strong> Back tax organization, audit document compilation, and negotiating compromise installment frameworks with tax authorities.</li>
            <li><strong>Financial Optimization:</strong> Structured educational programs focused on personal budgeting, statutory credit dispute procedures, and corporate credit establishment.</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">2. Subscription Billing & Payment Processing</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            All services and packages are billed via our secure **Stripe payment gateway**. Prices and intervals depend on the select package:
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li><strong>Turnkey Business Packages:</strong> Elite, Authority, and Enterprise configurations require a one-time setup fee ranging from $450 to $650.</li>
            <li><strong>Virtual Office Subscriptions:</strong> Billed on a recurring monthly or annual basis at interval thresholds of $10, $39.99, or $100 depending on the service level.</li>
            <li><strong>Tax Resolution Retainers:</strong> Billed as structured custom flat fees or milestones upon initiating a written Power of Attorney agreement.</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">3. Refund, Cancellation, & Billing Failures</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            We operate in strict conformity with consumer finance rules and professional standards:
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li><strong>One-Time Packages:</strong> Due to immediate costs incurred for state filing fees, entity name reservations, and Dun & Bradstreet setups, setup package payments are non-refundable once filing has commenced.</li>
            <li><strong>Subscription Cancellation:</strong> You can cancel recurring virtual office subscriptions at any time via our Stripe self-service customer portal. Cancellation takes effect at the end of the current billing cycle.</li>
            <li><strong>Delinquency & Interruption:</strong> If a subscription payment fails, Stripe will automatically re-attempt charge captures. If unpaid for 7 business days, mailing office services are suspended and any physical mail will be held or returned.</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">4. GoHighLevel CRM & SMS Delivery Agreements</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            We use Hono Workers and GoHighLevel (GHL) webhooks to automatically enroll you in our workflow pipelines, send text updates on your filing status, and track conversions. You agree to receive these automated communications. Standard carrier text rates apply. You may opt-out of text communications at any time by texting <strong>STOP</strong>.
          </p>

          <h2 className="text-xl font-bold mt-10 mb-4">5. Limitation of Liability & Dispute Resolution</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Angel Solutions ATL is an administrative advisory firm, not a law firm or registered investment firm. Our consultations and document preparations are educational and advisory. We are not liable for business operational failures, state registry delays, or tax settlement rejections by the IRS.
          </p>
          <p className="text-sm text-muted-foreground leading-relaxed mb-10">
            These Terms shall be governed by, and construed in accordance with, the laws of the **State of Georgia**, without regard to conflict of law principles. Any dispute arising out of or relating to these terms shall be resolved exclusively in the state and federal courts located in Fulton County, Georgia.
          </p>

          <div className="pt-8 border-t border-border/40 text-center">
            <Button asChild size="lg" className="shadow-lg">
              <Link href="/privacy">
                Review Our Privacy Policy
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
