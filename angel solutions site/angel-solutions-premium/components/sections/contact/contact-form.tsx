'use client'

import * as React from 'react'
import { motion } from 'framer-motion'
import { Send } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

export function ContactForm() {
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [submitted, setSubmitted] = React.useState(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Parse UTM parameters safely in client browser
    let utm_source = ''
    let utm_medium = ''
    let utm_campaign = ''

    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search)
      utm_source = params.get('utm_source') || ''
      utm_medium = params.get('utm_medium') || ''
      utm_campaign = params.get('utm_campaign') || ''
    }

    const formEl = e.currentTarget
    const formData = new FormData(formEl)
    const payload = {
      firstName: formData.get('firstName'),
      lastName: formData.get('lastName'),
      email: formData.get('email'),
      phone: formData.get('phone'),
      service: formData.get('service'),
      message: formData.get('message'),
      platform: 'website',
      intake_id: '6a46c0696b95e7dc9dd6251c',
      utm_source,
      utm_medium,
      utm_campaign,
    }

    try {
      const response = await fetch('https://angel-solutions-webhook.rickjefferson.workers.dev/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (response.ok) {
        setSubmitted(true)
        formEl.reset()
      } else {
        const errorData = await response.json()
        alert(`Submission Error: ${errorData.error || 'Failed to submit form.'}`)
      }
    } catch (err) {
      console.error('Contact form submission failed:', err)
      alert('Network Error: Unable to submit form. Please check your internet connection and try again.')
    } finally {
      setIsSubmitting(false)
      // Reset submitted state after 4 seconds
      setTimeout(() => setSubmitted(false), 4000)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Card className="glass-card border-0">
        <CardHeader>
          <CardTitle className="text-3xl">Send Us a Message</CardTitle>
          <CardDescription className="text-base">
            Fill out the form below and we'll get back to you within 24 hours.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name */}
            <div className="grid sm:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label htmlFor="firstName" className="text-sm font-medium">
                  First Name <span className="text-destructive">*</span>
                </label>
                <Input
                  id="firstName"
                  name="firstName"
                  placeholder="John"
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="lastName" className="text-sm font-medium">
                  Last Name <span className="text-destructive">*</span>
                </label>
                <Input
                  id="lastName"
                  name="lastName"
                  placeholder="Doe"
                  required
                />
              </div>
            </div>

            {/* Email & Phone */}
            <div className="grid sm:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">
                  Email <span className="text-destructive">*</span>
                </label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="john@example.com"
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="phone" className="text-sm font-medium">
                  Phone Number
                </label>
                <Input
                  id="phone"
                  name="phone"
                  type="tel"
                  placeholder="(555) 123-4567"
                />
              </div>
            </div>

            {/* Service */}
            <div className="space-y-2">
              <label htmlFor="service" className="text-sm font-medium">
                Service Interest <span className="text-destructive">*</span>
              </label>
              <select
                id="service"
                name="service"
                required
                className="flex h-12 w-full rounded-lg border border-input bg-background px-4 py-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-gold-500 focus-visible:ring-offset-2"
              >
                <option value="">Select a service...</option>
                <option value="business">Business Formation</option>
                <option value="tax">Tax Solutions</option>
                <option value="financial">Financial Solutions</option>
                <option value="consultation">General Consultation</option>
              </select>
            </div>

            {/* Message */}
            <div className="space-y-2">
              <label htmlFor="message" className="text-sm font-medium">
                Message <span className="text-destructive">*</span>
              </label>
              <Textarea
                id="message"
                name="message"
                placeholder="Tell us about your needs and goals..."
                required
                className="min-h-[150px]"
              />
            </div>

            {/* Submit */}
            <Button
              type="submit"
              size="lg"
              className="w-full"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                'Sending...'
              ) : submitted ? (
                '✓ Message Sent!'
              ) : (
                <>
                  Send Message
                  <Send className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>

            <p className="text-xs text-muted-foreground text-center">
              By submitting this form, you agree to our Privacy Policy and Terms of Service.
            </p>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  )
}
