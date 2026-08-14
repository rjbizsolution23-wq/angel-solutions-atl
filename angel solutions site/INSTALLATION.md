# 🚀 Quick Installation Guide

## Prerequisites

Before you begin, ensure you have:
- ✅ Node.js 20.0.0 or higher ([Download](https://nodejs.org/))
- ✅ npm, yarn, or pnpm package manager
- ✅ Git (optional, for version control)
- ✅ Code editor (VS Code recommended)

Check your versions:
```bash
node --version  # Should be v20.0.0 or higher
npm --version   # Should be 9.0.0 or higher
```

---

## Step-by-Step Installation

### 1️⃣ Navigate to Project Directory
```bash
cd angel-solutions-premium
```

### 2️⃣ Install Dependencies
```bash
# Using npm (recommended)
npm install

# Or using yarn
yarn install

# Or using pnpm
pnpm install
```

**Installation time**: 2-5 minutes depending on your internet speed.

### 3️⃣ Set Up Environment Variables
Create a `.env.local` file in the root directory:

```bash
# Create the file
touch .env.local
```

Add these variables:
```env
# Site Configuration
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Google Analytics (optional for development)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Email Service (add when ready)
SENDGRID_API_KEY=your_sendgrid_api_key
# OR
RESEND_API_KEY=your_resend_api_key
```

### 4️⃣ Update Site Information

Edit `/lib/constants.ts`:

```typescript
export const SITE_CONFIG = {
  name: 'Angel Solutions ATL',
  description: 'Elite Business, Tax & Financial Solutions',
  url: 'https://angelsolutionsatl.com',
  email: 'info@angelsolutionsatl.com',
  phone: '+1 (404) XXX-XXXX', // 👈 UPDATE THIS
  // ... rest of config
}
```

### 5️⃣ Start Development Server

```bash
npm run dev
```

**Success!** Your site should now be running at:
```
🌐 http://localhost:3000
```

---

## 🎯 First-Time Setup Checklist

After installation, complete these steps:

### Immediate (Before Launch)
- [ ] Update phone number in `lib/constants.ts`
- [ ] Update email address if different
- [ ] Add your business logo to `public/images/`
- [ ] Replace placeholder founder image
- [ ] Update social media links
- [ ] Test contact form
- [ ] Review all text content

### Important (Week 1)
- [ ] Set up Google Analytics
- [ ] Configure email service (SendGrid/Resend)
- [ ] Add real client testimonials
- [ ] Optimize and add business images
- [ ] Complete tax solutions page
- [ ] Complete financial solutions page
- [ ] Complete about page

### Optional (Ongoing)
- [ ] Set up blog functionality
- [ ] Add more service details
- [ ] Create case studies
- [ ] Add FAQ section
- [ ] Implement live chat

---

## 🛠️ Development Commands

```bash
# Start development server (with Turbopack)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Type checking
npm run type-check
```

---

## 📂 Important Files to Know

| File | Purpose |
|------|---------|
| `/lib/constants.ts` | Site configuration, pricing, services |
| `/app/globals.css` | Styles and design tokens |
| `/tailwind.config.ts` | Color palette and theme |
| `/next.config.js` | Next.js configuration |
| `/app/layout.tsx` | Root layout and metadata |

---

## 🎨 Quick Customizations

### Change Primary Color
**File**: `tailwind.config.ts`
```typescript
colors: {
  brand: {
    gold: {
      500: '#d4a05a', // Change to your color
    }
  }
}
```

### Update Business Packages
**File**: `lib/constants.ts`
```typescript
export const BUSINESS_PACKAGES = [
  {
    id: 'option-1',
    name: 'Starter Package',
    price: 450, // Change price
    features: [...], // Update features
  }
]
```

### Add New Navigation Link
**File**: `lib/constants.ts`
```typescript
export const NAV_LINKS = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About Us' },
  { href: '/your-page', label: 'New Page' }, // Add here
]
```

---

## 🔧 Troubleshooting

### Issue: Port 3000 Already in Use
```bash
# Kill the process using port 3000
# Mac/Linux
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID [PID_NUMBER] /F
```

### Issue: Module Not Found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Build Errors
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

### Issue: TypeScript Errors
```bash
# Check TypeScript configuration
npm run type-check
```

---

## 📱 Testing Your Site

### Desktop Testing
1. Open `http://localhost:3000`
2. Test all navigation links
3. Try the contact form
4. Switch between light/dark mode
5. Test all buttons and interactions

### Mobile Testing
1. Chrome DevTools (F12)
2. Click device toolbar icon
3. Select mobile device
4. Test navigation menu
5. Test form inputs

### Browser Testing
Test in:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

## 🚀 Ready for Production?

When you're ready to deploy:

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Test production build locally**
   ```bash
   npm start
   ```

3. **Deploy to Vercel** (recommended)
   ```bash
   npm i -g vercel
   vercel login
   vercel --prod
   ```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment guide.

---

## 📚 Additional Resources

- 📖 [README.md](./README.md) - Full documentation
- 🚀 [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
- 📊 [PROJECT-SUMMARY.md](./PROJECT-SUMMARY.md) - Project overview
- 🌐 [Next.js Docs](https://nextjs.org/docs)
- 🎨 [Tailwind CSS Docs](https://tailwindcss.com/docs)
- 🎬 [Framer Motion Docs](https://www.framer.com/motion/)

---

## 💬 Need Help?

### Common Questions
**Q: How do I add a new page?**
A: Create a new folder in `/app/` with a `page.tsx` file.

**Q: How do I change colors?**
A: Edit `tailwind.config.ts` and update the color values.

**Q: How do I add images?**
A: Place images in `/public/images/` and use Next.js Image component.

**Q: How do I connect the contact form?**
A: See [DEPLOYMENT.md](./DEPLOYMENT.md) section on email integration.

### Get Support
- 📧 Technical Support: support@rjbizsolution.com
- 💼 Business Inquiries: info@angelsolutionsatl.com
- 🐛 Report Issues: Create detailed description of the problem

---

## ✅ Installation Complete!

You're all set! Your ultra-premium website is ready for development.

**Next steps:**
1. ✅ Review the site at `http://localhost:3000`
2. ✅ Update placeholder content
3. ✅ Customize colors and branding
4. ✅ Add your images
5. ✅ Test all functionality
6. ✅ Deploy when ready

**Questions?** Check the documentation or reach out for support.

---

*Happy building! 🚀*
