# Web Template Rebrander - Claude Skill

**Version:** 2.0  
**Default Brand:** RJ Business Solutions  
**Author:** Rick Jefferson / RJ Business Solutions

## Overview

This Claude skill automatically rebrands ANY web template to **RJ Business Solutions** by default. It preserves all template functionality while replacing logos, colors, typography, company info, contact details, copyright, meta tags, and SEO data.

## Quick Start

When using this skill, simply ask Claude:

```
/rebrand this template
```

Or for a specific brand:
```
/rebrand this template to "Custom Company Name"
```

## What Gets Rebranded

### ✅ Automatically Updated
- **Logos** - Header, footer, favicon references
- **Company Name** - All text instances
- **Copyright** - Year and company name
- **Contact Info** - Email, address, phone
- **Social Links** - LinkedIn, TikTok, Twitter/X
- **Colors** - CSS variables, inline styles
- **Meta Tags** - Title, description, OG tags
- **JSON-LD Schema** - Organization markup
- **PWA Manifest** - App name, theme color

### 📁 Supported Frameworks
- React / Create React App
- Next.js
- Vue.js / Nuxt.js
- HTML/CSS/Vanilla JS
- Bootstrap templates
- Tailwind CSS templates

## Default Brand: RJ Business Solutions

Unless specified otherwise, all templates are rebranded to:

| Field | Value |
|-------|-------|
| **Company** | RJ Business Solutions |
| **Founder** | Rick Jefferson |
| **Website** | https://rjbusinesssolutions.org |
| **Email** | support@rjbusinesssolutions.org |
| **Address** | 1342 NM 333, Tijeras, New Mexico 87059 |
| **Logo** | [View Logo](https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg) |
| **Primary Color** | #2563eb (RJ Blue) |
| **Secondary Color** | #0ea5e9 (Sky Blue) |

### Social Links
- **LinkedIn:** https://www.linkedin.com/in/rick-jefferson-314998235
- **TikTok:** https://www.tiktok.com/@rick_jeff_solution
- **Twitter/X:** https://twitter.com/ricksolutions1

## File Structure

```
web-template-rebrander/
├── SKILL.md                    # Skill definition (required)
├── README.md                   # This file
├── brands/
│   └── rj-business-solutions.md   # Complete brand kit
├── templates/
│   ├── css-variables.css       # CSS color system
│   ├── footer-template.tsx     # Footer component
│   ├── header-template.tsx     # Header component
│   ├── meta-tags.html          # SEO meta tags
│   ├── manifest.json           # PWA manifest
│   └── brand-config.ts         # Centralized brand config
├── guides/
│   ├── react-nextjs.md         # React/Next.js guide
│   └── html-vanilla.md         # HTML/Vanilla JS guide
└── scripts/
    └── rebrand.sh              # Automation script
```

## Usage Instructions

### 1. Automatic Rebranding (Recommended)

Just provide the template files and ask:
```
Please rebrand this template to RJ Business Solutions
```

Claude will:
1. Scan all files for brand touchpoints
2. Replace company name, logo, colors
3. Update contact info and social links
4. Fix meta tags and SEO data
5. Verify no old references remain

### 2. Custom Brand Rebranding

Provide your brand details:
```
Rebrand this template to:
- Company: My Company Name
- Logo URL: https://example.com/logo.png
- Email: contact@mycompany.com
- Colors: Primary #ff6600, Secondary #333333
```

### 3. Preview Mode

See what would change without making edits:
```
Preview the rebranding changes for this template
```

## Color System

### RJ Business Solutions Colors

```css
:root {
  --rj-blue: #2563eb;         /* Primary */
  --rj-sky-blue: #0ea5e9;     /* Secondary */
  --rj-deep-blue: #1e3a8a;    /* Dark accent */
  --rj-navy: #0f172a;         /* Dark backgrounds */
  --rj-white: #ffffff;
  --rj-soft-white: #f8fafc;
  --rj-light-blue: #eff6ff;
  --rj-success: #10b981;
  --rj-warning: #f59e0b;
  --rj-danger: #ef4444;
}
```

### Color Mapping

When replacing template colors:

| Original Pattern | Replace With |
|------------------|--------------|
| Green/Teal accents | #2563eb (RJ Blue) |
| Cyan/Aqua accents | #0ea5e9 (Sky Blue) |
| Dark backgrounds | #0f172a (Navy) |
| Success states | #10b981 |
| Warning states | #f59e0b |
| Error states | #ef4444 |

## Verification Checklist

After rebranding, verify:

- [ ] Logo displays in header
- [ ] Logo displays in footer
- [ ] Copyright shows correct year and company
- [ ] Contact email is correct
- [ ] Address is correct
- [ ] Social links work
- [ ] Primary colors are RJ Blue
- [ ] Meta title is correct
- [ ] OG image displays
- [ ] No old brand references remain
- [ ] All pages load without errors

## Functionality Preservation

**IMPORTANT:** This skill preserves ALL template functionality:

- ✅ Animations and transitions
- ✅ Interactive components
- ✅ Form handling
- ✅ Navigation behavior
- ✅ Responsive design
- ✅ Third-party integrations
- ✅ Build configurations

Only brand-related content is modified. Logic and behavior remain untouched.

## Support

For questions or issues:
- **Website:** https://rjbusinesssolutions.org
- **Email:** support@rjbusinesssolutions.org

---

© 2026 RJ Business Solutions. All rights reserved.
