/**
 * RJ Business Solutions - Centralized Brand Configuration
 * 
 * USAGE:
 * 1. Import this config in your components
 * 2. Replace hardcoded brand values with config references
 * 3. Makes future rebranding a single-file change
 * 
 * Example:
 * import { brand, social, contact, colors } from './brand-config';
 * 
 * <img src={brand.logo} alt={brand.logoAlt} />
 * <a href={social.linkedin}>LinkedIn</a>
 * <p>{contact.email}</p>
 */

// ============================================
// COMPANY INFO
// ============================================

export const brand = {
  name: 'RJ Business Solutions',
  shortName: 'RJ Business',
  legalName: 'RJ Business Solutions',
  founder: 'Rick Jefferson',
  tagline: 'AI-powered systems for businesses ready to scale.',
  description: 'RJ Business Solutions builds AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale.',
  
  // Logo assets
  logo: 'https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg',
  logoAlt: 'RJ Business Solutions logo',
  logoWidth: 200, // Recommended display width
  logoHeight: 60, // Recommended display height
  
  // Favicon (update paths as needed)
  favicon: '/favicon.ico',
  faviconSvg: '/favicon.svg',
  appleTouchIcon: '/apple-touch-icon.png',
  
  // URLs
  website: 'https://rjbusinesssolutions.org',
  
  // Copyright
  copyrightYear: new Date().getFullYear(),
  copyright: `© ${new Date().getFullYear()} RJ Business Solutions. All rights reserved.`,
} as const;

// ============================================
// CONTACT INFORMATION
// ============================================

export const contact = {
  email: 'support@rjbusinesssolutions.org',
  emailLink: 'mailto:support@rjbusinesssolutions.org',
  
  // Address
  address: {
    street: '1342 NM 333',
    city: 'Tijeras',
    state: 'New Mexico',
    stateCode: 'NM',
    zip: '87059',
    country: 'USA',
    countryCode: 'US',
    full: '1342 NM 333, Tijeras, New Mexico 87059',
    multiline: `1342 NM 333\nTijeras, New Mexico 87059`
  },
  
  // Phone (optional - add if needed)
  // phone: '+1 (555) 123-4567',
  // phoneLink: 'tel:+15551234567',
} as const;

// ============================================
// SOCIAL MEDIA LINKS
// ============================================

export const social = {
  linkedin: 'https://www.linkedin.com/in/rick-jefferson-314998235',
  tiktok: 'https://www.tiktok.com/@rick_jeff_solution',
  twitter: 'https://twitter.com/ricksolutions1',
  
  // Handles (for display)
  handles: {
    twitter: '@ricksolutions1',
    tiktok: '@rick_jeff_solution',
  }
} as const;

// Array format for mapping
export const socialLinks = [
  { platform: 'linkedin', url: social.linkedin, label: 'LinkedIn', icon: 'fab fa-linkedin-in' },
  { platform: 'tiktok', url: social.tiktok, label: 'TikTok', icon: 'fab fa-tiktok' },
  { platform: 'twitter', url: social.twitter, label: 'Twitter/X', icon: 'fab fa-x-twitter' },
] as const;

// ============================================
// COLOR SYSTEM
// ============================================

export const colors = {
  // Primary brand colors
  primary: '#2563eb',      // RJ Blue
  secondary: '#0ea5e9',    // Sky Blue
  accent: '#0ea5e9',       // Sky Blue (same as secondary)
  
  // Blue spectrum
  blue: '#2563eb',
  skyBlue: '#0ea5e9',
  deepBlue: '#1e3a8a',
  navy: '#0f172a',
  
  // Whites & lights
  white: '#ffffff',
  softWhite: '#f8fafc',
  lightBlue: '#eff6ff',
  borderBlue: '#bfdbfe',
  mutedBlue: '#dbeafe',
  
  // Status colors
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  info: '#0ea5e9',
  
  // Text colors
  text: '#0f172a',
  textMuted: '#475569',
  textLight: '#94a3b8',
  
  // Backgrounds
  bgDark: '#0f172a',
  bgLight: '#f8fafc',
  
  // Gradients (as strings)
  gradientPrimary: 'linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%)',
  gradientDark: 'linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%)',
  gradientLight: 'linear-gradient(180deg, #ffffff 0%, #eff6ff 100%)',
} as const;

// CSS Variable format
export const cssColors = {
  '--rj-blue': colors.blue,
  '--rj-sky-blue': colors.skyBlue,
  '--rj-deep-blue': colors.deepBlue,
  '--rj-navy': colors.navy,
  '--rj-white': colors.white,
  '--rj-soft-white': colors.softWhite,
  '--rj-light-blue': colors.lightBlue,
  '--rj-border-blue': colors.borderBlue,
  '--rj-muted-blue': colors.mutedBlue,
  '--rj-success': colors.success,
  '--rj-warning': colors.warning,
  '--rj-danger': colors.danger,
  '--rj-dark-text': colors.text,
  '--rj-muted-text': colors.textMuted,
  '--color-primary': colors.primary,
  '--color-secondary': colors.secondary,
} as const;

// ============================================
// TYPOGRAPHY
// ============================================

export const fonts = {
  heading: '"Space Grotesk", "Poppins", system-ui, sans-serif',
  body: '"Inter", system-ui, sans-serif',
  mono: '"Space Grotesk", ui-monospace, monospace',
  
  // Google Fonts import URL
  googleFontsUrl: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap',
} as const;

// ============================================
// NAVIGATION
// ============================================

