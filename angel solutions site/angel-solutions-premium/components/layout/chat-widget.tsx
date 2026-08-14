'use client'

import * as React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageSquare, Send, X, Sparkles, User, Calendar, ArrowRight, Loader2, CheckCircle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { SITE_CONFIG } from '@/lib/constants'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isQuickOption?: boolean
}

export function ChatWidget() {
  const [isOpen, setIsOpen] = React.useState(false)
  const [messages, setMessages] = React.useState<Message[]>([])
  const [inputValue, setInputValue] = React.useState('')
  const [isTyping, setIsTyping] = React.useState(false)
  const [hasPromptedDetails, setHasPromptedDetails] = React.useState(false)
  
  // Lead Intake Form state (inside chat widget)
  const [showIntakeForm, setShowIntakeForm] = React.useState(false)
  const [formData, setFormData] = React.useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    service: 'credit_repair'
  })
  const [formSubmitted, setFormSubmitted] = React.useState(false)
  const [formLoading, setFormSubmittedLoading] = React.useState(false)

  const messagesEndRef = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    // Scroll to bottom on new messages
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  // Initial welcome trigger
  React.useEffect(() => {
    if (isOpen && messages.length === 0) {
      setIsTyping(true)
      const timer = setTimeout(() => {
        setIsTyping(false)
        setMessages([
          {
            id: 'welcome',
            role: 'assistant',
            content: `Hey! Jordynn Miller here, founder of Angel Solutions ATL. 🌟 Welcome!\n\nI'm so excited to connect and help you clear the credit and financial roadblocks holding you back.\n\nTo get started, which of our premium solutions can I assist you with today?`,
            timestamp: new Date()
          }
        ])
      }, 1200)
      return () => clearTimeout(timer)
    }
  }, [isOpen, messages.length])

  const quickOptions = [
    { label: 'Credit Restoral 💳', value: 'credit_restoral' },
    { label: 'Business Funding & Trade Lines 🚀', value: 'business_funding' },
    { label: 'Tax Settle & Resolution 💼', value: 'tax_resolve' },
    { label: 'DIY Skool Plan ($67/mo) 💻', value: 'skool_diy' },
    { label: 'Book 1-on-1 Consultation ($795) 📅', value: 'book_consult' }
  ]

  const handleQuickOptionClick = async (label: string, value: string) => {
    // Add user selection as message
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: label,
      timestamp: new Date(),
      isQuickOption: true
    }
    setMessages((prev) => [...prev, userMsg])
    
    setIsTyping(true)
    await new Promise((resolve) => setTimeout(resolve, 1500))
    setIsTyping(false)

    let reply = ''
    if (value === 'credit_restoral') {
      reply = `My Credit Restoral programs are designed to dispute up to 5 negative inaccuracies monthly (or all at once under our 1-on-1 Premium Restoral tier). We clear collections, late payments, bankruptcies, and repossessions by auditing every line under the Fair Credit Reporting Act (FCRA). 💳\n\nWould you like to pre-qualify and speak with one of my consultants? Click the booking link below or let's get your details mapped out right in this chat!`
    } else if (value === 'business_funding') {
      reply = `To qualify for up to $150k in unsecured corporate business funding, we focus on establishing a clean LLC, building an active PAYDEX business credit score of 80+ via vendor trade lines, and optimizing personal profiles. 🚀\n\nI would love to help you build out your corporate profile. You can schedule a strategy session or drop your details here!`
    } else if (value === 'tax_resolve') {
      reply = `Tax debt can feel incredibly heavy, but our team specializes in IRS Offer in Compromise (OIC) representations, setting up compliant installment agreements, and lifting tax liens/levies. 💼\n\nLet's get our tax legal team to look over your file. Schedule directly on my line or let's map your intake in this chat!`
    } else if (value === 'skool_diy') {
      reply = `Awesome! My Credit Solution Skool Community is our highly popular DIY option. For only **$67/mo**, you get 5 customized dispute letters drafted monthly and direct support inside our coaching community! 💻\n\nSign up instantly and start your disputes today: https://www.skool.com/creditsolution/about`
    } else if (value === 'book_consult') {
      reply = `Let's lock in your victory roadmap! Our premium 1-on-1 Strategy call starts at **$795** for legal audit, report analysis, and full restoral services.\n\nBook your strategy session on my official calendar here: https://angelsolutionsatl.com/book-online 📅`
    }

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: reply,
        timestamp: new Date()
      }
    ])

    // Prompt contact intake form after showing info
    if (value !== 'skool_diy' && value !== 'book_consult') {
      setIsTyping(true)
      await new Promise((resolve) => setTimeout(resolve, 1200))
      setIsTyping(false)
      setShowIntakeForm(true)
    }
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const userText = inputValue
    setInputValue('')

    // Add user message
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: userText,
      timestamp: new Date()
    }
    setMessages((prev) => [...prev, userMsg])

    setIsTyping(true)
    await new Promise((resolve) => setTimeout(resolve, 1500))
    setIsTyping(false)

    // Clientside keyword FAQ router
    const normalized = userText.toLowerCase().trim()
    let responseText = ''

    if (normalized.includes('price') || normalized.includes('cost') || normalized.includes('fee') || normalized.includes('how much')) {
      responseText = `I offer two premium solutions depending on your goals:\n\n1. **DIY Skool Community ($67/mo)**: Ideal for DIY credit repair with <10 collections and no active bankruptcy. Includes 5 letters monthly. [More info: https://www.skool.com/creditsolution/about]\n\n2. **Advanced Restoral ($795 - $1,250)**: Our full-service, 1-on-1 legal disputing program managed entirely by my expert team. [Schedule Strategy Call: https://angelsolutionsatl.com/book-online]`
    } else if (normalized.includes('guarantee') || normalized.includes('promise')) {
      responseText = `Legally, credit repair companies are strictly prohibited from guaranteeing specific score increases or items being removed. Anyone who guarantees you otherwise is not being honest!\n\nAt Angel Solutions ATL, we commit to leveraging your full legal rights under FCRA (15 U.S.C. § 1681) to aggressively dispute reporting inaccuracies and restore your financial health. 🌟`
    } else if (normalized.includes('how long') || normalized.includes('timeline') || normalized.includes('time')) {
      responseText = `Most clients see compounding, permanent improvements in their credit profile within **3 to 6 months**. Each dispute round takes 30-45 days under federal law for the credit bureaus to investigate and respond. It requires diligence, but we make sure the process moves as fast as possible!`
    } else if (normalized.includes('scam') || normalized.includes('refund') || normalized.includes('human') || normalized.includes('speak to') || normalized.includes('lawyer')) {
      responseText = `Got it! I am pausing our automated chat and flagging our team for an immediate manual takeover. Let's make sure we take care of you right away. 😊\n\nWhile my manual consultants load your chat, please fill out your contact details below so we can sync this directly to your file!`
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: responseText,
          timestamp: new Date()
        }
      ])
      setShowIntakeForm(true)
      return
    } else if (normalized.includes('bankruptcy') || normalized.includes('bk')) {
      responseText = `Yes, bankruptcies are major credit hurdles, but they can be audited! We inspect filed dates, discharge records, and schedules for reporting inaccuracies to dispute them off your report. If your bankruptcy is active/undischarged, we can route you to our manual legal specialists for assessment!`
    } else if (normalized.includes('tax') || normalized.includes('irs')) {
      responseText = `Unpaid IRS debts can feel heavy, but we have a dedicated tax resolution team! We specialize in Offer in Compromise (OIC) settlements, payment agreements, and clearing tax liens. Book a consultation: https://angelsolutionsatl.com/book-online`
    } else if (normalized.includes('funding') || normalized.includes('capital') || normalized.includes('loan')) {
      responseText = `We help secure up to $150k in unsecured business lines of credit and funding! We set up your LLC, establish business credit (PAYDEX 80+), and build banking lines. Let's pre-qualify you today!`
    } else {
      responseText = `Hey! Jordynn here. I received your question about "${userText}". While my custom AI helps answer FAQs 24/7, let's get you connected directly with me or my expert consultants to give you a definitive personal audit.\n\nLet's get your details registered so my team can review your report or secure your booking: https://angelsolutionsatl.com/book-online`
    }

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: responseText,
        timestamp: new Date()
      }
    ])

    // Prompt details form if they write manually
    if (!hasPromptedDetails) {
      setIsTyping(true)
      await new Promise((resolve) => setTimeout(resolve, 1200))
      setIsTyping(false)
      setShowIntakeForm(true)
      setHasPromptedDetails(true)
    }
  }

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormSubmittedLoading(true)

    try {
      // Wire directly to our production webhook!
      const response = await fetch('https://angel-solutions-webhook.rickjefferson.workers.dev/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          firstName: formData.firstName,
          lastName: formData.lastName,
          email: formData.email,
          phone: formData.phone,
          service: formData.service,
          message: 'Website Live Chat Widget Intake'
        }),
      })

      if (response.ok) {
        setFormSubmitted(true)
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: `Thank you, ${formData.firstName}! 🎉 Your file has been compiled and synced directly to our GoHighLevel CRM and database. My expert team will reach out to you within 24 business hours. Let's get you set up for victory!`,
            timestamp: new Date()
          }
        ])
        setShowIntakeForm(false)
      } else {
        console.error('Failed to submit live chat lead')
      }
    } catch (err) {
      console.error('Error submitting live chat lead:', err)
    } finally {
      setFormSubmittedLoading(false)
    }
  }

  return (
    <>
      {/* 1. Toggle Button with floating pulse animation */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={cn(
            "relative flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-r from-brand-gold-600 to-amber-500 text-white shadow-2xl transition-transform duration-300 hover:scale-110 active:scale-95 border border-white/20",
            isOpen && "rotate-90 bg-zinc-800"
          )}
          aria-label="Toggle live help chat"
        >
          {isOpen ? (
            <X className="h-6 w-6" />
          ) : (
            <>
              <span className="absolute -top-1 -right-1 flex h-4 w-4">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-4 w-4 bg-red-500 text-[9px] font-bold text-white items-center justify-center">1</span>
              </span>
              <MessageSquare className="h-6 w-6" />
            </>
          )}
        </button>
      </div>

      {/* 2. Floating Glassmorphic Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            className="fixed bottom-24 right-6 z-50 flex h-[580px] w-[380px] flex-col rounded-2xl border border-white/10 bg-zinc-950/85 backdrop-blur-xl shadow-2xl overflow-hidden text-white"
          >
            {/* Header: Gold Gradient Premium Aesthetic */}
            <div className="relative flex items-center justify-between bg-gradient-to-r from-zinc-900 to-zinc-950 p-4 border-b border-white/10">
              <div className="flex items-center gap-3">
                <div className="relative flex h-10 w-10 items-center justify-center rounded-full bg-brand-gold-500/10 border border-brand-gold-500/30 text-brand-gold-400 font-serif font-bold text-lg">
                  JM
                  <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-emerald-500 ring-2 ring-zinc-950 animate-pulse"></span>
                </div>
                <div>
                  <h3 className="font-serif text-sm font-bold tracking-wide text-brand-gold-400">Jordynn Miller</h3>
                  <p className="text-[11px] text-zinc-400 flex items-center gap-1">
                    <Sparkles className="h-3 w-3 text-brand-gold-500" /> AI Assistant Online
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-zinc-400 hover:text-white transition-colors p-1.5 rounded-lg hover:bg-white/5"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Conversation Flow Feed */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-white/5 scrollbar-track-transparent">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={cn(
                    "flex flex-col max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-md relative",
                    msg.role === 'user'
                      ? "bg-brand-gold-600 text-white rounded-br-none ml-auto"
                      : "bg-white/5 text-zinc-200 border border-white/10 rounded-bl-none mr-auto"
                  )}
                >
                  <p className="whitespace-pre-line">{msg.content}</p>
                  <span className="text-[9px] text-zinc-500 mt-1 block self-end">
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              ))}

              {/* Live typing indicator */}
              {isTyping && (
                <div className="flex items-center gap-2 bg-white/5 border border-white/10 max-w-[70px] rounded-2xl px-4 py-3 rounded-bl-none text-zinc-400 mr-auto">
                  <span className="h-1.5 w-1.5 bg-brand-gold-500 rounded-full animate-bounce"></span>
                  <span className="h-1.5 w-1.5 bg-brand-gold-500 rounded-full animate-bounce delay-100"></span>
                  <span className="h-1.5 w-1.5 bg-brand-gold-500 rounded-full animate-bounce delay-200"></span>
                </div>
              )}

              {/* Show FAQ Quick-Options if welcome is displayed */}
              {messages.length === 1 && !isTyping && (
                <div className="flex flex-col gap-2 pt-2">
                  <p className="text-xs text-zinc-500 uppercase tracking-wider font-semibold mb-1">Select an Option:</p>
                  {quickOptions.map((opt, i) => (
                    <button
                      key={i}
                      onClick={() => handleQuickOptionClick(opt.label, opt.value)}
                      className="text-left w-full px-4 py-2.5 rounded-xl border border-white/5 bg-white/5 hover:bg-brand-gold-500/10 hover:border-brand-gold-500/30 text-zinc-300 hover:text-brand-gold-300 text-xs font-medium transition-all duration-200 flex items-center justify-between group"
                    >
                      {opt.label}
                      <ArrowRight className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity text-brand-gold-400" />
                    </button>
                  ))}
                </div>
              )}

              {/* Lead Intake Form nested directly inside chat */}
              {showIntakeForm && !formSubmitted && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-zinc-900/90 border border-brand-gold-500/20 rounded-2xl p-4 space-y-3 mt-4 shadow-xl"
                >
                  <div className="flex items-center gap-2 text-brand-gold-400 font-serif font-bold text-xs">
                    <User className="h-4 w-4" /> SECURE ROADMAP INTAKE
                  </div>
                  <p className="text-[11px] text-zinc-400">
                    Submit your details to sync this chat directly to your private GoHighLevel client file.
                  </p>
                  
                  <form onSubmit={handleFormSubmit} className="space-y-2 text-xs">
                    <div className="grid grid-cols-2 gap-2">
                      <input
                        type="text"
                        placeholder="First Name"
                        required
                        value={formData.firstName}
                        onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                        className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white focus:border-brand-gold-500 focus:outline-none"
                      />
                      <input
                        type="text"
                        placeholder="Last Name"
                        required
                        value={formData.lastName}
                        onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                        className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white focus:border-brand-gold-500 focus:outline-none"
                      />
                    </div>
                    <input
                      type="email"
                      placeholder="Email Address"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white focus:border-brand-gold-500 focus:outline-none"
                    />
                    <input
                      type="tel"
                      placeholder="Phone Number"
                      required
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white focus:border-brand-gold-500 focus:outline-none"
                    />
                    <select
                      value={formData.service}
                      onChange={(e) => setFormData({ ...formData, service: e.target.value })}
                      className="w-full bg-zinc-900 border border-white/10 rounded-lg p-2 text-zinc-300 focus:border-brand-gold-500 focus:outline-none"
                    >
                      <option value="credit_repair">Credit Restoral & Audit</option>
                      <option value="business_funding">Business Capital Setup</option>
                      <option value="tax_resolution">IRS Tax Resolution</option>
                    </select>

                    <button
                      type="submit"
                      disabled={formLoading}
                      className="w-full bg-gradient-to-r from-brand-gold-600 to-amber-500 text-white font-bold py-2.5 rounded-lg hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
                    >
                      {formLoading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <>Pre-Qualify Now <ArrowRight className="h-3.5 w-3.5" /></>
                      )}
                    </button>
                  </form>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Bar Footer */}
            <div className="p-4 border-t border-white/10 bg-zinc-950">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <input
                  type="text"
                  placeholder="Ask a question..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:border-brand-gold-500 focus:outline-none transition-colors"
                />
                <button
                  type="submit"
                  disabled={!inputValue.trim()}
                  className="bg-brand-gold-600 hover:bg-brand-gold-500 text-white p-2.5 rounded-xl transition-colors disabled:opacity-50 disabled:hover:bg-brand-gold-600 flex items-center justify-center"
                >
                  <Send className="h-4 w-4" />
                </button>
              </form>
              <p className="text-[10px] text-zinc-500 text-center mt-2 font-light">
                Enterprise security secured by SSL & GHL CRM integrations.
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
