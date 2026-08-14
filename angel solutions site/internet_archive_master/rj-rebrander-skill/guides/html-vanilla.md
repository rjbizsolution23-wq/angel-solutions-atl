# HTML/Vanilla JS Rebranding Guide

## Quick Reference

### Key Files to Update

| File Pattern | What to Replace |
|--------------|-----------------|
| `index.html` | Title, meta tags, logo, footer |
| `*.html` | Headers, footers, navigation |
| `css/style.css` or `styles.css` | Colors, fonts |
| `js/*.js` | Any hardcoded strings |
| `images/logo.*` | Logo files |
| `favicon.*` | Favicon |

---

## Step-by-Step Rebranding

### Step 1: Find All Brand References

```bash
# Find company name references
grep -rn "Aivora\|AIVORA\|aivora" --include="*.{html,css,js}" .

# Find logo references  
grep -rn "logo\|Logo" --include="*.{html,css,js}" .

# Find color codes (adjust for template's accent colors)
grep -rn "#00ff\|#0ff\|green\|teal" --include="*.{css,html}" .

# Find copyright
grep -rn "copyright\|©\|2025\|All rights" --include="*.html" .

# Find contact info
grep -rn "email\|@.*\.com\|tel:\|phone" --include="*.{html,js}" .
```

### Step 2: Update HTML Head Section

**Find in each HTML file:**
```html
<head>
    <title>Aivora - AI Agency</title>
    <meta name="description" content="...">
</head>
```

**Replace with:**
```html
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>RJ Business Solutions | AI Automation, Credit Tech & Growth Systems</title>
    <meta name="description" content="RJ Business Solutions builds AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale.">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#2563eb">
    
    <!-- Favicon -->
    <link rel="shortcut icon" type="image/x-icon" href="assets/images/favicon.ico">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="RJ Business Solutions">
    <meta property="og:title" content="RJ Business Solutions | AI Automation, Credit Tech & Growth Systems">
    <meta property="og:description" content="AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale.">
    <meta property="og:image" content="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="RJ Business Solutions | AI Automation, Credit Tech & Growth Systems">
    <meta name="twitter:description" content="AI-powered automation, credit technology, funnels, client portals, CRM workflows, and growth systems for businesses ready to scale.">
    <meta name="twitter:image" content="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
```

### Step 3: Update Logo

**Find pattern:**
```html
<div class="logo">
    <a href="index.html">
        <img src="assets/images/logo.png" alt="Logo">
    </a>
</div>
```

**Replace with:**
```html
<div class="logo">
    <a href="index.html">
        <img src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" alt="RJ Business Solutions logo">
    </a>
</div>
```

### Step 4: Update Footer

**Find pattern:**
```html
<footer>
    <div class="footer-logo">
        <img src="assets/images/logo.png" alt="Logo">
    </div>
    <div class="footer-contact">
        <p>123 Main Street, City, State</p>
        <p><a href="mailto:info@company.com">info@company.com</a></p>
        <p><a href="tel:+1234567890">+1 (234) 567-890</a></p>
    </div>
    <div class="footer-social">
        <a href="#"><i class="fab fa-facebook"></i></a>
        <a href="#"><i class="fab fa-twitter"></i></a>
    </div>
    <div class="copyright">
        <p>© 2025 Company Name. All rights reserved.</p>
    </div>
</footer>
```

**Replace with:**
```html
<footer>
    <div class="footer-logo">
        <a href="index.html">
            <img src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" alt="RJ Business Solutions logo">
        </a>
    </div>
    <div class="footer-tagline">
        <p>AI-powered systems for businesses ready to scale.</p>
    </div>
    <div class="footer-contact">
        <p>1342 NM 333, Tijeras, New Mexico 87059</p>
        <p><a href="mailto:support@rjbusinesssolutions.org">support@rjbusinesssolutions.org</a></p>
        <p><a href="https://rjbusinesssolutions.org" target="_blank">rjbusinesssolutions.org</a></p>
    </div>
    <div class="footer-social">
        <a href="https://www.linkedin.com/in/rick-jefferson-314998235" target="_blank" rel="noopener" aria-label="LinkedIn">
            <i class="fab fa-linkedin-in"></i>
        </a>
        <a href="https://www.tiktok.com/@rick_jeff_solution" target="_blank" rel="noopener" aria-label="TikTok">
            <i class="fab fa-tiktok"></i>
        </a>
        <a href="https://twitter.com/ricksolutions1" target="_blank" rel="noopener" aria-label="Twitter">
            <i class="fab fa-x-twitter"></i>
        </a>
    </div>
    <div class="copyright">
        <p>© 2026 <a href="index.html">RJ Business Solutions</a>. All rights reserved.</p>
    </div>
    <div class="legal-links">
        <a href="privacy-policy.html">Privacy Policy</a> | 
        <a href="terms-of-service.html">Terms of Service</a>
    </div>
</footer>
```

