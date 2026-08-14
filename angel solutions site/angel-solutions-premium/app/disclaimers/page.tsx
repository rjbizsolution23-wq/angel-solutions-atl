import type { Metadata } from 'next'
import Link from 'next/link'
import { AlertTriangle, ShieldCheck, Landmark, CheckCircle2, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'Compliance & Legal Disclaimers | Angel Solutions ATL',
  description: 'Understand the legal frameworks, compliance disclosures, and consumer protection guidelines governing Angel Solutions ATL services.',
  alternates: {
    canonical: '/disclaimers',
  },
}

export default function DisclaimersPage() {
  const lastUpdated = 'April 18, 2026'

  return (
    <div className="pt-20">
      {/* Page Title Hero */}
      <section className="relative py-20 bg-muted/30 border-b border-border/40">
        <div className="container mx-auto px-4 max-w-4xl text-center space-y-4">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <AlertTriangle className="h-4 w-4 text-brand-gold-600" />
            <span className="text-foreground font-semibold">Regulatory Disclosures & Disclaimers</span>
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            Compliance & Disclaimers
          </h1>
          <p className="text-sm text-muted-foreground">
            Effective Date: {lastUpdated} | Version 9.0 (FTC, CROA, Circular 230 Compliant)
          </p>
        </div>
      </section>

      {/* Disclaimer Content */}
      <section className="py-20 bg-background text-foreground">
        <div className="container mx-auto px-4 max-w-4xl prose dark:prose-invert prose-brand-gold prose-sm">
          <div className="glass-card rounded-2xl p-6 bg-brand-gold-500/5 border border-brand-gold-500/20 mb-10 flex gap-4 items-start">
            <ShieldCheck className="h-6 w-6 text-brand-gold-600 mt-1 flex-shrink-0" />
            <div>
              <h4 className="font-bold text-foreground mb-1">Our Commitment to Compliance</h4>
              <p className="text-xs text-muted-foreground leading-relaxed m-0">
                Angel Solutions ATL operates under strict standards of consumer finance law, federal trade regulations, and IRS procedural guidelines. This disclosure page outlines our limitations of service to ensure full clarity, security, and alignment with federal, state, and local laws.
              </p>
            </div>
          </div>

          <h2 className="text-xl font-bold mt-8 mb-4">1. Non-Legal and Non-Accounting Representation</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Angel Solutions ATL is a premium business development, tax resolution support, and financial optimization consulting firm. 
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li><strong>No Legal Advice:</strong> The information provided on this website, during consults, or in our packages does not constitute formal legal advice. For formal legal representation or legal drafting beyond administrative document preparation, you must consult a licensed attorney.</li>
            <li><strong>No CPA/Audit Representation:</strong> Our tax resolution services involve compiling unfiled back taxes, evaluating reasonable collection potentials, and preparing Offer in Compromise documentations. We do not act as certified public accounting firms or represent clients before the tax court unless explicitly authorized under written Power of Attorney (Form 2848).</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">2. Credit Repair Organizations Act (CROA) & FTC Disclosures</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            In complete compliance with the Fair Trade Commission (FTC) and the **Credit Repair Organizations Act (CROA)** (15 U.S.C. § 1679):
          </p>
          <ul className="text-sm text-muted-foreground leading-relaxed list-disc pl-6 space-y-2">
            <li><strong>No Guaranteed Outcomes:</strong> Angel Solutions ATL does not make false, unverified, or misleading promises of overnight "credit wipes" or "erasing" accurate and verified derogatory marks from your credit history. No credit repair agency has the legal authority to do so.</li>
            <li><strong>Educational Methodology:</strong> We consult, guide, and instruct clients on statutory disputing procedures under the Fair Credit Reporting Act (FCRA) and Fair Debt Collection Practices Act (FDCPA) to challenge inaccurate, incomplete, or outdated listings.</li>
            <li><strong>Statutory Rights:</strong> Under the FCRA, consumers have the legal right to challenge inaccuracies themselves directly with credit bureaus for free. Engagement of our advisory services is entirely voluntary.</li>
          </ul>

          <h2 className="text-xl font-bold mt-10 mb-4">3. IRS Circular 230 Tax Disclaimers</h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Pursuant to IRS Circular 230 regulations, any tax advice or educational information contained on this site is not intended to be used, and cannot be used, by any taxpayer for the purpose of avoiding tax-related penalties that may be imposed by the Internal Revenue Service (IRS). Tax situations are unique, and you must review your individual records and transcripts with our advisors prior to negotiating compromises.
          </p>

          <h2 className="text-xl font-bold mt-10 mb-4">4. Business Funding & Credibility Projections</h2>
          <p className="text-sm text-muted-foreground leading-relaxed mb-10">
            While establishing an LLC, obtaining an EIN, setting up corporate trade lines, and securing a Dun & Bradstreet rating are essential steps to building business credibility, Angel Solutions ATL does not guarantee that lenders will approve your company for corporate credit, commercial loans, or business lines of credit. Underwriting decisions are at the sole discretion of the lending institutions and depend on creditworthiness, time in business, revenues, and market conditions.
          </p>

          <div className="pt-8 border-t border-border/40 text-center">
            <Button asChild size="lg" className="shadow-lg">
              <Link href="/terms">
                Review Our Terms of Service
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
