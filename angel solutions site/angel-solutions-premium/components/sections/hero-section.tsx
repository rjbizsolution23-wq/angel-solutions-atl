'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, Sparkles, TrendingUp, Shield } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { InteractiveParticles } from '@/components/visuals/interactive-particles'
import { HeroInteractiveDashboard } from '@/components/visuals/hero-interactive-dashboard'

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-navy-900 via-brand-purple-900/90 to-brand-navy-800" />
        <div className="absolute inset-0 bg-grid-pattern opacity-10" />
        <InteractiveParticles />
        <div className="absolute top-1/4 -left-48 w-96 h-96 bg-brand-gold-500/20 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-1/4 -right-48 w-96 h-96 bg-brand-purple-500/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
      </div>

      <div className="container mx-auto px-4 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm"
            >
              <Sparkles className="h-4 w-4 text-brand-gold-400" />
              <span className="text-white/90">Elite Business Solutions</span>
              <div className="w-2 h-2 rounded-full bg-brand-gold-400 animate-pulse" />
            </motion.div>

            {/* Main Headline */}
            <div className="space-y-4">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight"
              >
                <span className="text-white">Transform Your</span>
                <br />
                <span className="text-gold-gradient">Business Vision</span>
                <br />
                <span className="text-white">Into Reality</span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="text-xl text-white/80 leading-relaxed max-w-2xl"
              >
                Expert business formation, tax resolution, and financial solutions designed to accelerate your success. Join 500+ thriving businesses across Atlanta.
              </motion.p>
            </div>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-4"
            >
              <Button asChild size="xl" className="group shadow-2xl">
                <Link href="/contact">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Link>
              </Button>
              <Button asChild size="xl" variant="outline" className="border-white/20 text-white hover:bg-white/10">
                <Link href="/about">
                  Learn More
                </Link>
              </Button>
            </motion.div>

            {/* Trust indicators */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="flex flex-wrap items-center gap-8 pt-8"
            >
              {[
                { icon: TrendingUp, label: '500+ Businesses', color: 'text-brand-gold-400' },
                { icon: Shield, label: '98% Satisfaction', color: 'text-brand-purple-400' },
                { icon: Sparkles, label: '5+ Years', color: 'text-brand-gold-400' },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full glass-card flex items-center justify-center">
                    <item.icon className={`h-5 w-5 ${item.color}`} />
                  </div>
                  <span className="text-sm font-medium text-white/90">{item.label}</span>
                </div>
              ))}
            </motion.div>
          </motion.div>

          {/* Hero Image / Visual */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative lg:pl-4"
          >
            <HeroInteractiveDashboard />
          </motion.div>

        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex items-start justify-center p-2">
          <motion.div
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="w-1.5 h-1.5 bg-brand-gold-400 rounded-full"
          />
        </div>
      </motion.div>
    </section>
  )
}
