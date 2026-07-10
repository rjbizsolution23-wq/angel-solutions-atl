# Angel Solutions ATL - Design System Guide

This document maps out the core typography hierarchies, component states, and spacing structures that define the premium visual experience of **Angel Solutions ATL**.

## 🖋️ Typography Scale

| Hierarchy | Font Family | Size | Weight | Line Height | Letter Spacing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Title** | Playfair Display | `3.25rem` / `52px` | 700 | `1.15` | `-0.02em` |
| **Page Heading (H1)** | Playfair Display | `2.5rem` / `40px` | 600 | `1.2` | `normal` |
| **Section Heading (H2)**| Playfair Display | `1.75rem` / `28px`| 600 | `1.25` | `normal` |
| **Body Paragraph** | Inter | `1.0rem` / `16px` | 400 | `1.6` | `+0.01em` |
| **Muted Annotation** | Inter | `0.875rem` / `14px`| 300 | `1.5` | `normal` |

---

## 📦 Component Styling Guidelines

- **Cards & Overlays**: Always styled using a glassmorphic background layer:
  - Background: Surface Gray with opacity `rgba(22, 22, 24, 0.7)`.
  - Border: Zinc thin line `1px solid rgba(39, 39, 42, 0.5)`.
  - Backdrop Blur: `blur(12px)`.
- **Buttons (Call to Action)**:
  - Default: Sleek Metallic Gold background (`#D4AF37`) with solid dark text (`#0F0F10`), bold weight `600`, padding `12px 24px`, border-radius `8px`.
  - Hover: Background glows with `#F3E5AB` with subtle drop shadow `var(--shadow-gold)` for rich interaction experience.
- **Form Fields**:
  - Background: `#161618` with subtle thin border `rgba(39,39,42,0.6)`.
  - Focus State: Gold metallic border glows (`var(--shadow-gold)`).
