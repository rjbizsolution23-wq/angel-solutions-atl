'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { STATS } from '@/lib/constants'
import { Shield, Sparkles, TrendingUp, Award } from 'lucide-react'

const icons = [TrendingUp, Shield, Award, Sparkles]

export function StatsSection() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section ref={ref} className="py-12 relative overflow-hidden bg-background">
      {/* Background radial accent */}
      <div className="absolute inset-0 -z-10 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-brand-gold-500/5 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 max-w-6xl">
        <div className="glass-card-dark rounded-3xl p-8 md:p-10 border border-white/5 shadow-2xl relative overflow-hidden">
          {/* subtle decorative diagonal line */}
          <div className="absolute inset-0 bg-gradient-to-tr from-brand-gold-500/5 via-transparent to-brand-purple-500/5 opacity-50" />
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-4 relative z-10 divide-y md:divide-y-0 md:divide-x divide-white/5">
            {STATS.map((stat, i) => {
              const StatIcon = icons[i % icons.length]
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={inView ? { opacity: 1, y: 0 } : {}}
                  transition={{ delay: i * 0.1, duration: 0.6 }}
                  className="text-center space-y-3 pt-6 md:pt-0 md:px-6 first:pt-0"
                >
                  <div className="mx-auto w-10 h-10 rounded-xl bg-gradient-to-br from-brand-gold-400/10 to-brand-gold-600/10 border border-brand-gold-500/20 flex items-center justify-center text-brand-gold-400 mb-1">
                    <StatIcon className="h-5 w-5" />
                  </div>
                  <div className="text-4xl md:text-5xl lg:text-6xl font-black font-mono tracking-tight text-gold-gradient">
                    {stat.value}
                  </div>
                  <div className="text-xs lg:text-sm text-white/70 font-semibold uppercase tracking-wider">
                    {stat.label}
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}

