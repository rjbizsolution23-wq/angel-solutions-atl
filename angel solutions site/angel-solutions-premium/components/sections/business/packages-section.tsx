'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import Link from 'next/link'
import { Check, Star, ArrowRight } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BUSINESS_PACKAGES } from '@/lib/constants'
import { formatCurrency } from '@/lib/utils'

export function PackagesSection() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section id="packages" ref={ref} className="py-24 bg-background">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="text-foreground">Choose Your</span>
            <br />
            <span className="text-gold-gradient">Business Package</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            All-inclusive packages designed to launch your business professionally from day one.
          </p>
        </motion.div>

        {/* Packages Grid */}
        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {BUSINESS_PACKAGES.map((pkg, i) => (
            <motion.div
              key={pkg.id}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.1 + i * 0.1, duration: 0.6 }}
              className="relative"
            >
              {/* Popular badge */}
              {pkg.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 z-10">
                  <div className="glass-card px-4 py-1.5 rounded-full flex items-center gap-2 shadow-lg">
                    <Star className="h-4 w-4 text-brand-gold-500 fill-brand-gold-500" />
                    <span className="text-sm font-semibold">Most Popular</span>
                  </div>
                </div>
              )}

              <Card className={`luxury-card h-full ${pkg.popular ? 'border-brand-gold-500/50 shadow-xl scale-105' : ''}`}>
                {/* Header */}
                <CardHeader className="text-center pb-8">
                  <CardTitle className="text-2xl mb-2">{pkg.name}</CardTitle>
                  <div className="mb-4">
                    <div className="text-5xl font-bold text-brand-gold-600">
                      {formatCurrency(pkg.price)}
                    </div>
                    <div className="text-sm text-muted-foreground mt-2">One-time setup fee</div>
                  </div>
                  <CardDescription className="text-base">
                    + {formatCurrency(pkg.virtualOfficeFee)}/{pkg.virtualOfficeInterval} virtual office
                  </CardDescription>
                </CardHeader>

                {/* Features */}
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    {pkg.features.map((feature, j) => (
                      <div key={j} className="flex items-start gap-3">
                        <div className="w-5 h-5 rounded-full bg-brand-gold-50 dark:bg-brand-gold-950/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <Check className="h-3 w-3 text-brand-gold-600" />
                        </div>
                        <span className="text-sm text-muted-foreground leading-relaxed">
                          {feature}
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>

                {/* CTA */}
                <CardFooter className="pt-0">
                  <Button asChild className="w-full" size="lg" variant={pkg.popular ? 'default' : 'outline'}>
                    <Link href="/contact">
                      Get Started
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </CardFooter>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Additional info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.5 }}
          className="text-center mt-16 space-y-4"
        >
          <p className="text-muted-foreground">
            💳 Flexible payment options available: PayPal, Sezzle, Zip, AfterPay, and Affirm
          </p>
          <p className="text-sm text-muted-foreground">
            All packages include business funding program eligibility
          </p>
        </motion.div>
      </div>
    </section>
  )
}
