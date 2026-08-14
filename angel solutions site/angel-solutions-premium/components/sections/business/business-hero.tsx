'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, Building2, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function BusinessHero() {
  return (
    <section className="relative min-h-[70vh] flex items-center justify-center overflow-hidden pt-32 pb-20">
      {/* Background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-purple-900 via-brand-navy-900 to-brand-navy-800" />
        <div className="absolute inset-0 grid-bg opacity-20" />
      </div>

      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm"
          >
            <Building2 className="h-4 w-4 text-brand-gold-400" />
            <span className="text-white/90">Professional Business Formation</span>
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight"
          >
            <span className="text-white">Launch Your Business</span>
            <br />
            <span className="text-gold-gradient">Professionally</span>
          </motion.h1>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl text-white/80 leading-relaxed max-w-3xl mx-auto"
          >
            Complete business formation packages from $450. LLC registration, professional branding, virtual office setup, and optional business funding programs.
          </motion.p>

          {/* Key benefits */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-wrap justify-center gap-6 text-white/90"
          >
            {['LLC Formation', 'Professional Logo', 'Virtual Office', 'Business Funding'].map((item, i) => (
              <div key={i} className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-brand-gold-400" />
                <span>{item}</span>
              </div>
            ))}
          </motion.div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex flex-col sm:flex-row gap-4 justify-center pt-4"
          >
            <Button asChild size="xl" className="shadow-2xl">
              <Link href="#packages">
                View Packages
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild size="xl" variant="outline" className="border-white/20 text-white hover:bg-white/10">
              <Link href="/contact">
                Schedule Consultation
              </Link>
            </Button>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
