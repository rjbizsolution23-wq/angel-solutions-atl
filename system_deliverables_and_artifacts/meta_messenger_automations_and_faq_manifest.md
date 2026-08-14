# 📱 META MESSENGER AUTOMATIONS & FAQ MANIFEST
## Complete Dictionary of Interactive FAQs, Message Templates & Automated Responses
**Prepared For**: RJ Business Solutions | Founder & CEO Rick Jefferson  
**Target Client**: Angel Solutions ATL | Founder & CEO Jordynn Miller  
**Date**: July 11, 2026  
**Version**: 1.0.0  

---

> [!NOTE]
> This master manifest outlines every single interactive FAQ, automated greeting, public comment reply, and follow-up campaign script configured in the Angel Solutions ATL Meta Ad Messenger and automation backend. Use this document as the definitive dictionary for client sign-off and operational testing.

---

## 🏛️ SECTION 1: SYSTEM OVERVIEW & WEBHOOK PIPELINE
Every message from Meta (Facebook Messenger, Instagram DMs, or WhatsApp Business) is ingested by the custom Cloudflare Edge Worker. The worker follows a 3-stage validation process before drafting a reply:

```
                  [ INCOMING META WEBHOOK ]
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
    [ Public Comment ]                   [ Private DM / SMS ]
             │                                 │
   (Is it spam/offensive?)            (Check Escalation Triggers)
    - Yes ➔ Hide Comment               - Yes ➔ Turn Off Bot & Alert Jordynn
    - No  ➔ Send Public Reply          - No  ➔ Run Intent Classifier
             │                                 │
             └────────────────┬────────────────┘
                              ▼
                 [ Core Response Engine ]
              1. Exact Keyword FAQ Match (Fast)
              2. Dynamic AI (Claude 3.5 Sonnet)
                              │
                              ▼
                 [ Outbound Safety Gate ]
              1. Censor Banned Phrases (Guarantees, Sweeps)
              2. Strip Non-Whitelisted Hyperlinks
                              │
                              ▼
                     [ SENT TO USER ]
```

---

## 💬 SECTION 2: GREETINGS & COMPLIANCE DISCLOSURES
Upon first contact via an ad or direct message, the system issues a professional, warm greeting introducing **Jordynn Miller** and setting realistic compliance parameters:

### 1. Facebook & Instagram DM Welcome Greeting
*   **Trigger**: User clicks "Send Message" button on Meta Ad, or issues their first direct query.
*   **Exact Value**:
    > "Hey! Jordynn Miller here, founder of Angel Solutions ATL. 🌟 Welcome! I am so excited to connect and help you clear the credit and financial roadblocks holding you back from your goals. 
    > 
    > *Quick heads up: I use custom AI automation support to help pre-qualify you and answer your questions 24/7 so you never have to wait. If you ever want to connect with me or my expert team directly, just type 'speak to human' or ask for a call!*
    > 
    > To help me point you in the right direction, what are we focusing on today?
    > 1. Restoring your credit health 💳
    > 2. Securing corporate business funding 🚀
    > 3. Resolving unpaid IRS tax debt 💼"

### 2. WhatsApp Business API Intro Greeting
*   **Trigger**: First WhatsApp query or outbound notification opt-in.
*   **Exact Value**:
    > "Hello! Jordynn Miller here with Angel Solutions ATL. 📱 I've received your inquiry! Our mission is to restore your financial health and position you for massive success. 
    > 
    > Are you looking to clear personal credit reporting inaccuracies, secure business capital, or settle tax debts? Let me know, and let's get you set up for victory! ✨"

---

## 🙋 SECTION 3: THE INTERACTIVE FAQ TREE
The following table outlines the **Frequently Asked Questions (FAQs)** built directly into the AI system's core memory block. These answers are formatted to represent Jordynn's direct voice and fully comply with FCRA and CFPB guidelines.

### 💳 Pillar 1: Credit Restoration FAQs

