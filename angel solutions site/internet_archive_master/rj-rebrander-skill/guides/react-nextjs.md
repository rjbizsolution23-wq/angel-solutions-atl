# React/Next.js Rebranding Guide

## Quick Reference

### Key Files to Update

| File Pattern | What to Replace |
|--------------|-----------------|
| `src/components/Header*.tsx` | Logo, company name, navigation |
| `src/components/Footer*.tsx` | Logo, copyright, contact, socials |
| `public/index.html` or `app/layout.tsx` | Meta tags, title, favicon |
| `public/manifest.json` | App name, theme color |
| `src/index.css` or `globals.css` | CSS variables, colors |
| `tailwind.config.js` | Theme colors, fonts |
| `package.json` | Project name |
| `*.tsx` files with hardcoded strings | Company name, taglines |

---

## Step-by-Step Rebranding

### Step 1: Find All Brand References

```bash
# Find company name references
grep -rn "Aivora\|AIVORA" --include="*.{tsx,ts,jsx,js,css,json,html,md}" .

# Find logo references
grep -rn "logo\|Logo" --include="*.{tsx,ts,jsx,js}" src/

# Find color patterns (common accent colors)
grep -rn "#00ff\|#0ff\|rgb(0,\|rgba(0," --include="*.{css,scss,tsx,ts}" .

# Find copyright notices
grep -rn "copyright\|Copyright\|©\|2025\|2024\|2023" --include="*.{tsx,ts,jsx,js,html}" .

# Find contact info
grep -rn "@.*\.com\|@.*\.org\|tel:\|mailto:" --include="*.{tsx,ts,jsx,js,html}" .
```

### Step 2: Update Logo Import

**Before (typical pattern):**
```tsx
// src/components/Header/Header.tsx
import logo from '../../assets/images/logo.png';
// or
const logo = '/images/logo.svg';
```

**After (RJ Business Solutions):**
```tsx
// Option A: Direct URL (simplest)
const logo = 'https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg';

// Option B: Import from brand config
import { brand } from '../../config/brand';
// Then use: brand.logo

// Option C: Download and use local file
import logo from '../../assets/images/rj-logo.jpeg';
```

### Step 3: Update Header Component

**Find pattern:**
```tsx
<div className="xb-header-logo">
  <Link to="/" className="logo">
    <img src={logo} alt="Logo" />
  </Link>
</div>
```

**Replace with:**
```tsx
<div className="xb-header-logo">
  <Link to="/" className="logo">
    <img 
      src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" 
      alt="RJ Business Solutions logo" 
    />
  </Link>
</div>
```

### Step 4: Update Footer Component

**Find patterns like:**
```tsx
<p>
  Copyright © 2025 <Link to="/">Aivora</Link>, All rights reserved.
</p>
```

**Replace with:**
```tsx
<p>
  © {new Date().getFullYear()} <Link to="/">RJ Business Solutions</Link>. All rights reserved.
</p>
```

**Find contact info like:**
```tsx
<span className="contact-method">4517 Washington, USA</span>
// or
<a href="tel:+1123045285897">+(1)1230 452 8597</a>
```

**Replace with:**
```tsx
<span className="contact-method">1342 NM 333, Tijeras, New Mexico 87059</span>
// or
<a href="mailto:support@rjbusinesssolutions.org">support@rjbusinesssolutions.org</a>
```

### Step 5: Update CSS Variables

**Find in `src/index.css`, `globals.css`, or theme file:**
```css
:root {
  --color-primary: #00ff97;
  --color-secondary: #00bfff;
  /* etc */
}
```

**Replace with:**
```css
:root {
  /* RJ Business Solutions Colors */
  --color-primary: #2563eb;
  --color-secondary: #0ea5e9;
  --rj-blue: #2563eb;
  --rj-sky-blue: #0ea5e9;
  --rj-deep-blue: #1e3a8a;
  --rj-navy: #0f172a;
  --rj-white: #ffffff;
  --rj-soft-white: #f8fafc;
  --rj-light-blue: #eff6ff;
  --rj-success: #10b981;
  --rj-warning: #f59e0b;
  --rj-danger: #ef4444;
  --rj-dark-text: #0f172a;
  --rj-muted-text: #475569;
}
```

### Step 6: Update Tailwind Config (if applicable)

**File: `tailwind.config.js`**

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        rj: {
          blue: '#2563eb',
          sky: '#0ea5e9',
          deep: '#1e3a8a',
          navy: '#0f172a',
        }
      },
      fontFamily: {
        heading: ['Space Grotesk', 'Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

### Step 7: Update Meta Tags

**File: `public/index.html` (CRA) or `app/layout.tsx` (Next.js)**

```html
<head>
  <meta charset="utf-8" />
  <title>RJ Business Solutions | AI Automation, Credit Tech & Growth Systems</title>
  <meta name="description" content="RJ Business Solutions builds AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale." />
  <meta name="theme-color" content="#2563eb" />
  
  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="RJ Business Solutions" />
  <meta property="og:title" content="RJ Business Solutions | AI Automation, Credit Tech & Growth Systems" />
  <meta property="og:description" content="AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale." />
  <meta property="og:image" content="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" />
</head>
```

### Step 8: Update manifest.json

```json
{
  "short_name": "RJ Business",
  "name": "RJ Business Solutions",
  "description": "AI-powered systems for businesses ready to scale.",
  "theme_color": "#2563eb",
  "background_color": "#ffffff"
}
```

### Step 9: Update package.json

```json
{
  "name": "rj-business-solutions",
  "version": "1.0.0",
  "description": "RJ Business Solutions - AI-powered business automation",
  "author": "Rick Jefferson <support@rjbusinesssolutions.org>",
  "homepage": "https://rjbusinesssolutions.org"
}
```

---

## Common Component Patterns

### Replacing Social Links

**Find:**
```tsx
const socials = [
  { icon: 'facebook', url: 'https://facebook.com/...' },
  { icon: 'twitter', url: 'https://twitter.com/...' },
];
```

**Replace:**
```tsx
const socials = [
  { icon: 'linkedin', url: 'https://www.linkedin.com/in/rick-jefferson-314998235' },
  { icon: 'tiktok', url: 'https://www.tiktok.com/@rick_jeff_solution' },
  { icon: 'twitter', url: 'https://twitter.com/ricksolutions1' },
];
```

### Replacing Hardcoded Text

Use grep to find and replace:

```bash
# Find all instances
grep -rn "Aivora" --include="*.tsx" src/

# Common replacements:
# "Aivora" → "RJ Business Solutions"
# "AI Agency" → "AI Business Solutions"
# "info@aivora.com" → "support@rjbusinesssolutions.org"
```

---

## Verification Checklist

After rebranding, verify:

- [ ] Logo displays correctly in header
- [ ] Logo displays correctly in footer
- [ ] Logo displays correctly in mobile menu
- [ ] Copyright text shows "RJ Business Solutions"
- [ ] Copyright year is current (dynamic)
- [ ] Contact email is correct
- [ ] Address is correct
- [ ] Social links work and are correct
- [ ] Meta title shows correctly
- [ ] OG image displays correctly (test with Facebook debugger)
- [ ] Favicon displays correctly
- [ ] No old brand references in console
- [ ] Run: `grep -rn "Aivora" .` returns no results
- [ ] All pages load without errors
- [ ] All links navigate correctly
