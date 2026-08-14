'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { FileCheck, Building, Sparkles, Rocket } from 'lucide-react'

const steps = [
  {
    icon: FileCheck,
    title: 'Choose Your Package',
    description: 'Select the business formation package that best fits your needs and goals.',
  },
  {
    icon: Building,
    title: 'Submit Information',
    description: 'Provide your business details and we\'ll handle all the paperwork and filings.',
  },
  {
    icon: Sparkles,
    title: 'We Build Your Brand',
    description: 'Receive your professional logo, domain, email, and virtual office setup.',
  },
  {
    icon: Rocket,
    title: 'Launch & Grow',
    description: 'Your business is ready! Access funding programs and ongoing support.',
  },
]

export function ProcessSection() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section ref={ref} className="py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="text-foreground">Simple</span>{' '}
            <span className="text-gold-gradient">4-Step Process</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            From concept to launch in just a few simple steps. We handle everything.
          </p>
        </motion.div>

        {/* Process Steps */}
        <div className="grid md:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {steps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.1 + i * 0.1, duration: 0.6 }}
              className="relative"
            >
              {/* Connector line */}
              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 left-full w-full h-px bg-gradient-to-r from-brand-gold-500/50 to-transparent -z-10" />
              )}

              <div className="text-center space-y-4">
                {/* Icon */}
                <div className="w-24 h-24 mx-auto rounded-2xl bg-gradient-to-br from-brand-gold-400 to-brand-gold-600 flex items-center justify-center shadow-xl">
                  <step.icon className="h-12 w-12 text-white" />
                </div>

                {/* Step number */}
                <div className="text-sm font-bold text-brand-gold-600">
                  STEP {i + 1}
                </div>

                {/* Title */}
                <h3 className="text-xl font-bold">{step.title}</h3>

                {/* Description */}
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
