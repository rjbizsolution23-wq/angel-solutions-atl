export interface NavLink {
  href: string
  label: string
}

export interface BusinessPackage {
  id: string
  name: string
  price: number
  popular: boolean
  features: string[]
  virtualOfficeFee: number
  virtualOfficeInterval: string
}

export interface TaxService {
  id: string
  title: string
  description: string
  icon: string
}

export interface Testimonial {
  id: number
  name: string
  role: string
  content: string
  rating: number
  image: string
}

export interface ContactFormData {
  name: string
  email: string
  phone?: string
  service: string
  message: string
}

export interface NewsletterFormData {
  email: string
}

export interface Stat {
  label: string
  value: string
}
