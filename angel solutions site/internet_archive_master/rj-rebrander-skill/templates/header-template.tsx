/**
 * RJ Business Solutions - Header Component Template
 * 
 * USAGE:
 * 1. Replace existing header component content
 * 2. Preserve original CSS classes and structure where possible
 * 3. Update imports as needed for your framework
 */

import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom'; // or 'next/link' for Next.js

// Brand constants
const BRAND = {
  name: 'RJ Business Solutions',
  shortName: 'RJ Business',
  logo: 'https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg',
  logoAlt: 'RJ Business Solutions logo',
  website: 'https://rjbusinesssolutions.org'
};

// Navigation configuration
const NAV_ITEMS = [
  { 
    label: 'Home', 
    href: '/',
    submenu: null
  },
  { 
    label: 'Services', 
    href: '/services',
    submenu: [
      { label: 'AI Automation', href: '/services/ai-automation' },
      { label: 'Credit Technology', href: '/services/credit-technology' },
      { label: 'Social Media', href: '/services/social-media' },
      { label: 'CRM & Funnels', href: '/services/crm-funnels' },
      { label: 'Client Portals', href: '/services/client-portals' }
    ]
  },
  { 
    label: 'About', 
    href: '/about',
    submenu: [
      { label: 'About RJ Business', href: '/about' },
      { label: 'About Rick Jefferson', href: '/about/rick-jefferson' },
      { label: 'Case Studies', href: '/case-studies' }
    ]
  },
  { 
    label: 'Pricing', 
    href: '/pricing',
    submenu: null
  },
  { 
    label: 'Contact', 
    href: '/contact',
    submenu: null
  }
];

// CTA Button configuration
const CTA = {
  label: 'Book a Call',
  href: '/book-call',
  variant: 'primary' // 'primary' | 'secondary' | 'outline'
};

interface NavItem {
  label: string;
  href: string;
  submenu?: { label: string; href: string }[] | null;
}