### Step 5: Update CSS Colors

**Find in CSS file:**
```css
:root {
    --primary-color: #00ff97;
    --secondary-color: #00bfff;
    --accent-color: #00ff97;
    /* etc */
}

/* Or inline colors like: */
.btn-primary {
    background-color: #00ff97;
}
```

**Replace with:**
```css
:root {
    /* RJ Business Solutions Brand Colors */
    --color-primary: #2563eb;
    --color-secondary: #0ea5e9;
    --rj-blue: #2563eb;
    --rj-sky-blue: #0ea5e9;
    --rj-deep-blue: #1e3a8a;
    --rj-navy: #0f172a;
    --rj-white: #ffffff;
    --rj-soft-white: #f8fafc;
    --rj-light-blue: #eff6ff;
    --rj-border-blue: #bfdbfe;
    --rj-success: #10b981;
    --rj-warning: #f59e0b;
    --rj-danger: #ef4444;
    --rj-dark-text: #0f172a;
    --rj-muted-text: #475569;
    
    /* Typography */
    --font-heading: "Space Grotesk", "Poppins", system-ui, sans-serif;
    --font-body: "Inter", system-ui, sans-serif;
    
    /* Gradients */
    --gradient-primary: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%);
    --gradient-dark: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
}

/* Update any hardcoded colors */
.btn-primary {
    background-color: var(--color-primary);
    background: var(--gradient-primary);
}

.btn-primary:hover {
    background-color: var(--rj-deep-blue);
}
```

### Step 6: Find/Replace Color Codes

Common color replacements for template accent colors:

| Find | Replace With |
|------|--------------|
| `#00ff97` | `#2563eb` |
| `#00FF97` | `#2563eb` |
| `#00bfff` | `#0ea5e9` |
| `#00ffff` | `#0ea5e9` |
| `rgb(0, 255, 151)` | `rgb(37, 99, 235)` |
| `rgba(0, 255, 151, 0.5)` | `rgba(37, 99, 235, 0.5)` |
| `green` (accent) | `#2563eb` |
| `teal` (accent) | `#0ea5e9` |

### Step 7: Add JSON-LD Schema

Add before `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "RJ Business Solutions",
  "legalName": "RJ Business Solutions",
  "url": "https://rjbusinesssolutions.org",
  "logo": "https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg",
  "email": "support@rjbusinesssolutions.org",
  "founder": {
    "@type": "Person",
    "name": "Rick Jefferson"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1342 NM 333",
    "addressLocality": "Tijeras",
    "addressRegion": "NM",
    "postalCode": "87059",
    "addressCountry": "US"
  },
  "sameAs": [
    "https://www.linkedin.com/in/rick-jefferson-314998235",
    "https://www.tiktok.com/@rick_jeff_solution",
    "https://twitter.com/ricksolutions1"
  ]
}
</script>
```

---

## Batch Find/Replace Commands

```bash
# Replace company name in all HTML files
find . -name "*.html" -exec sed -i 's/Aivora/RJ Business Solutions/g' {} \;

# Replace copyright year
find . -name "*.html" -exec sed -i 's/© 2025/© 2026/g' {} \;

# Replace email
find . -name "*.html" -exec sed -i 's/info@aivora.com/support@rjbusinesssolutions.org/g' {} \;
```

---

## Verification Checklist

- [ ] All HTML files have updated title
- [ ] Meta descriptions are updated
- [ ] OG tags are correct
- [ ] Logo displays in header
- [ ] Logo displays in footer
- [ ] Copyright shows "RJ Business Solutions"
- [ ] Contact email is correct
- [ ] Address is correct
- [ ] Social links are correct
- [ ] Primary colors are RJ Blue (#2563eb)
- [ ] Secondary colors are RJ Sky Blue (#0ea5e9)
- [ ] No old brand name appears anywhere
- [ ] Run: `grep -rn "Aivora" .` returns no results
