'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { Award, Clock, DollarSign, HeadphonesIcon } from 'lucide-react'

const features = [
  {
    icon: Award,
    title: 'Professional Setup',
    description: 'Complete business infrastructure including LLC, logo, domain, and virtual office.',
  },
  {
    icon: Clock,
    title: 'Fast Turnaround',
    description: 'Your business can be up and running within days, not weeks.',
  },
  {
    icon: DollarSign,
    title: 'Funding Access',
    description: 'Eligible for business funding programs to fuel your growth.',
  },
  {
    icon: HeadphonesIcon,
    title: 'Ongoing Support',
    description: 'Continuous guidance and support as your business scales.',
  },
]

export function BusinessFeaturesSection() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section ref={ref} className="py-24">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="text-center space-y-4"
            >
              <div className="w-16 h-16 mx-auto rounded-xl bg-gradient-to-br from-brand-gold-400 to-brand-gold-600 flex items-center justify-center shadow-lg">
                <feature.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-bold">{feature.title}</h3>
              <p className="text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
