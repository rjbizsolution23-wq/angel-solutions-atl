'use client'

import * as React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Shield, Sparkles, Building2, Landmark, Coins, CheckCircle, ArrowRight, ArrowLeft, Loader2, AlertTriangle, FileSpreadsheet } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import Link from 'next/link'

export default function FundingEligibilityPage() {
  const [step, setStep] = React.useState(1)
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [submitted, setSubmitted] = React.useState(false)

  // Form Fields State
  const [formData, setFormData] = React.useState({
    businessName: '',
    entityType: 'LLC',
    yearsInBusiness: '1-2',
    hasEIN: 'yes',
    hasDUNS: 'no',
    hasCommercialAddress: 'no',
    hasBusinessBank: 'yes',
    monthlyDeposits: '5k-10k',
    merchantAccount: 'no',
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
  })

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  // Scoring and Capacity Algorithm
  const evaluateFunding = () => {
    let credibilityScore = 20
    let estimatedMin = 0
    let estimatedMax = 0
    const recommendations: string[] = []

    // 1. Bank Account Rejection Check
    if (formData.hasBusinessBank === 'no') {
      return {
        score: 15,
        min: 0,
        max: 0,
        rejection: 'Lenders structurally require an active business checking account to verify business cash flow. Running business operations out of personal accounts leads to instant credit card and line declines.',
        recs: [
          'Open a dedicated business checking account immediately.',
          'Secure our Business Formation Starter Package to get legal EIN & filing articles to open your bank account.'
        ]
      }
    }

    // 2. Base Credibility Check
    if (formData.hasEIN === 'yes') credibilityScore += 20
    else recommendations.push('Register a federal EIN for tax tracking.')

    if (formData.hasDUNS === 'yes') credibilityScore += 20
    else recommendations.push('Secure a Dun & Bradstreet D-U-N-S number to start reporting Net-30 vendor lines.')

    if (formData.hasCommercialAddress === 'yes') credibilityScore += 15
    else recommendations.push('Adopt a real commercial mailing address instead of a home/PO Box (major lender red flag).')

    if (formData.yearsInBusiness === '3+') credibilityScore += 25
    else if (formData.yearsInBusiness === '1-2') credibilityScore += 15
    else credibilityScore += 5

    // 3. Deposit Multipliers
    let depositMultiplier = 1.0
    if (formData.monthlyDeposits === '25k+') {
      depositMultiplier = 4.5
      credibilityScore += 10
    } else if (formData.monthlyDeposits === '10k-25k') {
      depositMultiplier = 2.5
      credibilityScore += 8
    } else if (formData.monthlyDeposits === '5k-10k') {
      depositMultiplier = 1.2
      credibilityScore += 5
    } else {
      depositMultiplier = 0.4
    }

    if (formData.merchantAccount === 'yes') {
      depositMultiplier *= 1.2
    }

    // Baseline calculation based on deposits
    const depositBase = formData.monthlyDeposits === '25k+' ? 35000 :
                        formData.monthlyDeposits === '10k-25k' ? 15000 :
                        formData.monthlyDeposits === '5k-10k' ? 5000 : 1500

    estimatedMin = Math.round(depositBase * depositMultiplier * (credibilityScore / 80))
    estimatedMax = Math.round(depositBase * 1.5 * depositMultiplier * (credibilityScore / 70))

    if (credibilityScore < 50) {
      recommendations.push('Establish Net-30 corporate credit reporting trade lines (e.g., Quill, Uline, Grainger).')
    }

    return {
      score: Math.min(100, credibilityScore),
      min: Math.max(2500, Math.round(estimatedMin / 500) * 500),
      max: Math.round(estimatedMax / 1000) * 1000,
      rejection: null,
      recs: recommendations.length > 0 ? recommendations : ['Maintain consistent monthly revenue deposits.', 'Keep credit utilization below 10% on business lines.']
    }
  }

  const evaluation = evaluateFunding()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Construct unified lead payload
    const payload = {
      firstName: formData.firstName,
      lastName: formData.lastName,
      email: formData.email,
      phone: formData.phone,
      service: 'business_funding',
      message: `Eligibility Tool Completed. Estimated score: ${evaluation.score}/100. Capacity: $${evaluation.min}-$${evaluation.max}. Has Bank Acc: ${formData.hasBusinessBank}.`,
      platform: 'website',
      intake_id: '6a46c0696b95e7dc9dd6251c',
      utm_source: 'funding_calculator'
    }

    try {
      const response = await fetch('https://angel-solutions-webhook.rickjefferson.workers.dev/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        setSubmitted(true)
      }
    } catch (err) {
      console.error('Failed to sync eligibility lead:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="pt-20 min-h-screen bg-zinc-950 text-white flex flex-col justify-center relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-gold-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-brand-purple-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="container mx-auto px-4 py-16 relative z-10 max-w-3xl">
        <div className="text-center space-y-4 mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs text-brand-gold-400">
            <Shield className="h-3.5 w-3.5" />
            <span>Fiduciary Funding Pre-Audit</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
            Corporate <span className="text-gold-gradient">Funding & Credibility</span> Scanner
          </h1>
          <p className="text-sm md:text-base text-white/60 max-w-xl mx-auto">
            Audit your corporate files against underwriter checklists to compute your borrowing strength and lock in targeted funding.
          </p>
        </div>

        {/* Progress Bar */}
        {!submitted && (
          <div className="mb-8 max-w-md mx-auto">
            <div className="flex justify-between text-xs text-white/40 mb-2">
              <span>Step {step} of 4</span>
              <span>{Math.round((step / 4) * 100)}% Complete</span>
            </div>
            <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-brand-gold-500 to-amber-400"
                animate={{ width: `${(step / 4) * 100}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
        )}

        <AnimatePresence mode="wait">
          {!submitted ? (
            <motion.div
              key={step}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
              className="glass-card-dark rounded-3xl p-6 md:p-10 border border-white/10 shadow-2xl relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-64 h-64 bg-brand-gold-500/5 rounded-full blur-3xl -z-10 pointer-events-none" />

              {/* STEP 1: Business Profile */}
              {step === 1 && (
                <div className="space-y-6">
                  <div className="space-y-2">
                    <h2 className="text-xl md:text-2xl font-bold flex items-center gap-2">
                      <Building2 className="h-5 w-5 text-brand-gold-400" />
                      <span>Corporate Entity Profile</span>
                    </h2>
                    <p className="text-xs text-white/50">Provide your official filing details to review corporate record formatting.</p>
                  </div>

                  <div className="space-y-4">
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">Filing Legal Business Name</label>
                      <Input
                        type="text"
                        placeholder="e.g. Angel Solutions ATL LLC"
                        value={formData.businessName}
                        onChange={(e) => handleChange('businessName', e.target.value)}
                        className="bg-white/5 border-white/10 text-white focus:border-brand-gold-500"
                      />
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <label className="text-xs font-semibold text-white/80">Entity Structure</label>
                        <select
                          value={formData.entityType}
                          onChange={(e) => handleChange('entityType', e.target.value)}
                          className="w-full h-10 px-3 bg-zinc-900 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:ring-1 focus:ring-brand-gold-500 focus:border-brand-gold-500"
                        >
                          <option value="LLC">Limited Liability Company (LLC)</option>
                          <option value="S-Corp">S-Corporation (S-Corp)</option>
                          <option value="C-Corp">C-Corporation (C-Corp)</option>
                          <option value="Sole-Prop">Sole Proprietorship</option>
                        </select>
                      </div>

                      <div className="space-y-2">
                        <label className="text-xs font-semibold text-white/80">Filing Age (Years in Business)</label>
                        <select
                          value={formData.yearsInBusiness}
                          onChange={(e) => handleChange('yearsInBusiness', e.target.value)}
                          className="w-full h-10 px-3 bg-zinc-900 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:ring-1 focus:ring-brand-gold-500 focus:border-brand-gold-500"
                        >
                          <option value="0-1">Startup / Under 1 year</option>
                          <option value="1-2">1 to 2 Years (Standard threshold)</option>
                          <option value="3+">3+ Years (Seasoned Entity)</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 flex justify-end">
                    <Button
                      onClick={() => setStep(2)}
                      disabled={!formData.businessName}
                      className="gap-2 px-6"
                    >
                      <span>Continue Audit</span>
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}

              {/* STEP 2: Credibility Markers */}
              {step === 2 && (
                <div className="space-y-6">
                  <div className="space-y-2">
                    <h2 className="text-xl md:text-2xl font-bold flex items-center gap-2">
                      <Landmark className="h-5 w-5 text-brand-gold-400" />
                      <span>Credibility Registry & Compliance</span>
                    </h2>
                    <p className="text-xs text-white/50">Underwriters scan these state & federal systems automatically on submission.</p>
                  </div>

                  <div className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      {/* EIN */}
                      <div className="space-y-2">
                        <label className="text-xs font-semibold text-white/80">Has Federal EIN (Tax ID)?</label>
                        <div className="flex gap-4">
                          {['yes', 'no'].map((opt) => (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => handleChange('hasEIN', opt)}
                              className={`flex-1 py-2 rounded-lg text-xs font-bold border capitalize transition-all ${formData.hasEIN === opt ? 'bg-brand-gold-500/20 border-brand-gold-500 text-white' : 'border-white/10 text-white/60 hover:bg-white/5'}`}
                            >
                              {opt}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Business Bank Account */}
                      <div className="space-y-2">
                        <label className="text-xs font-semibold text-white/80">Has Active Business Checking?</label>
                        <div className="flex gap-4">
                          {['yes', 'no'].map((opt) => (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => handleChange('hasBusinessBank', opt)}
                              className={`flex-1 py-2 rounded-lg text-xs font-bold border capitalize transition-all ${formData.hasBusinessBank === opt ? 'bg-brand-gold-500/20 border-brand-gold-500 text-white' : 'border-white/10 text-white/60 hover:bg-white/5'}`}
                            >
                              {opt}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      {/* DUNS */}
                      <div className="space-y-2">
                        <label className="text-xs font-semibold text-white/80">Has Dun & Bradstreet Profile (D-U-N-S)?</label>
                        <div className="flex gap-4">
                          {['yes', 'no'].map((opt) => (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => handleChange('hasDUNS', opt)}
                              className={`flex-1 py-2 rounded-lg text-xs font-bold border capitalize transition-all ${formData.hasDUNS === opt ? 'bg-brand-gold-500/20 border-brand-gold-500 text-white' : 'border-white/10 text-white/60 hover:bg-white/5'}`}
                            >
                              {opt}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Commercial Address */}
                      <div className="space-y-2">
                        <label className="text-xs font-semibold text-white/80">Has Real Commercial Address? (No PO Box/Home)</label>
                        <div className="flex gap-4">
                          {['yes', 'no'].map((opt) => (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => handleChange('hasCommercialAddress', opt)}
                              className={`flex-1 py-2 rounded-lg text-xs font-bold border capitalize transition-all ${formData.hasCommercialAddress === opt ? 'bg-brand-gold-500/20 border-brand-gold-500 text-white' : 'border-white/10 text-white/60 hover:bg-white/5'}`}
                            >
                              {opt}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 flex justify-between">
                    <Button variant="ghost" onClick={() => setStep(1)} className="gap-2 text-white/60 hover:text-white">
                      <ArrowLeft className="h-4 w-4" />
                      <span>Back</span>
                    </Button>
                    <Button onClick={() => setStep(3)} className="gap-2 px-6">
                      <span>Continue Audit</span>
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}

              {/* STEP 3: Financials */}
              {step === 3 && (
                <div className="space-y-6">
                  <div className="space-y-2">
                    <h2 className="text-xl md:text-2xl font-bold flex items-center gap-2">
                      <Coins className="h-5 w-5 text-brand-gold-400" />
                      <span>Corporate Revenue Audit</span>
                    </h2>
                    <p className="text-xs text-white/50">Your monthly cash-flow health dictates your instant borrowing limits.</p>
                  </div>

                  <div className="space-y-6">
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">Monthly Gross Bank Deposits (Averaged)</label>
                      <select
                        value={formData.monthlyDeposits}
                        onChange={(e) => handleChange('monthlyDeposits', e.target.value)}
                        className="w-full h-10 px-3 bg-zinc-900 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:ring-1 focus:ring-brand-gold-500 focus:border-brand-gold-500"
                      >
                        <option value="0-5k">Under $5,000 / month</option>
                        <option value="5k-10k">$5,000 to $10,000 / month</option>
                        <option value="10k-25k">$10,000 to $25,000 / month</option>
                        <option value="25k+">$25,000+ / month (Cash flow seasoned)</option>
                      </select>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">Does your business accept credit cards via Merchant Accounts?</label>
                      <div className="flex gap-4">
                        {['yes', 'no'].map((opt) => (
                          <button
                            key={opt}
                            type="button"
                            onClick={() => handleChange('merchantAccount', opt)}
                            className={`flex-1 py-2 rounded-lg text-xs font-bold border capitalize transition-all ${formData.merchantAccount === opt ? 'bg-brand-gold-500/20 border-brand-gold-500 text-white' : 'border-white/10 text-white/60 hover:bg-white/5'}`}
                          >
                            {opt}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 flex justify-between">
                    <Button variant="ghost" onClick={() => setStep(2)} className="gap-2 text-white/60 hover:text-white">
                      <ArrowLeft className="h-4 w-4" />
                      <span>Back</span>
                    </Button>
                    <Button onClick={() => setStep(4)} className="gap-2 px-6">
                      <span>Generate Scores</span>
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}

              {/* STEP 4: Submit & Access Results */}
              {step === 4 && (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <h2 className="text-xl md:text-2xl font-bold flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-brand-gold-400" />
                      <span>Secure Your Pre-Audit Report</span>
                    </h2>
                    <p className="text-xs text-white/50">Enter your contact details to run the calculation engine and lock in your funding advisor consultation.</p>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">First Name</label>
                      <Input
                        required
                        type="text"
                        value={formData.firstName}
                        onChange={(e) => handleChange('firstName', e.target.value)}
                        className="bg-white/5 border-white/10 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">Last Name</label>
                      <Input
                        required
                        type="text"
                        value={formData.lastName}
                        onChange={(e) => handleChange('lastName', e.target.value)}
                        className="bg-white/5 border-white/10 text-white"
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">Contact Email</label>
                      <Input
                        required
                        type="email"
                        value={formData.email}
                        onChange={(e) => handleChange('email', e.target.value)}
                        className="bg-white/5 border-white/10 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-semibold text-white/80">Direct Phone Number</label>
                      <Input
                        required
                        type="tel"
                        value={formData.phone}
                        onChange={(e) => handleChange('phone', e.target.value)}
                        className="bg-white/5 border-white/10 text-white"
                      />
                    </div>
                  </div>

                  <div className="pt-4 flex justify-between">
                    <Button type="button" variant="ghost" onClick={() => setStep(3)} className="gap-2 text-white/60 hover:text-white">
                      <ArrowLeft className="h-4 w-4" />
                      <span>Back</span>
                    </Button>
                    <Button type="submit" disabled={isSubmitting || !formData.email} className="gap-2 px-6">
                      {isSubmitting ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span>Auditing Records...</span>
                        </>
                      ) : (
                        <>
                          <span>Calculate Borrowing Power</span>
                          <ArrowRight className="h-4 w-4" />
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              )}
            </motion.div>
          ) : (
            /* SUBMITTED / RESULTS VIEW */
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-card-dark rounded-3xl p-6 md:p-10 border border-white/10 shadow-2xl relative overflow-hidden text-center space-y-8 max-w-2xl mx-auto"
            >
              <div className="absolute top-0 right-0 w-80 h-80 bg-brand-gold-500/10 rounded-full blur-3xl -z-10" />

              <div className="flex justify-center">
                <div className="w-16 h-16 bg-brand-gold-500/10 border border-brand-gold-500/30 rounded-2xl flex items-center justify-center">
                  <CheckCircle className="h-8 w-8 text-brand-gold-400" />
                </div>
              </div>

              <div className="space-y-2">
                <span className="text-[10px] uppercase font-bold tracking-widest text-brand-gold-400">Pre-Audit Computed successfully</span>
                <h2 className="text-2xl md:text-3xl font-bold">Your Borrowing Capacity Profile</h2>
                <p className="text-xs text-white/60">
                  Congratulations {formData.firstName}! We analyzed your credibility markers against current underwriting rules.
                </p>
              </div>

              {/* Core Score & capacity */}
              {evaluation.rejection ? (
                <div className="p-6 bg-rose-500/10 border border-rose-500/20 rounded-2xl space-y-3 text-left">
                  <div className="flex items-center gap-2 text-rose-400 font-bold text-sm">
                    <AlertTriangle className="h-4 w-4 flex-shrink-0" />
                    <span>Rejection Event Identified</span>
                  </div>
                  <p className="text-xs text-white/80 leading-relaxed">
                    {evaluation.rejection}
                  </p>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 gap-4">
                  {/* Score */}
                  <div className="p-6 bg-white/5 border border-white/10 rounded-2xl flex flex-col items-center justify-center">
                    <span className="text-[10px] text-white/40 uppercase font-bold tracking-wider">Credibility Strength</span>
                    <span className="text-4xl font-extrabold font-mono text-brand-gold-400 mt-1">{evaluation.score} <span className="text-xs text-white/40">/100</span></span>
                    <span className="text-[10px] text-emerald-400 font-bold tracking-widest uppercase mt-2 px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full">Passed Pre-check</span>
                  </div>
                  {/* Limit */}
                  <div className="p-6 bg-white/5 border border-white/10 rounded-2xl flex flex-col items-center justify-center">
                    <span className="text-[10px] text-white/40 uppercase font-bold tracking-wider">Estimated Capital Line</span>
                    <span className="text-3xl font-extrabold font-mono text-white mt-1">${evaluation.min.toLocaleString()} - ${evaluation.max.toLocaleString()}</span>
                    <span className="text-[10px] text-white/50 tracking-wide mt-2 font-medium">Unsecured Corporate lines</span>
                  </div>
                </div>
              )}

              {/* Recommendations Checklists */}
              <div className="space-y-3 text-left">
                <h4 className="text-xs font-bold uppercase tracking-widest text-white/40 flex items-center gap-2">
                  <FileSpreadsheet className="h-4 w-4" />
                  <span>Fiduciary Action Checklist</span>
                </h4>
                <div className="space-y-2 pl-2">
                  {evaluation.recs.map((rec, idx) => (
                    <div key={idx} className="flex items-start gap-2.5 text-xs text-white/80">
                      <span className="text-brand-gold-400 font-bold text-xs mt-0.5">▪</span>
                      <span className="leading-relaxed">{rec}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 flex flex-col sm:flex-row gap-4 justify-center">
                <Button asChild size="lg" className="shadow-2xl">
                  <Link href="/contact">
                    Claim My Capital Verification Checklist
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
                {evaluation.score < 50 && (
                  <Button asChild size="lg" variant="outline" className="border-white/10 text-white hover:bg-white/10">
                    <Link href="/business-solutions">View Corporate Setup Packages</Link>
                  </Button>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
