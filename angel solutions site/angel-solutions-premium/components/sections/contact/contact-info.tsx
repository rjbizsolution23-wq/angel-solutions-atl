'use client'

import { motion } from 'framer-motion'
import { Mail, Phone, MapPin, Clock } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { SITE_CONFIG } from '@/lib/constants'

const contactMethods = [
  {
    icon: Mail,
    label: 'Email',
    value: SITE_CONFIG.email,
    href: `mailto:${SITE_CONFIG.email}`,
  },
  {
    icon: Phone,
    label: 'Phone',
    value: SITE_CONFIG.phone,
    href: `tel:${SITE_CONFIG.phone}`,
  },
  {
    icon: MapPin,
    label: 'Location',
    value: `${SITE_CONFIG.address.city}, ${SITE_CONFIG.address.state}`,
    href: '#',
  },
  {
    icon: Clock,
    label: 'Business Hours',
    value: 'Mon-Fri: 9AM-6PM EST',
    href: '#',
  },
]

export function ContactInfo() {
  return (
    <div className="space-y-8">
      {/* Contact Methods */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <Card className="glass-card border-0">
          <CardContent className="pt-6 space-y-6">
            <div>
              <h3 className="text-2xl font-bold mb-2">Contact Information</h3>
              <p className="text-muted-foreground">
                Reach out to us through any of these channels.
              </p>
            </div>

            <div className="space-y-4">
              {contactMethods.map((method, i) => (
                <a
                  key={i}
                  href={method.href}
                  className="flex items-start gap-4 p-4 rounded-lg hover:bg-accent transition-colors group"
                >
                  <div className="w-12 h-12 rounded-xl bg-brand-gold-50 dark:bg-brand-gold-950/20 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                    <method.icon className="h-6 w-6 text-brand-gold-600" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-muted-foreground mb-1">
                      {method.label}
                    </div>
                    <div className="font-semibold">{method.value}</div>
                  </div>
                </a>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Response */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
      >
        <Card className="glass-card border-0 bg-gradient-to-br from-brand-gold-500 to-brand-gold-600 text-white">
          <CardContent className="pt-6">
            <h4 className="text-xl font-bold mb-3">Quick Response Guarantee</h4>
            <p className="text-white/90 leading-relaxed">
              We typically respond to all inquiries within 24 hours. For urgent matters, please call us directly.
            </p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Additional Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="glass-card rounded-2xl p-6 space-y-4"
      >
        <h4 className="font-bold">What to Expect</h4>
        <ul className="space-y-2 text-sm text-muted-foreground">
          <li className="flex items-start gap-2">
            <span className="text-brand-gold-500 mt-1">✓</span>
            <span>Free initial consultation</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-brand-gold-500 mt-1">✓</span>
            <span>Personalized service recommendations</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-brand-gold-500 mt-1">✓</span>
            <span>Transparent pricing and timeline</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-brand-gold-500 mt-1">✓</span>
            <span>No obligation to proceed</span>
          </li>
        </ul>
      </motion.div>
    </div>
  )
}
