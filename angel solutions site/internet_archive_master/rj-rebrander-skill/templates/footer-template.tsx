/**
 * RJ Business Solutions - Footer Component Template
 * 
 * USAGE:
 * 1. Replace existing footer component content
 * 2. Preserve original CSS classes and structure where possible
 * 3. Update imports as needed for your framework
 */

import React from 'react';
import { Link } from 'react-router-dom'; // or 'next/link' for Next.js

// Brand constants - can be imported from a central config
const BRAND = {
  name: 'RJ Business Solutions',
  founder: 'Rick Jefferson',
  tagline: 'AI-powered systems for businesses ready to scale.',
  website: 'https://rjbusinesssolutions.org',
  email: 'support@rjbusinesssolutions.org',
  address: {
    street: '1342 NM 333',
    city: 'Tijeras',
    state: 'New Mexico',
    zip: '87059',
    country: 'USA',
    full: '1342 NM 333, Tijeras, New Mexico 87059'
  },
  logo: 'https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg',
  social: {
    linkedin: 'https://www.linkedin.com/in/rick-jefferson-314998235',
    tiktok: 'https://www.tiktok.com/@rick_jeff_solution',
    twitter: 'https://twitter.com/ricksolutions1'
  },
  copyright: {
    year: new Date().getFullYear(),
    text: `© ${new Date().getFullYear()} RJ Business Solutions. All rights reserved.`
  }
};

