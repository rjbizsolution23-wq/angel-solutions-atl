'use client'

import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import Image from 'next/image'
import Link from 'next/link'
import { ArrowRight, Award, Users, Target } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function AboutPreview() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section ref={ref} className="py-24 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/2 left-0 w-96 h-96 bg-brand-purple-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-brand-gold-500/10 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Image Side */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6 }}
            className="relative"
          >
            <div className="relative aspect-square rounded-3xl overflow-hidden glass-card p-2">
              <div className="relative w-full h-full rounded-2xl overflow-hidden">
                <Image
                  src="/assets/founder/founder-2446f0_6bd22d41670a4ac09cd47437899274b0.jpg"
                  alt="Jordynn Miller, Founder & CEO of Angel Solutions ATL"
                  fill
                  className="object-cover object-center"
                />
                <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent p-6 text-white pt-20">
                  <p className="text-xl font-bold">Jordynn Miller</p>
                  <p className="text-sm text-brand-gold-300">Founder & CEO</p>
                </div>
              </div>
            </div>

            {/* Floating badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={inView ? { opacity: 1, scale: 1 } : {}}
              transition={{ delay: 0.3 }}
              className="absolute -top-6 -right-6 glass-card rounded-2xl p-6 shadow-xl"
            >
              <Award className="h-12 w-12 text-brand-gold-500 mb-2" />
              <p className="text-2xl font-bold">5+</p>
              <p className="text-sm text-muted-foreground">Years Excellence</p>
            </motion.div>
          </motion.div>

          {/* Content Side */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div className="inline-flex items-center gap-2 glass-card px-4 py-2 rounded-full text-sm">
              <Target className="h-4 w-4 text-brand-gold-500" />
              <span>About Us</span>
            </div>

            <h2 className="text-4xl md:text-5xl font-bold leading-tight">
              <span className="text-foreground">Empowering Your</span>
              <br />
              <span className="text-gold-gradient">Business Growth</span>
            </h2>

            <p className="text-lg text-muted-foreground leading-relaxed">
              Founded by Jordynn Miller, Angel Solutions ATL has been transforming businesses across Atlanta for over 5 years. We provide comprehensive solutions that help business owners expand operations, enhance cash flow, identify opportunities, and scale on an accelerated timeline.
            </p>

            <div className="grid sm:grid-cols-2 gap-4 pt-4">
              {[
                { icon: Users, label: 'Expert Team', desc: 'Seasoned professionals' },
                { icon: Target, label: 'Proven Results', desc: '500+ success stories' },
                { icon: Award, label: 'Quality Service', desc: '98% satisfaction' },
                { icon: ArrowRight, label: 'Fast Growth', desc: 'Accelerated scaling' },
              ].map((item, i) => (
                <div key={i} className="flex gap-4 items-start">
                  <div className="w-12 h-12 rounded-xl bg-brand-gold-50 dark:bg-brand-gold-950/20 flex items-center justify-center flex-shrink-0">
                    <item.icon className="h-6 w-6 text-brand-gold-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">{item.label}</h4>
                    <p className="text-sm text-muted-foreground">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-4 pt-4">
              <Button asChild size="lg">
                <Link href="/about">
                  Learn More About Us
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/contact">
                  Schedule Consultation
                </Link>
              </Button>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