export const navigation = {
  main: [
    { label: 'Home', href: '/' },
    { label: 'Services', href: '/services' },
    { label: 'About', href: '/about' },
    { label: 'Pricing', href: '/pricing' },
    { label: 'Contact', href: '/contact' },
  ],
  services: [
    { label: 'AI Automation', href: '/services/ai-automation' },
    { label: 'Credit Technology', href: '/services/credit-technology' },
    { label: 'Social Media', href: '/services/social-media' },
    { label: 'CRM & Funnels', href: '/services/crm-funnels' },
    { label: 'Client Portals', href: '/services/client-portals' },
  ],
  legal: [
    { label: 'Privacy Policy', href: '/privacy-policy' },
    { label: 'Terms of Service', href: '/terms-of-service' },
    { label: 'Refund Policy', href: '/refund-policy' },
    { label: 'Accessibility', href: '/accessibility' },
  ],
  cta: {
    label: 'Book a Call',
    href: '/book-call',
  }
} as const;

// ============================================
// SEO DEFAULTS
// ============================================

export const seo = {
  defaultTitle: 'RJ Business Solutions | AI Automation, Credit Tech & Growth Systems',
  titleTemplate: '%s | RJ Business Solutions',
  defaultDescription: 'RJ Business Solutions builds AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale.',
  siteUrl: 'https://rjbusinesssolutions.org',
  siteName: 'RJ Business Solutions',
  
  // Open Graph
  ogType: 'website',
  ogImage: brand.logo,
  ogImageAlt: 'RJ Business Solutions — AI-powered business automation and growth systems',
  
  // Twitter
  twitterCard: 'summary_large_image',
  twitterSite: '@ricksolutions1',
  twitterCreator: '@ricksolutions1',
  
  // Keywords
  keywords: [
    'AI automation',
    'credit technology',
    'business automation',
    'CRM systems',
    'fintech',
    'lead follow-up',
    'client portals',
    'Rick Jefferson',
    'RJ Business Solutions'
  ],
} as const;

// ============================================
// ABOUT / COPY BLOCKS
// ============================================

export const copy = {
  aboutCompany: {
    short: 'RJ Business Solutions builds AI-powered systems, automation workflows, and growth infrastructure for businesses ready to scale.',
    medium: `RJ Business Solutions builds AI-powered systems, automation workflows, and growth infrastructure for businesses ready to scale.

Founded by Rick Jefferson, RJ Business Solutions helps companies replace scattered manual work with clean, conversion-focused systems — from social media and DM automation to credit technology platforms, client portals, CRM workflows, payment infrastructure, and AI-powered business operations.`,
    full: `RJ Business Solutions builds AI-powered systems, automation workflows, and growth infrastructure for businesses ready to scale.

Founded by Rick Jefferson, RJ Business Solutions helps companies replace scattered manual work with clean, conversion-focused systems — from social media and DM automation to credit technology platforms, client portals, CRM workflows, payment infrastructure, and AI-powered business operations.

We do not just create pages or tools. We build connected systems designed to capture leads, automate follow-up, organize pipelines, support clients, and create measurable business growth.`
  },
  aboutFounder: {
    short: 'Rick Jefferson is a credit technology architect, AI systems builder, and business automation strategist.',
    full: `Rick Jefferson is a credit technology architect, AI systems builder, and business automation strategist focused on helping credit, fintech, and service-based businesses scale with secure, automated infrastructure.

As the founder of Rick Jefferson Solutions and a lead operator at RJ Business Solutions, Rick builds the systems behind modern growth: AI-powered credit repair platforms, credit monitoring APIs, automated client communication, payment and subscription infrastructure, client portals, social media automation, DM follow-up systems, CRM workflows, and white-label fintech platforms.`
  },
  taglines: [
    'AI-powered systems for businesses ready to scale.',
    'We turn business chaos into automated growth systems.',
    'Built systems. Better follow-up. More booked calls.',
    'Automation, credit technology, and growth infrastructure — built to convert.',
    'From scattered leads to scalable systems.',
    'Where AI automation meets real business execution.',
  ]
} as const;

// ============================================
// SERVICES
// ============================================

export const services = [
  { id: 'ai-automation', name: 'AI Business Automation' },
  { id: 'social-media', name: 'Done-For-You Social Media + DM Management' },
  { id: 'lead-followup', name: 'Lead Follow-Up Systems' },
  { id: 'crm', name: 'CRM + Pipeline Automation' },
  { id: 'credit-repair', name: 'Credit Repair Technology Platforms' },
  { id: 'credit-monitoring', name: 'Credit Monitoring / Scoring API Infrastructure' },
  { id: 'ai-agents', name: 'Conversational AI Agents' },
  { id: 'client-portals', name: 'Client Portals + Dashboards' },
  { id: 'payments', name: 'Payment + Subscription Systems' },
  { id: 'white-label', name: 'White-Label SaaS / FinTech Platforms' },
  { id: 'compliance', name: 'Compliance-Aware Workflow Design' },
  { id: 'funnels', name: 'Funnel + Landing Page Systems' },
  { id: 'bpa', name: 'Business Process Automation' },
  { id: 'agency', name: 'Agency Infrastructure' },
  { id: 'analytics', name: 'Reporting + Analytics Dashboards' },
] as const;

// ============================================
// EXPORT ALL
// ============================================

export default {
  brand,
  contact,
  social,
  socialLinks,
  colors,
  cssColors,
  fonts,
  navigation,
  seo,
  copy,
  services,
};