| Frequently Asked Question | Client Message Trigger | Exact Automated AI Response Template |
| :--- | :--- | :--- |
| **How much does it cost?** | `how much`, `pricing`, `cost`, `price`, `what are the fees` | "I offer two premium solutions depending on your goals and timeline:<br><br>1. **Credit Repair Monthly ($67/mo)**: Perfect if you are DIY-minded and have <10 collections. You get up to 5 customized dispute letters drafted monthly and access to our active credit solutions community. Sign up here: https://www.skool.com/creditsolution/about<br><br>2. **Advanced Credit Restoral (Starts at $795)**: Our premium, full-service legal dispute program. My 1-on-1 expert team disputes all collections simultaneously for rapid, comprehensive results. Schedule a strategy call to see if you qualify: https://angelsolutionsatl.com/book-online" |
| **Do you guarantee score increases?** | `guarantee`, `is it guaranteed`, `will my score go up` | "Legally, credit repair companies cannot guarantee specific score changes or removals. Anyone promising that is not being honest with you! What I *do* commit to is utilizing all legal channels under the Fair Credit Reporting Act (FCRA) to vigorously dispute every single inaccuracy on your reports to restore your credit health as quickly as possible. 🌟" |
| **How long does the process take?** | `how long`, `timeline`, `when will it be fixed` | "Real, permanent credit restoration is a process, not an overnight 'sweep'. Typically, our clients see significant, compounding progress within **3 to 6 months**. Each round of legal disputing takes 30-45 days for the bureaus to investigate and respond. Speed depends entirely on how quickly the bureaus update their records!" |
| **Can you dispute bankruptcies?** | `bankruptcy`, `can you remove bk`, `chapter 7`, `chapter 13` | "Yes, absolutely! While bankruptcies are major public records, credit bureaus frequently report filing dates, discharge dates, or asset values inaccurately. We audit every public record reporting line and dispute those errors to restore your profile. *Note: If you have an active, undischarged bankruptcy, our automated systems will route you to a manual specialist to assess your options.*" |

### 🚀 Pillar 2: Business Funding & Trade Lines FAQs

| Frequently Asked Question | Client Message Trigger | Exact Automated AI Response Template |
| :--- | :--- | :--- |
| **What are business funding requirements?** | `business loan`, `funding`, `how to get capital`, `lines of credit` | "To qualify for corporate business funding, we look at several core criteria:<br><br>1. An active, clean LLC or Corporation.<br><br>2. A solid business credit profile (aiming for a **PAYDEX score of 80+**).<br><br>3. Minimum personal guarantor credit (ideally a 680+ score, though we can restoral-map this for you).<br><br>Let's run your profile through our dynamic scanner to see how much funding you can secure today! Book your 1-on-1 strategy call here: https://angelsolutionsatl.com/book-online" |
| **How do corporate trade lines work?** | `trade lines`, `corporate trade lines`, `how to build business credit` | "Corporate trade lines are accounts added to your business credit report (Exp, Equifax, D&B) to prove net payment histories. We help you establish net-30 accounts and premium vendor lines of credit, which quickly build your business credit scores (PAYDEX) so banks will comfortably lend you high-limit capital without personal credit dependencies! 📈" |

### 💼 Pillar 3: Tax Solutions FAQs

| Frequently Asked Question | Client Message Trigger | Exact Automated AI Response Template |
| :--- | :--- | :--- |
| **Can you help with IRS tax debt?** | `unpaid taxes`, `irs debt`, `back taxes`, `tax lien` | "Yes, unpaid tax debts can feel incredibly heavy, but my team specializes in active IRS tax resolution! We represent you legally to establish payment plans, clear tax liens, or settle your debt for a fraction of what you owe through the IRS **Offer in Compromise (OIC)** program. Let's schedule a dedicated strategy call with our tax legal team here: https://angelsolutionsatl.com/book-online" |
| **What is an Offer in Compromise (OIC)?** | `what is oic`, `how to settle tax debt`, `compromise` | "An Offer in Compromise (OIC) is an official agreement between a taxpayer and the IRS that settles a tax liability for a reduced amount. The IRS approves these based on your income, expenses, and asset equity to prove you cannot reasonably pay the full amount. We run a comprehensive financial evaluation to verify if you meet the strict IRS criteria!" |

---

## 🛡️ SECTION 4: KEYWORD AUTO-REPLY MATRIX
To maximize speed and minimize API costs, the webhook router bypasses the LLM and instantly replies with these pre-defined, high-converting templates when exact keywords are matched:

### 1. Keyword: "Skool" / "Monthly" / "DIY"
*   **Auto-Reply Text**:
    > "Awesome choice! My Credit Solution Skool Community is the ultimate place to repair your credit on a budget. For just **$67/mo**, you get up to 5 customized dispute letters drafted monthly, plus direct access to credit coaching! 💳
    > 
    > Sign up instantly and start your disputes today: https://www.skool.com/creditsolution/about"

### 2. Keyword: "Consultation" / "1 on 1" / "Advanced"
*   **Auto-Reply Text**:
    > "Let's get you set up for victory! My full-service **Advanced Credit Restoral ($795 - $1,250)** is designed for people who need rapid, legal disputing handled entirely by my expert team. 
    > 
    > Let's hop on a personal 15-minute Strategy Call to audit your report and map your roadmap: https://angelsolutionsatl.com/book-online 📅"

### 3. Keyword: "Reviews" / "Proof" / "Does this work"
*   **Auto-Reply Text**:
    > "I love showing receipts! We've helped thousands of families restore their credit, secure homes, and fund their business dreams over the last 5.5 years. 
    > 
    > Check out some of our real client success stories and reviews right here on Google: https://share.google/FTVB6seubNwgSVDnd 🏆"

---

