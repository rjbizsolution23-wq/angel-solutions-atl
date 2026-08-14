export const SITE_CONFIG = {
  name: 'Angel Solutions ATL',
  description: 'Elite Business, Tax & Financial Solutions',
  url: 'https://angelsolutionsatl.com',
  email: 'info@angelsolutionsatl.com',
  phone: '+1 (470) 338-6689',
  address: {
    street: 'Atlanta, GA',
    city: 'Atlanta',
    state: 'GA',
    country: 'United States',
  },
  social: {
    facebook: 'https://www.facebook.com/angelsolutionsatl',
    twitter: '#',
    instagram: 'https://www.instagram.com/angelsolutionsatl',
    linkedin: 'https://www.linkedin.com/company/angelsolutionsatl',
  },
  bookingLink: 'https://angelsolutionsatl.com/book-online',
} as const

export const NAV_LINKS = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About Us' },
  { href: '/business-solutions', label: 'Business Solutions' },
  { href: '/tax-solutions', label: 'Tax Solutions' },
  { href: '/financial-solutions', label: 'Financial Solutions' },
  { href: '/funding-eligibility', label: 'Funding Scanner' },
  { href: '/resources', label: 'Resources' },
  { href: '/contact', label: 'Contact' },
] as const