const Header: React.FC = () => {
  const [isSticky, setIsSticky] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [activeSubmenu, setActiveSubmenu] = useState<string | null>(null);
  const location = useLocation();

  // Handle scroll for sticky header
  useEffect(() => {
    const handleScroll = () => {
      setIsSticky(window.scrollY > 100);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setIsMobileMenuOpen(false);
    setActiveSubmenu(null);
  }, [location]);

  // Toggle mobile menu
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  // Check if link is active
  const isActive = (href: string) => {
    if (href === '/') return location.pathname === '/';
    return location.pathname.startsWith(href);
  };

  return (
    <header 
      id="xb-header-area"
      className={`header-area header-style-one header-transparent ${isSticky ? 'is-sticky' : ''}`}
    >
      <div 
        className={`xb-header xb-sticky-stt ${isSticky ? 'xb-header-area-sticky' : ''}`}
      >
        <div className="container mxw-1650">
          <div className="header__wrap ul_li_between">
            
            {/* Logo */}
            <div className="xb-header-logo">
              <Link to="/" className="logo" onClick={() => setIsMobileMenuOpen(false)}>
                <img src={BRAND.logo} alt={BRAND.logoAlt} />
              </Link>
            </div>

            {/* Desktop Navigation */}
            <nav className="main-menu__wrap navbar navbar-expand-lg p-0">
              <ul className="main-menu collapse navbar-collapse">
                {NAV_ITEMS.map((item) => (
                  <li 
                    key={item.href}
                    className={`menu-item ${item.submenu ? 'menu-item-has-children' : ''} ${isActive(item.href) ? 'active' : ''}`}
                    onMouseEnter={() => item.submenu && setActiveSubmenu(item.label)}
                    onMouseLeave={() => setActiveSubmenu(null)}
                  >
                    <Link to={item.href}>
                      <span>{item.label}</span>
                    </Link>
                    
                    {/* Submenu */}
                    {item.submenu && (
                      <ul className={`submenu ${activeSubmenu === item.label ? 'show' : ''}`}>
                        {item.submenu.map((subItem) => (
                          <li key={subItem.href}>
                            <Link to={subItem.href}>
                              <span>{subItem.label}</span>
                            </Link>
                          </li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            </nav>

            {/* Header Actions (CTA Button + Mobile Toggle) */}
            <div className="header-actions">
              {/* CTA Button */}
              <div className="xb-header-btn d-none d-lg-block">
                <Link to={CTA.href} className="xb-btn xb-btn-primary">
                  {CTA.label}
                </Link>
              </div>

              {/* Mobile Menu Toggle */}
              <button 
                className="mobile-menu-toggle d-lg-none"
                onClick={toggleMobileMenu}
                aria-label="Toggle navigation menu"
                aria-expanded={isMobileMenuOpen}
              >
                <span className={`hamburger ${isMobileMenuOpen ? 'is-active' : ''}`}>
                  <span className="line"></span>
                  <span className="line"></span>
                  <span className="line"></span>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className={`mobile-nav ${isMobileMenuOpen ? 'is-open' : ''}`}>
        <div className="mobile-nav-inner">
          {/* Mobile Logo */}
          <div className="mobile-nav-header">
            <Link to="/" onClick={() => setIsMobileMenuOpen(false)}>
              <img src={BRAND.logo} alt={BRAND.logoAlt} />
            </Link>
            <button 
              className="mobile-nav-close"
              onClick={() => setIsMobileMenuOpen(false)}
              aria-label="Close navigation menu"
            >
              <i className="fas fa-times" />
            </button>
          </div>

          {/* Mobile Menu Items */}
          <ul className="mobile-menu-list">
            {NAV_ITEMS.map((item) => (
              <li key={item.href} className={isActive(item.href) ? 'active' : ''}>
                <Link to={item.href} onClick={() => setIsMobileMenuOpen(false)}>
                  {item.label}
                </Link>
                {item.submenu && (
                  <ul className="mobile-submenu">
                    {item.submenu.map((subItem) => (
                      <li key={subItem.href}>
                        <Link to={subItem.href} onClick={() => setIsMobileMenuOpen(false)}>
                          {subItem.label}
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>

          {/* Mobile CTA */}
          <div className="mobile-nav-cta">
            <Link 
              to={CTA.href} 
              className="xb-btn xb-btn-primary"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              {CTA.label}
            </Link>
          </div>
        </div>
      </div>

      {/* Mobile Nav Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="mobile-nav-overlay"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </header>
  );
};

export default Header;

/* ============================================
   LOGO COMPONENT (for simple replacements)
   ============================================ */

export const Logo: React.FC<{ className?: string }> = ({ className = '' }) => (
  <Link to="/" className={`logo ${className}`}>
    <img 
      src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg"
      alt="RJ Business Solutions logo"
    />
  </Link>
);

/* ============================================
   BRAND CONFIG EXPORT (for use in other components)
   ============================================ */

export const brandConfig = {
  name: 'RJ Business Solutions',
  shortName: 'RJ Business',
  logo: 'https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg',
  logoAlt: 'RJ Business Solutions logo',
  website: 'https://rjbusinesssolutions.org',
  email: 'support@rjbusinesssolutions.org',
  founder: 'Rick Jefferson'
};

/* ============================================
   HTML VERSION (for non-React templates)
   ============================================

<header id="xb-header-area" class="header-area header-style-one">
  <div class="xb-header">
    <div class="container">
      <div class="header__wrap">
        
        <!-- Logo -->
        <div class="xb-header-logo">
          <a href="/" class="logo">
            <img 
              src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" 
              alt="RJ Business Solutions logo"
            />
          </a>
        </div>

        <!-- Navigation -->
        <nav class="main-menu">
          <ul>
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/pricing">Pricing</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </nav>

        <!-- CTA Button -->
        <div class="header-cta">
          <a href="/book-call" class="btn btn-primary">Book a Call</a>
        </div>

      </div>
    </div>
  </div>
</header>

============================================ */