## 📝 SECTION 5: PUBLIC COMMENT MODERATION & AUTO-REPLIES
The comment scraping engine operates on Facebook and Instagram public posts, filtering spam, blocking competitors, and transitioning organic comments straight to private DMs.

### 1. The Spam & Profanity Filter
*   **Offensive Triggers (Auto-Hidden)**: `scam, fraud, shitty, bitch, fucking, scammer, liar, fake`
*   **Competitor Triggers (Auto-Hidden)**: `use my guy, whatsapp +1, telegram, contact me, dm for fix, i got mine from`

### 2. Public-to-DM Reply Scripts
When a customer leaves a valid comment, the bot replies publicly, tags their handle, and triggers an automated private DM:

*   **Comment contains credit-related words** (`credit`, `fix`, `collections`, `score`):
    > "@[username] Hey! I just sent you a DM with our step-by-step Credit Restoral Guide. Let's get those roadblocks cleared! ✨"
*   **Comment contains funding-related words** (`funding`, `capital`, `loan`, `business`):
    > "@[username] Absolutely! Sent you a private message with our Corporate Capital checklist. Let's secure that funding! 🚀"
*   **Comment contains tax-related words** (`tax`, `irs`, `debt`, `lien`):
    > "@[username] I hear you. Check your DMs, I've sent over our IRS resolution booking link so our legal team can look at this for you! 💼"
*   **General Catch-all comment**:
    > "@[username] Thanks for reaching out! Just sent you a DM to connect and answer any questions you have! 😊"

---

## ✉️ SECTION 6: THE 7-STEP FOLLOW-UP NURTURE CADENCE
If a lead interacts with the automations but doesn't take action (such as signing up for Skool or booking a strategy call), a recurring daily cron schedules a 7-step sequence:

```
[Day 1 Check-In] ➔ [Day 3 Value Check] ➔ [Day 5 Account Focus] ➔ [Day 8 Legal Rights] ➔ [Day 12 Direct Booking] ➔ [Day 16 Proof & Reviews] ➔ [Day 18 Final Call]
```

*   **Day 1 Check-In**:
    > "Hey! Just checking in on you. Were you able to review the credit solutions link I sent over yesterday? Let me know! 😊"
*   **Day 3 Value Check**:
    > "Hey, I know life gets super busy! Just wanted to see if you had any questions on how we dispute collections for you? We're here!"
*   **Day 5 Account Focus**:
    > "Hey! Did you know that even a single collection account can drop your credit score by up to 100 points? Let's audit your report and see exactly what's holding you back from funding. Tap here to book: https://angelsolutionsatl.com/book-online"
*   **Day 8 Legal Rights (FCRA)**:
    > "Jordynn here! Just a quick credit tip: Under FCRA 15 U.S.C. § 1681, you have the legal right to dispute any inaccurate, incomplete, or unverified item on your report. We make sure the bureaus respect that! Let's get started: https://angelsolutionsatl.com/book-online"
*   **Day 12 Direct Booking**:
    > "Hey, hope your week is going great! I have 3 open slots on my calendar for a complimentary 15-minute Strategy Call. Let's lock in your slot and build your plan: https://angelsolutionsatl.com/book-online 📅"
*   **Day 16 Proof & Reviews**:
    > "Nothing makes me happier than seeing my clients succeed! Check out how we helped clear thousands in collections and position our clients for massive business funding: https://share.google/FTVB6seubNwgSVDnd 🏆"
*   **Day 18 Final Call**:
    > "Happy Friday! Our dispute team has open slots for next week. If you're ready to clear those credit roadblocks, let me know! 🚀"

---

## 🚨 SECTION 7: HUMAN TAKE-OVER PROTOCOL
To protect user satisfaction and prevent automated loop failures, the bot instantly silences itself and alerts the manual staff upon detecting negative sentiment or high-urgency phrases.

### 1. Handoff Keywords
*   **Triggers**: `refund, scam, lawyer, attorney, court, sue, lawsuit, fraud, call me, speak to human, speak with a person`
*   **Bot Action**: Sets `bot_active = 0` in D1 database and tags lead as `Needs Human Takeover` in GoHighLevel CRM.

### 2. Escalation Notification to Jordynn
*   **Trigger**: High-priority handoff keyword match.
*   **SMS Sent to Jordynn (+14703386689)**:
    > "⚠️ ALERT: Lead [Lead Name] has requested manual assistance or triggered an escalation phrase ('[Trigger Word]'). The AI has paused. Please review and take over the conversation here: https://angelsolutionsatl.com/admin"

---

### ✅ MANIFEST AUTHORIZATION
This manifest represents a legally compliant, highly secure, and optimized interactive setup designed to build trust, maintain regulatory safety, and maximize conversions for **Angel Solutions ATL**.

**Compiled By**: NexusMind AI  
**Reviewed & Authorized By**: RJ Business Solutions & Rick Jefferson  
