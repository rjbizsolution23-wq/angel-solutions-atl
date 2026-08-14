'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import Link from 'next/link'
import { Briefcase, FileText, TrendingUp, ArrowRight } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

const services = [
  {
    icon: Briefcase,
    title: 'Business Solutions',
    description: 'Complete LLC formation, business branding, virtual office setup, and funding programs to launch your business professionally.',
    href: '/business-solutions',
    features: ['LLC Registration', 'Professional Logo', 'Virtual Office', 'Business Funding'],
    color: 'from-brand-purple-500 to-brand-purple-600',
  },
  {
    icon: FileText,
    title: 'Tax Solutions',
    description: 'Expert tax preparation, IRS compliance, debt resolution, and lien/levy relief for individuals and businesses.',
    href: '/tax-solutions',
    features: ['Tax Preparation', 'Debt Resolution', 'IRS Compliance', 'Lien Relief'],
    color: 'from-brand-gold-500 to-brand-gold-600',
  },
  {
    icon: TrendingUp,
    title: 'Financial Solutions',
    description: 'Credit score optimization, budgeting strategies, debt elimination, and financial education for sustainable growth.',
    href: '/financial-solutions',
    features: ['Credit Repair', 'Budgeting', 'Debt Elimination', 'Financial Education'],
    color: 'from-brand-navy-600 to-brand-navy-700',
  },
]

export function ServicesOverview() {
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
          <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm mb-6">
            <Briefcase className="h-4 w-4 text-brand-gold-500" />
            <span>Our Services</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="text-foreground">Comprehensive Solutions for</span>
            <br />
            <span className="text-gold-gradient">Business Success</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            Three powerful service categories designed to take your business from concept to thriving enterprise.
          </p>
        </motion.div>

        {/* Services Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {services.map((service, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.2 + i * 0.1, duration: 0.6 }}
            >
              <Card className="luxury-card h-full glass-card border-0 overflow-hidden group">
                {/* Gradient header */}
                <div className={`h-2 bg-gradient-to-r ${service.color}`} />
                
                <CardHeader>
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${service.color} flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                    <service.icon className="h-8 w-8 text-white" />
                  </div>
                  <CardTitle className="text-2xl mb-2">{service.title}</CardTitle>
                  <CardDescription className="text-base leading-relaxed">
                    {service.description}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  {/* Features list */}
                  <ul className="space-y-2">
                    {service.features.map((feature, j) => (
                      <li key={j} className="flex items-center gap-2 text-sm">
                        <div className="w-1.5 h-1.5 rounded-full bg-brand-gold-500" />
                        <span className="text-muted-foreground">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  {/* CTA */}
                  <Button asChild variant="ghost" className="w-full group/btn mt-4">
                    <Link href={service.href}>
                      Explore Service
                      <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.6 }}
          className="text-center mt-12"
        >
          <p className="text-muted-foreground mb-4">
            Not sure which service you need?
          </p>
          <Button asChild size="lg" variant="outline">
            <Link href="/contact">
              Schedule Free Consultation
            </Link>
          </Button>
        </motion.div>
      </div>
    </section>
  )
}
