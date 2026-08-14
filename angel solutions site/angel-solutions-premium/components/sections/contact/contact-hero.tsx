'use client'

import { motion } from 'framer-motion'
import { MessageSquare } from 'lucide-react'

export function ContactHero() {
  return (
    <section className="relative min-h-[50vh] flex items-center justify-center overflow-hidden pt-32 pb-20">
      {/* Background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-purple-900 via-brand-navy-900 to-brand-navy-800" />
        <div className="absolute inset-0 grid-bg opacity-20" />
      </div>

      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm"
          >
            <MessageSquare className="h-4 w-4 text-brand-gold-400" />
            <span className="text-white/90">Get In Touch</span>
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl md:text-6xl font-bold leading-tight"
          >
            <span className="text-white">Let's Build Your</span>
            <br />
            <span className="text-gold-gradient">Success Together</span>
          </motion.h1>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-xl text-white/80 leading-relaxed"
          >
            Schedule your free discovery call and discover how we can transform your business.
          </motion.p>
        </div>
      </div>
    </section>
  )
}
