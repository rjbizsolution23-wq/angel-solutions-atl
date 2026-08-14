'use client'

import * as React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { usePathname } from 'next/navigation'
import { Menu, X, Phone, Mail } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { NAV_LINKS, SITE_CONFIG } from '@/lib/constants'
import { cn } from '@/lib/utils'
import { motion, AnimatePresence } from 'framer-motion'
import { ThemeToggle } from './theme-toggle'

export function Header() {
  const [isOpen, setIsOpen] = React.useState(false)
  const [scrolled, setScrolled] = React.useState(false)
  const pathname = usePathname()

  React.useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        scrolled ? 'nav-glass shadow-xl' : 'bg-transparent'
      )}
    >
      {/* Top bar with contact info */}
      <div className={cn(
        'border-b border-white/10 transition-all duration-300',
        scrolled ? 'h-0 opacity-0 overflow-hidden' : 'h-auto opacity-100'
      )}>
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between py-2 text-sm">
            <div className="flex items-center gap-6">
              <a
                href={`mailto:${SITE_CONFIG.email}`}
                className="flex items-center gap-2 text-muted-foreground hover:text-brand-gold-500 transition-colors"
              >
                <Mail className="h-4 w-4" />
                <span className="hidden sm:inline">{SITE_CONFIG.email}</span>
              </a>
              <a
                href={`tel:${SITE_CONFIG.phone}`}
                className="flex items-center gap-2 text-muted-foreground hover:text-brand-gold-500 transition-colors"
              >
                <Phone className="h-4 w-4" />
                <span className="hidden sm:inline">{SITE_CONFIG.phone}</span>
              </a>
            </div>
            <div className="hidden md:flex items-center gap-4">
              <span className="text-muted-foreground">Empowering Business Growth</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main navigation */}
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative w-12 h-12 flex items-center justify-center transition-all duration-300 group-hover:scale-110">
              <Image
                src="/assets/logos/primary/logos-primary-2446f0_364e0a9712d24cc39d9b1ab72f9212a8.png"
                alt="Angel Solutions ATL Logo"
                fill
                className="object-contain"
                priority
              />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-foreground group-hover:text-brand-gold-600 transition-colors">
                Angel Solutions ATL
              </span>
              <span className="text-xs text-muted-foreground">ATL</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 relative',
                  pathname === link.href
                    ? 'text-brand-gold-600 dark:text-brand-gold-400'
                    : 'text-foreground hover:text-brand-gold-600 dark:hover:text-brand-gold-400'
                )}
              >
                {link.label}
                {pathname === link.href && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute inset-0 bg-brand-gold-50 dark:bg-brand-gold-950/20 rounded-lg -z-10"
                    transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                  />
                )}
              </Link>
            ))}
          </nav>

          {/* CTA Button & Theme Toggle */}
          <div className="hidden lg:flex items-center gap-4">
            <ThemeToggle />
            <Button asChild size="lg" className="shadow-lg">
              <Link href="/contact">Get Started</Link>
            </Button>
          </div>

          {/* Mobile menu actions */}
          <div className="flex lg:hidden items-center gap-2">
            <ThemeToggle />
            <button
              className="p-2 rounded-lg hover:bg-accent transition-colors"
              onClick={() => setIsOpen(!isOpen)}
              aria-label="Toggle menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden border-t border-white/10 nav-glass"
          >
            <nav className="container mx-auto px-4 py-4 flex flex-col gap-2">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setIsOpen(false)}
                  className={cn(
                    'px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200',
                    pathname === link.href
                      ? 'bg-brand-gold-50 text-brand-gold-600 dark:bg-brand-gold-950/20 dark:text-brand-gold-400'
                      : 'text-foreground hover:bg-accent'
                  )}
                >
                  {link.label}
                </Link>
              ))}
              <Button asChild size="lg" className="mt-4">
                <Link href="/contact" onClick={() => setIsOpen(false)}>
                  Get Started
                </Link>
              </Button>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
