import type { Metadata } from 'next'
import Link from 'next/link'
import { BookOpen, Scale, FileText, ArrowRight, ShieldCheck, Download, HelpCircle, FileCheck2, Info } from 'lucide-react'
import { Button } from '@/components/ui/button'

export const metadata: Metadata = {
  title: 'FCRA, FDCPA & Legal Consumer Resources | Angel Solutions ATL',
  description: 'Understand your consumer protection rights under 15 U.S.C. § 1681 (FCRA) and 15 U.S.C. § 1692 (FDCPA). Free dispute letter templates and compliance breakdowns.',
  alternates: {
    canonical: '/resources',
  },
}

export default function ResourcesPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    'name': 'Legal Consumer Protection Resources & Dispute Guides',
    'description': 'Educational breakdowns of consumer credit protection laws including the FCRA, FDCPA, CROA, and IRS Offer in Compromise formulas.',
    'publisher': {
      '@type': 'LocalBusiness',
      'name': 'Angel Solutions ATL',
      'telephone': '+1-470-338-6689'
    }
  }

  return (
    <div className="pt-20 bg-zinc-950 text-white min-h-screen">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero Section */}
      <section className="relative py-24 overflow-hidden bg-gradient-to-br from-brand-navy-900 via-brand-purple-900/90 to-zinc-950 text-white border-b border-white/5">
        <div className="absolute inset-0 bg-grid-pattern opacity-10" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-gold-500/20 rounded-full blur-3xl" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-4xl">
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
            <Scale className="h-4 w-4 text-brand-gold-400" />
            <span>Educational Compliance & Law Corner</span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            Consumer Protection <span className="text-gold-gradient">Law & Resource Hub</span>
          </h1>
          <p className="text-sm md:text-base text-white/80 max-w-2xl mx-auto leading-relaxed">
            Empower yourself with direct knowledge. Under federal laws, you have strict statutory channels to challenge inaccurate, incomplete, and unverifiable items on your credit reports. Read our attorney-vetted guidance.
          </p>
        </div>
      </section>

      {/* Legal Pillars Cards Section */}
      <section className="py-24 bg-zinc-950 relative">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="grid lg:grid-cols-3 gap-8">
            
            {/* Pillar 1: FCRA */}
            <div className="glass-card-dark rounded-3xl p-8 border border-white/10 space-y-5 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center border border-brand-gold-500/20">
                  <Scale className="h-6 w-6 text-brand-gold-400" />
                </div>
                <h3 className="text-xl font-bold">15 U.S.C. § 1681 — FCRA</h3>
                <p className="text-xs text-white/60 leading-relaxed">
                  The **Fair Credit Reporting Act (FCRA)** is your primary shield. It declares that any reporting bureau must guarantee the **maximum possible accuracy** of all information they publish. If a record contains inaccurate or unverified metrics, bureaus are legally obligated to permanently purge it within 30 days.
                </p>
              </div>
              <Button asChild variant="outline" className="w-full border-white/10 text-white hover:bg-white/5 text-xs">
                <a href="#fcra-guide">Read FCRA Breakdown</a>
              </Button>
            </div>

            {/* Pillar 2: FDCPA */}
            <div className="glass-card-dark rounded-3xl p-8 border border-white/10 space-y-5 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center border border-brand-gold-500/20">
                  <ShieldCheck className="h-6 w-6 text-brand-gold-400" />
                </div>
                <h3 className="text-xl font-bold">15 U.S.C. § 1692 — FDCPA</h3>
                <p className="text-xs text-white/60 leading-relaxed">
                  The **Fair Debt Collection Practices Act (FDCPA)** defines how collection agencies are permitted to interact with you. Collection accounts are highly prone to validation breaches. Third-party collectors structurally fail to hold direct chain-of-title contracts, making their credit lines legally disputable.
                </p>
              </div>
              <Button asChild variant="outline" className="w-full border-white/10 text-white hover:bg-white/5 text-xs">
                <a href="#fdcpa-guide">Read FDCPA Breakdown</a>
              </Button>
            </div>

            {/* Pillar 3: CROA */}
            <div className="glass-card-dark rounded-3xl p-8 border border-white/10 space-y-5 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="w-12 h-12 rounded-xl bg-brand-gold-500/10 flex items-center justify-center border border-brand-gold-500/20">
                  <FileText className="h-6 w-6 text-brand-gold-400" />
                </div>
                <h3 className="text-xl font-bold">15 U.S.C. § 1679 — CROA</h3>
                <p className="text-xs text-white/60 leading-relaxed">
                  The **Credit Repair Organizations Act (CROA)** regulates credit services. We abide by strict, transparent guidelines. No credit organization is legally allowed to charge you upfront fees before work is completed. Always ensure your contract states clear, performance-based billing milestones.
                </p>
              </div>
              <Button asChild variant="outline" className="w-full border-white/10 text-white hover:bg-white/5 text-xs">
                <a href="#croa-guide">Read CROA Disclosures</a>
              </Button>
            </div>

          </div>
        </div>
      </section>

      {/* FCRA Deep Dive & Dispute block */}
      <section id="fcra-guide" className="py-24 bg-zinc-950 border-t border-white/5">
        <div className="container mx-auto px-4 max-w-4xl space-y-12">
          <div className="space-y-4">
            <h2 className="text-2xl md:text-3xl font-bold">FCRA Dispute Mechanics & Bureau Guidelines</h2>
            <div className="h-1 w-20 bg-brand-gold-500 rounded" />
          </div>

          <div className="space-y-6 text-sm text-white/80 leading-relaxed">
            <p>
              Under **15 U.S.C. Section 1681i**, if a consumer disputes the accuracy of an item in their credit file, the consumer reporting agency (Experian, Equifax, TransUnion) must conduct a **reasonable reinvestigation** free of charge. This must occur within 30 days of receiving your formal written dispute.
            </p>
            <p>
              Crucially, if the disputed record is found to be inaccurate, incomplete, or cannot be verified by the creditor within that 30-day window, the bureau must **immediately delete or modify** the record. 
            </p>

            {/* Template Box */}
            <div className="p-6 bg-zinc-900 border border-white/10 rounded-2xl space-y-4 relative">
              <div className="absolute top-4 right-4 text-[10px] text-brand-gold-400 font-mono tracking-widest uppercase bg-brand-gold-500/10 px-2 py-0.5 border border-brand-gold-500/20 rounded">
                Section 609 Letter Template
              </div>
              <h4 className="font-bold text-white flex items-center gap-2">
                <FileCheck2 className="h-4 w-4 text-brand-gold-400" />
                <span>FCRA Bureau Verification Request Block</span>
              </h4>
              <p className="text-xs text-white/50">
                You can copy-paste the text below to draft your first formal verification dispute to be sent directly to the Credit Bureaus via Certified Mail:
              </p>

              <pre className="bg-black/40 p-4 rounded-xl text-[11px] font-mono text-white/90 overflow-x-auto border border-white/5 whitespace-pre-wrap leading-relaxed">
{`[Your Full Name]
[Your Mailing Address]
[Your Social Security Number]
[Your Date of Birth]

To: Experian / Equifax / TransUnion
[Bureau Mailing Address]

Date: [Current Date]

RE: WRITTEN VERIFICATION REQUEST UNDER 15 U.S.C. § 1681

Dear Dispute Department,

I am writing to formally request physical verification of the following accounts reported in my credit file. Under the Fair Credit Reporting Act (15 U.S.C. § 1681i), I have the legal right to challenge the accuracy of any record you publish in my file.

Please provide physical proof of verification (including the original contract or signed application with my signature) for the following reported accounts:

1. Account Name: [Name of Account] | Account Number: [Acct Number]
Reason for dispute: Inaccurate balances and unverified history on record.

If you are unable to produce verifiable physical documentation with my signature within the legally mandated 30-day window, you must immediately delete this account from my credit profile, as required by 15 U.S.C. § 1681i(a)(5).

Sincerely,

___________________________
[Your Signature]`}
              </pre>
              
              <div className="flex items-center gap-2 text-[10px] bg-brand-gold-500/5 text-brand-gold-400 p-3 rounded-lg border border-brand-gold-500/10">
                <Info className="h-4 w-4 flex-shrink-0" />
                <span>IMPORTANT: Always attach a clear photocopy of your driver's license and a utility bill to confirm physical identity when mailing disputes.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FDCPA Collection Rights Breakdown */}
      <section id="fdcpa-guide" className="py-24 bg-zinc-950 border-t border-white/5">
        <div className="container mx-auto px-4 max-w-4xl space-y-12">
          <div className="space-y-4">
            <h2 className="text-2xl md:text-3xl font-bold">FDCPA Collections & Third-Party Limitations</h2>
            <div className="h-1 w-20 bg-brand-gold-500 rounded" />
          </div>

          <div className="space-y-6 text-sm text-white/80 leading-relaxed">
            <p>
              Under the **Fair Debt Collection Practices Act (FDCPA) (15 U.S.C. § 1692)**, third-party collection agencies are strictly forbidden from engaging in deceptive, abusive, or harassing practices. 
            </p>
            <p>
              Crucially, under **15 U.S.C. § 1692g**, if you send a written dispute within 30 days of receiving their initial collection notice, the collector must **cease all collection efforts** until they obtain verification of the debt.
            </p>
            <p className="font-medium text-brand-gold-400">
              Why collections are highly disputable:
            </p>
            <p>
              When a creditor writes off an account and sells it to a third-party debt buyer, the buyer buys records in bulk. They rarely receive the actual signed contract or underlying statements with your signature. Under the law, if they cannot produce these contracts to validate the debt, they are barred from pursuing collection and reporting.
            </p>
          </div>
        </div>
      </section>

      {/* IRS Offer in Compromise Compliance Section */}
      <section id="irs-guide" className="py-24 bg-zinc-950 border-t border-white/5">
        <div className="container mx-auto px-4 max-w-4xl space-y-12">
          <div className="space-y-4">
            <h2 className="text-2xl md:text-3xl font-bold">IRS Offer in Compromise — Settlement Criteria</h2>
            <div className="h-1 w-20 bg-brand-gold-500 rounded" />
          </div>

          <div className="space-y-6 text-sm text-white/80 leading-relaxed">
            <p>
              Under **Internal Revenue Code § 7122**, the IRS is authorized to settle tax debt with qualifying individuals and businesses for less than the full amount owed through the **Offer in Compromise (OIC)** program.
            </p>
            <p>
              Settlement is not arbitrary. The IRS evaluates eligibility using a strict mathematical formula known as **Reasonable Collection Potential (RCP)**:
            </p>
            <div className="p-6 bg-zinc-900 border border-white/10 rounded-2xl space-y-3 font-mono text-xs">
              <p className="font-bold text-white uppercase text-[10px] text-brand-gold-400">The RCP Settlement Equation:</p>
              <div className="p-3 bg-black/40 rounded-lg text-white">
                RCP = (Current Liquid Equity in Assets) + (Remaining Monthly Disposable Income × multiplier)
              </div>
              <p className="text-white/50 text-[10px] leading-relaxed pt-2">
                *Asset Equity includes cash, property, and vehicle values (discounted to quick sale values). Disposable income is calculated by subtracting allowable local housing/utility standards from gross monthly revenue.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* SGE FAQ Accordion Area */}
      <section className="py-24 bg-zinc-950 border-t border-white/5">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center mb-16 space-y-4">
            <div className="inline-flex items-center gap-2 glass-card px-3 py-1 rounded-full text-xs text-brand-gold-400">
              <HelpCircle className="h-3.5 w-3.5" />
              <span>SGE / AI Structured FAQ Overview</span>
            </div>
            <h2 className="text-3xl font-bold">Consumer Rights Frequently Asked Questions</h2>
            <p className="text-muted-foreground text-sm">
              Conversational, factual answers structured to address direct consumer queries about regulatory protection.
            </p>
          </div>

          <div className="space-y-6">
            <div className="glass-card-dark rounded-2xl p-6 border border-white/10">
              <h3 className="text-base font-bold text-white mb-2 flex items-start gap-2">
                <span className="text-brand-gold-400 text-sm mt-0.5">Q.</span>
                Can collections report on my file if they purchased the debt from my original creditor?
              </h3>
              <p className="text-xs md:text-sm text-white/60 leading-relaxed pl-5">
                Yes, they can report, but they must adhere to strict validation regulations. Because they are a third-party and you never signed a direct agreement with them, they must be able to prove they hold the complete, unbroken chain-of-custody transfer records. If they fail to provide complete validation upon receipt of a dispute letter, they are legally required to remove the record.
              </p>
            </div>

            <div className="glass-card-dark rounded-2xl p-6 border border-white/10">
              <h3 className="text-base font-bold text-white mb-2 flex items-start gap-2">
                <span className="text-brand-gold-400 text-sm mt-0.5">Q.</span>
                How long are negative accounts permitted to report on my credit file?
              </h3>
              <p className="text-xs md:text-sm text-white/60 leading-relaxed pl-5">
                Under the FCRA (15 U.S.C. § 1681c), standard negative records (such as collections, late payments, or charge-offs) are legally permitted to remain on your consumer files for a maximum of **7 years** from the original date of delinquency. Chapter 7 bankruptcies can report for up to **10 years**. Any reporting beyond these limits is a severe violation of the FCRA.
              </p>
            </div>

            <div className="glass-card-dark rounded-2xl p-6 border border-white/10">
              <h3 className="text-base font-bold text-white mb-2 flex items-start gap-2">
                <span className="text-brand-gold-400 text-sm mt-0.5">Q.</span>
                What is an IRS tax levy and how do I prevent it?
              </h3>
              <p className="text-xs md:text-sm text-white/60 leading-relaxed pl-5">
                An IRS levy is a legal seizure of your assets (including bank garnishments or wage garnishments) to satisfy tax liabilities. To prevent a levy, you must respond to the IRS "Notice of Intent to Levy" within 30 days and file for a Collection Due Process (CDP) hearing. This freezes all seizure actions while we negotiate an installment agreement, Currently Not Collectible (CNC) status, or an Offer in Compromise.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="py-20 relative overflow-hidden bg-brand-navy-900 text-white border-t border-white/5">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="container mx-auto px-4 relative z-10 text-center space-y-6 max-w-3xl">
          <h2 className="text-3xl font-bold">Empower Your Financial Credibility</h2>
          <p className="text-sm text-white/80 leading-relaxed max-w-2xl mx-auto">
            Don't let inaccurate reporting or overwhelming tax burdens stall your future. Schedule a complete, direct consultation with Jordynn Miller and lock in your restoral action plan today.
          </p>
          <div className="pt-4 flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="xl" className="shadow-2xl">
              <Link href="/contact">
                Schedule My Free Strategy Session
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild size="xl" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <Link href="/funding-eligibility">Run My Funding Scanner</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
