'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Shield, Sparkles, Building, CreditCard, ChevronRight, CheckCircle2, Terminal } from 'lucide-react'

export function HeroInteractiveDashboard() {
  const [activeTab, setActiveTab] = useState<'tracker' | 'credit' | 'api'>('tracker')
  const [creditScore, setCreditScore] = useState(35)
  const [isBuildingCredit, setIsBuildingCredit] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)

  // API Feed Simulation
  const [logs, setLogs] = useState<string[]>([
    'GET /api/contact - 200 OK (3.4ms)',
    'DB - lead_state set to NEW',
    'GHL Sync - Contact created with Location Sfvt5kBZ3EUO'
  ])

  // Automatically cycle timeline steps
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % 4)
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  // Simulate Credit score builder
  useEffect(() => {
    if (!isBuildingCredit) return
    const timer = setInterval(() => {
      setCreditScore((prev) => {
        if (prev >= 85) {
          setIsBuildingCredit(false)
          return 85
        }
        return prev + 1
      })
    }, 40)
    return () => clearInterval(timer)
  }, [isBuildingCredit])

  const triggerCreditBuild = () => {
    setCreditScore(35)
    setIsBuildingCredit(true)
  }

  const steps = [
    { label: 'LLC Filing & Registration', desc: 'Articles of Organization submitted to State', icon: Building },
    { label: 'EIN & Professional Virtual Office', desc: 'Secure real commercial address & IRS tax ID', icon: Shield },
    { label: 'D&B Registration (D-U-N-S)', desc: 'Dun & Bradstreet business file initialized', icon: Sparkles },
    { label: 'Corporate Trade Lines Active', desc: 'Net-30 reporting active to Experian & Equifax', icon: CreditCard }
  ]

  return (
    <div className="relative glass-card-dark rounded-3xl p-6 md:p-8 shadow-2xl border border-white/10 bg-zinc-950/80 backdrop-blur-xl">
      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-white/5 pb-4">
        {[
          { id: 'tracker', label: 'Launch Tracker' },
          { id: 'credit', label: 'Credit Visualizer' },
          { id: 'api', label: 'API Telemetry' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all ${
              activeTab === tab.id
                ? 'bg-brand-gold-500 text-brand-navy-950 shadow-lg shadow-brand-gold-500/20'
                : 'text-white/60 hover:text-white hover:bg-white/5'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      <div className="min-h-[280px] flex flex-col justify-between">
        
          {activeTab === 'tracker' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h4 className="text-sm font-bold text-white tracking-wide uppercase">Elite Corporate Onboarding</h4>
                <span className="text-[10px] font-semibold text-brand-gold-400 bg-brand-gold-500/10 px-2 py-0.5 rounded-full uppercase tracking-wider">
                  Live Flow
                </span>
              </div>

              <div className="space-y-3">
                {steps.map((step, idx) => {
                  const Icon = step.icon
                  const isActive = idx === currentStep
                  const isCompleted = idx < currentStep

                  return (
                    <div
                      key={idx}
                      className={`flex gap-4 p-3 rounded-2xl transition-all duration-300 border ${
                        isActive
                          ? 'bg-gradient-to-r from-brand-purple-900/40 to-brand-navy-900/40 border-brand-purple-500/30 shadow-lg'
                          : 'bg-transparent border-transparent'
                      }`}
                    >
                      <div className="flex flex-col items-center">
                        <div
                          className={`w-8 h-8 rounded-full flex items-center justify-center border transition-all ${
                            isActive
                              ? 'bg-brand-purple-500 border-brand-purple-400 text-white shadow-md shadow-brand-purple-500/30 scale-110'
                              : isCompleted
                              ? 'bg-brand-gold-500/20 border-brand-gold-500/40 text-brand-gold-400'
                              : 'bg-white/5 border-white/10 text-white/40'
                          }`}
                        >
                          {isCompleted ? <CheckCircle2 className="h-4 w-4" /> : <Icon className="h-4 w-4" />}
                        </div>
                        {idx < steps.length - 1 && (
                          <div
                            className={`w-0.5 h-6 my-1 transition-all ${
                              isCompleted ? 'bg-brand-gold-500/40' : 'bg-white/10'
                            }`}
                          />
                        )}
                      </div>

                      <div className="space-y-0.5">
                        <h5
                          className={`text-xs font-bold transition-colors ${
                            isActive ? 'text-white' : isCompleted ? 'text-white/80' : 'text-white/40'
                          }`}
                        >
                          {step.label}
                        </h5>
                        <p
                          className={`text-[10px] leading-relaxed transition-colors ${
                            isActive ? 'text-white/70' : 'text-white/40'
                          }`}
                        >
                          {step.desc}
                        </p>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {activeTab === 'credit' && (
            <div className="space-y-6 text-center py-4">
              <h4 className="text-sm font-bold text-white text-left tracking-wide uppercase">Corporate PAYDEX & Credit Engine</h4>

              <div className="flex flex-col items-center justify-center space-y-4">
                {/* Radial Gauge */}
                <div className="relative w-40 h-40 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle
                      cx="80"
                      cy="80"
                      r="65"
                      className="stroke-white/5"
                      strokeWidth="10"
                      fill="transparent"
                    />
                    <circle
                      cx="80"
                      cy="80"
                      r="65"
                      className="stroke-brand-gold-500"
                      strokeWidth="10"
                      fill="transparent"
                      strokeDasharray="408.4"
                      strokeDashoffset={408.4 - (408.4 * creditScore) / 100}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-extrabold text-white tracking-tight">{creditScore}</span>
                    <span className="text-[10px] uppercase font-bold tracking-wider text-white/50">D&B Score</span>
                  </div>
                </div>

                <div className="space-y-2 max-w-xs mx-auto">
                  <p className="text-xs text-white/70 leading-relaxed">
                    {creditScore < 50
                      ? 'No files detected. Limited vendor trading relationships.'
                      : creditScore < 75
                      ? 'Standard profile active. High financing eligibility.'
                      : 'Elite PAYDEX Level. Qualified for no-PG business credit lines.'}
                  </p>
                  <button
                    onClick={triggerCreditBuild}
                    disabled={isBuildingCredit}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-brand-gold-500 to-brand-gold-600 text-brand-navy-950 hover:opacity-90 active:scale-95 transition-all shadow-lg disabled:opacity-50"
                  >
                    {isBuildingCredit ? 'Injecting Trade Lines...' : 'Simulate Funding Builder'}
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'api' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h4 className="text-sm font-bold text-white tracking-wide uppercase flex items-center gap-2">
                  <Terminal className="h-4 w-4 text-brand-purple-400" />
                  Edge Webhook Stream
                </h4>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
                  <span className="text-[9px] font-bold text-emerald-400 uppercase tracking-wider">Active</span>
                </div>
              </div>

              <div className="font-mono text-[11px] bg-black/40 rounded-2xl p-4 border border-white/5 h-44 overflow-y-auto space-y-2.5 leading-relaxed text-zinc-300">
                {logs.map((log, idx) => (
                  <div key={idx} className="flex gap-2 items-start">
                    <span className="text-brand-gold-500 select-none">&gt;</span>
                    <span>{log}</span>
                  </div>
                ))}
              </div>

              <p className="text-[10px] text-white/40 leading-relaxed">
                Fully mapped to your live Cloudflare D1 SQLite database storage and GoHighLevel CRM instance.
              </p>
            </div>
          )}
        
      </div>

      {/* Background glow highlights */}
      <div className="absolute -top-10 -left-10 w-24 h-24 rounded-full bg-brand-gold-500/10 blur-2xl pointer-events-none" />
      <div className="absolute -bottom-10 -right-10 w-24 h-24 rounded-full bg-brand-purple-500/10 blur-2xl pointer-events-none" />
    </div>
  )
}