// Social icons - replace with your icon library (FontAwesome, Heroicons, etc.)
const SocialIcon: React.FC<{ platform: string }> = ({ platform }) => {
  const icons: Record<string, string> = {
    linkedin: 'fab fa-linkedin-in',
    tiktok: 'fab fa-tiktok',
    twitter: 'fab fa-x-twitter', // or 'fab fa-twitter' for old Twitter icon
    facebook: 'fab fa-facebook-f',
    instagram: 'fab fa-instagram',
    youtube: 'fab fa-youtube'
  };
  return <i className={icons[platform] || 'fas fa-link'} />;
};

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();
  
  // Social links array for mapping
  const socialLinks = [
    { platform: 'linkedin', url: BRAND.social.linkedin, label: 'LinkedIn' },
    { platform: 'tiktok', url: BRAND.social.tiktok, label: 'TikTok' },
    { platform: 'twitter', url: BRAND.social.twitter, label: 'Twitter/X' }
  ];

  // Footer navigation links
  const footerLinks = {
    company: [
      { label: 'About', href: '/about' },
      { label: 'Services', href: '/services' },
      { label: 'Case Studies', href: '/case-studies' },
      { label: 'Contact', href: '/contact' }
    ],
    services: [
      { label: 'AI Automation', href: '/services/ai-automation' },
      { label: 'Credit Technology', href: '/services/credit-technology' },
      { label: 'Social Media', href: '/services/social-media' },
      { label: 'CRM Systems', href: '/services/crm' }
    ],
    legal: [
      { label: 'Privacy Policy', href: '/privacy-policy' },
      { label: 'Terms of Service', href: '/terms-of-service' },
      { label: 'Refund Policy', href: '/refund-policy' },
      { label: 'Accessibility', href: '/accessibility' }
    ]
  };

  return (
    <footer className="xb-footer">
      {/* Footer Main Content */}
      <div className="xb-footer-main">
        <div className="container">
          <div className="row">
            {/* Brand Column */}
            <div className="col-lg-4 col-md-6">
              <div className="xb-footer-widget">
                <div className="xb-footer-logo">
                  <Link to="/">
                    <img src={BRAND.logo} alt={`${BRAND.name} logo`} />
                  </Link>
                </div>
                <p className="xb-footer-desc">
                  {BRAND.tagline}
                </p>
                <div className="xb-footer-social">
                  {socialLinks.map((social) => (
                    <a 
                      key={social.platform}
                      href={social.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      aria-label={`Visit our ${social.label}`}
                      className="xb-social-link"
                    >
                      <SocialIcon platform={social.platform} />
                    </a>
                  ))}
                </div>
              </div>
            </div>

            {/* Company Links */}
            <div className="col-lg-2 col-md-6">
              <div className="xb-footer-widget">
                <h4 className="xb-footer-title">Company</h4>
                <ul className="xb-footer-links">
                  {footerLinks.company.map((link) => (
                    <li key={link.href}>
                      <Link to={link.href}>{link.label}</Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Services Links */}
            <div className="col-lg-2 col-md-6">
              <div className="xb-footer-widget">
                <h4 className="xb-footer-title">Services</h4>
                <ul className="xb-footer-links">
                  {footerLinks.services.map((link) => (
                    <li key={link.href}>
                      <Link to={link.href}>{link.label}</Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Contact Column */}
            <div className="col-lg-4 col-md-6">
              <div className="xb-footer-widget">
                <h4 className="xb-footer-title">Contact</h4>
                <ul className="xb-footer-contact">
                  <li className="contact-item">
                    <span className="contact-icon">
                      <i className="fas fa-map-marker-alt" />
                    </span>
                    <span className="contact-text">
                      {BRAND.address.full}
                    </span>
                  </li>
                  <li className="contact-item">
                    <span className="contact-icon">
                      <i className="fas fa-envelope" />
                    </span>
                    <a href={`mailto:${BRAND.email}`} className="contact-text">
                      {BRAND.email}
                    </a>
                  </li>
                  <li className="contact-item">
                    <span className="contact-icon">
                      <i className="fas fa-globe" />
                    </span>
                    <a 
                      href={BRAND.website} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="contact-text"
                    >
                      {BRAND.website.replace('https://', '')}
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Bottom / Copyright */}
      <div className="xb-footer-bottom">
        <div className="container">
          <div className="xb-footer-bottom-inner">
            {/* Copyright */}
            <div className="copyright-item">
              <p>
                © {currentYear} <Link to="/">{BRAND.name}</Link>. All rights reserved.
              </p>
            </div>

            {/* Legal Links */}
            <div className="legal-links">
              {footerLinks.legal.map((link, index) => (
                <React.Fragment key={link.href}>
                  <Link to={link.href}>{link.label}</Link>
                  {index < footerLinks.legal.length - 1 && <span className="separator">|</span>}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

/* ============================================
   ALTERNATIVE: Simple Copyright Component
   Use this for minimal footer updates
   ============================================ */

export const SimpleCopyright: React.FC = () => (
  <div className="copyright-item">
    <p>
      © {new Date().getFullYear()}{' '}
      <Link to="/">RJ Business Solutions</Link>. All rights reserved.
    </p>
  </div>
);

/* ============================================
   ALTERNATIVE: Contact Info Component
   ============================================ */

export const ContactInfo: React.FC = () => (
  <div className="contact-info">
    <p><strong>RJ Business Solutions</strong></p>
    <p>1342 NM 333, Tijeras, New Mexico 87059</p>
    <p>
      <a href="mailto:support@rjbusinesssolutions.org">
        support@rjbusinesssolutions.org
      </a>
    </p>
    <p>
      <a href="https://rjbusinesssolutions.org" target="_blank" rel="noopener noreferrer">
        rjbusinesssolutions.org
      </a>
    </p>
  </div>
);

/* ============================================
   HTML VERSION (for non-React templates)
   ============================================

<footer class="footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-brand">
        <img 
          src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" 
          alt="RJ Business Solutions logo"
        />
        <p>AI-powered systems for businesses ready to scale.</p>
      </div>
      
      <div class="footer-contact">
        <h4>Contact</h4>
        <p>1342 NM 333, Tijeras, New Mexico 87059</p>
        <p><a href="mailto:support@rjbusinesssolutions.org">support@rjbusinesssolutions.org</a></p>
      </div>
      
      <div class="footer-social">
        <a href="https://www.linkedin.com/in/rick-jefferson-314998235" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://www.tiktok.com/@rick_jeff_solution" target="_blank" rel="noopener">TikTok</a>
        <a href="https://twitter.com/ricksolutions1" target="_blank" rel="noopener">Twitter/X</a>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>© 2026 <a href="/">RJ Business Solutions</a>. All rights reserved.</p>
      <div class="legal-links">
        <a href="/privacy-policy">Privacy Policy</a>
        <a href="/terms-of-service">Terms of Service</a>
      </div>
    </div>
  </div>
</footer>

============================================ */
