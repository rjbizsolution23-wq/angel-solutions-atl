'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Zap, Shield, HeartHandshake, Clock, Award, Users } from 'lucide-react'

const features = [
  {
    icon: Zap,
    title: 'Fast Turnaround',
    description: 'Get your business up and running quickly with our streamlined processes.',
  },
  {
    icon: Shield,
    title: 'Secure & Compliant',
    description: 'Full compliance with IRS and state regulations. Your data is protected.',
  },
  {
    icon: HeartHandshake,
    title: 'Personalized Service',
    description: 'Dedicated support tailored to your unique business needs and goals.',
  },
  {
    icon: Clock,
    title: '24/7 Support',
    description: 'Access to our expert team whenever you need guidance or assistance.',
  },
  {
    icon: Award,
    title: 'Proven Results',
    description: '500+ successful business launches and 98% client satisfaction rate.',
  },
  {
    icon: Users,
    title: 'Expert Team',
    description: 'Years of combined experience in business, tax, and financial services.',
  },
]

export function FeaturesSection() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section ref={ref} className="py-24 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-background via-muted/30 to-background" />

      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="text-foreground">Why Choose</span>
            <br />
            <span className="text-gold-gradient">Angel Solutions ATL</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            We're committed to delivering exceptional service and results that exceed expectations.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.1 + i * 0.1, duration: 0.5 }}
              className="group"
            >
              <div className="glass-card rounded-2xl p-8 h-full hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-brand-gold-400 to-brand-gold-600 flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <feature.icon className="h-7 w-7 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
