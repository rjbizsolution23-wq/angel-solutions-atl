'use client'

import * as React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mail, Calendar, Sparkles } from 'lucide-react'
import { ContactForm } from './contact-form'
import { SITE_CONFIG } from '@/lib/constants'

export function ContactContainer() {
  const [activeTab, setActiveTab] = React.useState<'enquiry' | 'booking'>('enquiry')

  return (
    <div className="space-y-8">
      {/* Tab Switcher */}
      <div className="flex p-1 bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl max-w-md mx-auto relative z-10 backdrop-blur-md">
        <button
          onClick={() => setActiveTab('enquiry')}
          className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-lg text-sm font-semibold transition-all relative ${activeTab === 'enquiry' ? 'text-brand-gold-700 dark:text-brand-gold-400' : 'text-zinc-500 hover:text-zinc-800 dark:text-white/60 dark:hover:text-white'}`}
        >
          {activeTab === 'enquiry' && (
            <motion.div
              layoutId="active-contact-tab"
              className="absolute inset-0 bg-white dark:bg-brand-gold-500/20 border border-zinc-200 dark:border-brand-gold-500/30 shadow-sm rounded-lg -z-10"
              transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            />
          )}
          <Mail className="h-4 w-4" />
          <span>Quick Enquiry</span>
        </button>
        <button
          onClick={() => setActiveTab('booking')}
          className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-lg text-sm font-semibold transition-all relative ${activeTab === 'booking' ? 'text-brand-gold-700 dark:text-brand-gold-400' : 'text-zinc-500 hover:text-zinc-800 dark:text-white/60 dark:hover:text-white'}`}
        >
          {activeTab === 'booking' && (
            <motion.div
              layoutId="active-contact-tab"
              className="absolute inset-0 bg-white dark:bg-brand-gold-500/20 border border-zinc-200 dark:border-brand-gold-500/30 shadow-sm rounded-lg -z-10"
              transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            />
          )}
          <Calendar className="h-4 w-4" />
          <span>Schedule Call</span>
        </button>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === 'enquiry' ? (
          <motion.div
            key="enquiry-form"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.3 }}
          >
            <ContactForm />
          </motion.div>
        ) : (
          <motion.div
            key="calendar-booking"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.3 }}
            className="glass-card-dark rounded-3xl p-4 md:p-8 border border-white/10 overflow-hidden relative"
          >
            <div className="absolute top-0 right-0 w-64 h-64 bg-brand-gold-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />
            <div className="space-y-4 mb-6">
              <h3 className="text-xl md:text-2xl font-bold text-white flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-brand-gold-400" />
                <span>Book Your <span className="text-gold-gradient">Strategy Session</span></span>
              </h3>
              <p className="text-xs md:text-sm text-white/60">
                Select an available slot below to secure your direct legal restoral or business credit structuring call with Jordynn Miller and our elite advisory team.
              </p>
            </div>
            
            <div className="w-full h-[650px] rounded-2xl bg-zinc-950/40 border border-white/5 overflow-hidden shadow-2xl relative">
              <iframe
                src={SITE_CONFIG.bookingLink}
                className="w-full h-full border-none"
                allow="camera; microphone; geolocation; autoplay"
                title="Angel Solutions ATL Booking Calendar"
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
