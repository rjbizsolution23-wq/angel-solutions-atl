'use client'

import * as React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sliders, Sparkles, TrendingUp, AlertTriangle, CheckCircle2, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export function CreditSimulator() {
  const [utilization, setUtilization] = React.useState(45)
  const [negativeItems, setNegativeItems] = React.useState(5)
  const [historyDepth, setHistoryDepth] = React.useState(2)

  // FICO Estimation Engine
  const calculateScore = () => {
    // FICO Score Range: 300 - 850 (550 point range)
    let baseScore = 300

    // 1. Payment History (35% of FICO = ~192 max points)
    // Starting with full points, subtract per negative item
    let paymentHistoryPoints = 192
    if (negativeItems > 0) {
      paymentHistoryPoints = Math.max(10, 192 - negativeItems * 25)
    }

    // 2. Credit Utilization (30% of FICO = ~165 max points)
    let utilizationPoints = 0
    if (utilization <= 9) {
      utilizationPoints = 165 // Ideal zone
    } else if (utilization <= 29) {
      utilizationPoints = 145 // Good zone
    } else if (utilization <= 49) {
      utilizationPoints = 95  // Moderate zone
    } else if (utilization <= 89) {
      utilizationPoints = 40  // High utilization
    } else {
      utilizationPoints = 5   // Overlimit / Maxed
    }

    // 3. Length of Credit History (15% of FICO = ~82 max points)
    let historyPoints = 0
    if (historyDepth >= 7) {
      historyPoints = 82
    } else if (historyDepth >= 5) {
      historyPoints = 65
    } else if (historyDepth >= 3) {
      historyPoints = 45
    } else if (historyDepth >= 1) {
      historyPoints = 25
    } else {
      historyPoints = 5
    }

    // 4. Mix & New Credit (20% of FICO = ~111 points) - baseline constant
    const baselinePoints = 111

    const finalScore = Math.round(baseScore + paymentHistoryPoints + utilizationPoints + historyPoints + baselinePoints)
    return Math.min(850, Math.max(300, finalScore))
  }

  const score = calculateScore()

  // Score Tier Label and Styling
  const getScoreDetails = (sc: number) => {
    if (sc >= 740) {
      return {
        label: 'Excellent',
        desc: 'Top-tier rating. Qualifies you for the lowest rates and highest funding limits.',
        colorClass: 'text-emerald-500',
        glowClass: 'shadow-emerald-500/20 border-emerald-500/30',
        bgClass: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
      }
    } else if (sc >= 670) {
      return {
        label: 'Good',
        desc: 'Highly competitive. Highly likely to secure premium credit cards and business lines.',
        colorClass: 'text-brand-gold-500',
        glowClass: 'shadow-brand-gold-500/20 border-brand-gold-500/30',
        bgClass: 'bg-brand-gold-500/10 text-brand-gold-400 border-brand-gold-500/20'
      }
    } else if (sc >= 580) {
      return {
        label: 'Fair',
        desc: 'Sub-prime tier. Some limitations on funding and higher interest rates apply.',
        colorClass: 'text-amber-500',
        glowClass: 'shadow-amber-500/20 border-amber-500/30',
        bgClass: 'bg-amber-500/10 text-amber-400 border-amber-500/20'
      }
    } else {
      return {
        label: 'Poor',
        desc: 'High credit risk. Substantial funding barriers; strategic restoral is highly recommended.',
        colorClass: 'text-rose-500',
        glowClass: 'shadow-rose-500/20 border-rose-500/30',
        bgClass: 'bg-rose-500/10 text-rose-400 border-rose-500/20'
      }
    }
  }

  const scoreDetails = getScoreDetails(score)

  return (
    <div className="glass-card-dark rounded-3xl p-6 md:p-10 border border-white/10 relative overflow-hidden max-w-4xl mx-auto">
      {/* Background Ornaments */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-brand-gold-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />
      <div className="absolute -bottom-10 -left-10 w-80 h-80 bg-brand-purple-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />

      <div className="grid lg:grid-cols-12 gap-8 md:gap-12 items-center">
        {/* Left Side: Sliders */}
        <div className="lg:col-span-7 space-y-8">
          <div className="space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs text-brand-gold-400">
              <Sliders className="h-3.5 w-3.5" />
              <span>Real-Time FICO Simulator</span>
            </div>
            <h3 className="text-2xl md:text-3xl font-bold text-white">
              Simulate Your <span className="text-gold-gradient">Score Trajectory</span>
            </h3>
            <p className="text-sm text-white/60 leading-relaxed">
              Adjust the sliders below to see how optimizing credit utilization, removing negative records, and building payment history depth influence your FICO trajectory under federal consumer law parameters.
            </p>
          </div>

          <div className="space-y-6">
            {/* Slider 1: Credit Card Balances / Utilization */}
            <div className="space-y-2">
              <div className="flex justify-between items-center text-sm">
                <span className="text-white/80 font-medium">Revolving Credit Utilization</span>
                <span className={`font-mono font-bold ${utilization <= 30 ? 'text-emerald-400' : utilization <= 50 ? 'text-brand-gold-400' : 'text-rose-400'}`}>
                  {utilization}%
                </span>
              </div>
              <input
                type="range"
                min="1"
                max="100"
                value={utilization}
                onChange={(e) => setUtilization(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-brand-gold-500 focus:outline-none focus:ring-1 focus:ring-brand-gold-500"
              />
              <div className="flex justify-between text-[10px] text-white/40">
                <span>0% (Ideal)</span>
                <span>30% (Recommended Limit)</span>
                <span>100% (Maxed)</span>
              </div>
            </div>

            {/* Slider 2: Negative/Derogatory Items */}
            <div className="space-y-2">
              <div className="flex justify-between items-center text-sm">
                <span className="text-white/80 font-medium">Inaccurate Negative Records (Collections / Charge-offs)</span>
                <span className={`font-mono font-bold ${negativeItems === 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {negativeItems} {negativeItems === 1 ? 'item' : 'items'}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="15"
                value={negativeItems}
                onChange={(e) => setNegativeItems(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-brand-gold-500 focus:outline-none focus:ring-1 focus:ring-brand-gold-500"
              />
              <div className="flex justify-between text-[10px] text-white/40">
                <span>0 (Clean File)</span>
                <span>5 items</span>
                <span>15 items (Severe)</span>
              </div>
            </div>

            {/* Slider 3: Length of Credit History */}
            <div className="space-y-2">
              <div className="flex justify-between items-center text-sm">
                <span className="text-white/80 font-medium">Depth of Credit History</span>
                <span className="font-mono text-emerald-400 font-bold">
                  {historyDepth} {historyDepth === 1 ? 'year' : 'years'}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="10"
                value={historyDepth}
                onChange={(e) => setHistoryDepth(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-brand-gold-500 focus:outline-none focus:ring-1 focus:ring-brand-gold-500"
              />
              <div className="flex justify-between text-[10px] text-white/40">
                <span>New Credit</span>
                <span>5 years</span>
                <span>10+ years (Prime)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Score Gauge */}
        <div className="lg:col-span-5 flex flex-col items-center text-center">
          <div className={`relative w-56 h-56 rounded-full flex flex-col items-center justify-center border bg-zinc-950/40 backdrop-blur-md transition-all duration-500 shadow-2xl ${scoreDetails.glowClass}`}>
            
            {/* Pulsing Outer Ring */}
            <div className="absolute inset-0 rounded-full border border-white/5 animate-pulse" />
            
            <span className="text-[10px] uppercase tracking-widest text-white/40 font-bold">Estimated FICO</span>
            
            <AnimatePresence mode="wait">
              <motion.span
                key={score}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                className="text-5xl md:text-6xl font-black font-mono tracking-tighter text-white mt-1"
              >
                {score}
              </motion.span>
            </AnimatePresence>

            <span className={`text-sm font-bold uppercase tracking-wider mt-2 px-3 py-0.5 rounded-full border ${scoreDetails.bgClass}`}>
              {scoreDetails.label}
            </span>
          </div>

          <div className="mt-6 space-y-4 max-w-sm">
            <p className="text-xs text-white/70 leading-relaxed">
              {scoreDetails.desc}
            </p>

            {negativeItems > 0 && (
              <div className="flex items-center gap-2 justify-center text-[10px] bg-rose-500/10 border border-rose-500/20 text-rose-400 p-2 rounded-lg">
                <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0" />
                <span className="text-left font-medium">Removing {negativeItems} negative accounts could restore up to {negativeItems * 25} points!</span>
              </div>
            )}

            {utilization > 30 && (
              <div className="flex items-center gap-2 justify-center text-[10px] bg-amber-500/10 border border-amber-500/20 text-amber-400 p-2 rounded-lg">
                <TrendingUp className="h-3.5 w-3.5 flex-shrink-0" />
                <span className="text-left font-medium">Paying card utilization from {utilization}% below 30% will instantly trigger a major score jump.</span>
              </div>
            )}

            <Button asChild className="w-full shadow-lg text-xs" size="lg">
              <Link href="/contact">
                Dispute Negative Records Now
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
