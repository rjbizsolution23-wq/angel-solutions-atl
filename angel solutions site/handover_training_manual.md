# 🏆 ANGEL SOLUTIONS ATL: SYSTEM OPERATOR & CLIENT HANDOVER MANUAL
## Complete Technical Reference & Business Playbook
**Prepared For**: Angel Solutions ATL | Founder & CEO Jordynn Miller  
**Target Client**: Angel Solutions ATL | Founder & CEO Jordynn Miller  
**Date**: July 11, 2026  

---

> [!NOTE]
> This master manual is divided into two distinct handbooks: **Book A: The Technical Operator Manual** (engineered for Jordynn Miller) and **Book B: The Business Operations Playbook** (engineered for Jordynn Miller). Use this document as your single source of truth for managing, scaling, and running the Angel Solutions ATL platform.

---

## 🏛️ PART A: THE TECHNICAL OPERATOR MANUAL
*Designed for Jordynn Miller / System Administrators*

### 1. Unified Architectural Blueprint
The system is built on a high-concurrency, serverless edge-native infrastructure. By utilizing **Cloudflare Pages** for the frontend and **Cloudflare Workers** + **D1 SQLite** for the backend, we achieve sub-50ms round-trip times and eliminate all database connection pooling bottlenecks.

```
                                      +------------------------------------+
                                      |       NEXT.JS FRONTEND (PAGES)     |
                                      |   https://angelsolutionsatl.com    |
                                      +-----------------+------------------+
                                                        | (API POST Form Data)
                                                        v
+-------------------------+           +-----------------+------------------+
|    CLIENT INTERFACES    |           |    CLOUDFLARE EDGE ROUTER WORKER   |
| IG Comments, DMs, SMS   +---------->+   /cloudflare-worker/src/index.js  |
+-------------------------+ (Webhooks)+--------+--------+------------------+
                                               |        |
                         +---------------------+        +------------------+
                         | (Read/Write States)                     | (Inference Calls)
                         v                                         v
            +------------+-------------+            +--------------+---------------+
            |  SQLITE RELATIONAL D1 DB |            |      AI ENSEMBLE ENGINE      |
            |     angel-solutions-db   |            |   OpenRouter API / Local LLaMA|
            +--------------------------+            +--------------+---------------+
                         |                                         |
                         | (Real-time Sync)                        | (Escalation Triggers)
                         v                                         v
            +------------+-------------+            +--------------+---------------+
            |     GOHIGHLEVEL CRM      |            |      HUMAN ESCALATION        |
            | Location: Sfvt5kBZ3EUO   |            |   Twilio SMS / Staff Alert   |
            +--------------------------+            +------------------------------+
```

---

### 2. Core Repository File Map

The codebase is split into two cleanly separated workspaces:

```
├── /angel-solutions-premium           # THE NEXT.JS 16 FRONTEND WEB APP
│   ├── /app
│   │   ├── page.tsx                    # Landing Page with dynamic modules
│   │   ├── /about                      # Jordynn Miller's Biography & SGE Q&A
│   │   ├── /business-solutions         # Turnkey corporate credit pricing tables
│   │   ├── /tax-solutions              # Advanced tax resolution modules
│   │   ├── /financial-solutions        # Interactive PAYDEX score slider
│   │   ├── /funding-eligibility        # Dynamic capital qualification scanner
│   │   ├── /resources                  # Dispute copy-paste resource library
│   │   └── /contact                    # Web contact page with GHL calendar hooks
│   └── /components
│       ├── /layout                     # Sticky header and credit-attributed footer
│       └── /sections                   # High-end glassmorphic UI modules
│
└── /angel-solutions-complete-system    # THE BACKEND AUTOMATION WORKSPACE
    ├── /cloudflare-worker
    │   ├── /src
    │   │   ├── index.js                # Core Webhook gateway & route dispatcher
    │   │   ├── keyword-engine.js       # Fast regex triggers for automated replies
    │   │   └── comment-moderation.js   # Filters bad reviews & auto-hides spam
    │   └── wrangler.toml               # Cloudflare Serverless Deployment config
    ├── /database
    │   ├── schema.sql                  # D1 tables (leads, chats, interactions)
    │   └── seed_data.sql               # Live brand metrics, settings, credentials
    └── /ai-ensemble
        ├── jordynn_ai.py               # Jordynn's first-person LLM system prompt
        ├── ml_lead_scoring.py          # Dynamic algorithm for DIY vs. 1-on-1 Restoral
        └── conversation_handoff.py     # Deactivates AI and handles human handover
```

---

### 3. Database Schema Blueprint
The backend database is running on **Cloudflare D1**. It consists of relational tables tracking lead metadata, session states, and historical chat messages.

#### Key Tables Layout (`database/schema.sql`):
```sql
CREATE TABLE leads (
  id TEXT PRIMARY KEY,
  name TEXT,
  phone TEXT,
  email TEXT,
  instagram_username TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lead_state (
  lead_id TEXT PRIMARY KEY,
  qualification_score INTEGER DEFAULT 0,
  qualification_state TEXT DEFAULT 'NEW', -- 'NEW', 'QUALIFIED', 'DQ'
  target_product TEXT,                    -- 'Skool Monthly', '1-on-1 Restoral'
  bot_active INTEGER DEFAULT 1,           -- 1 = Bot active, 0 = Paused (Human takeover)
  FOREIGN KEY(lead_id) REFERENCES leads(id)
);

CREATE TABLE chat_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id TEXT,
  sender TEXT,                            -- 'customer', 'ai', 'staff'
  message TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(lead_id) REFERENCES leads(id)
);
```

---

### 4. Step-by-Step Operator Commands

#### A. Redeploying the Cloudflare Edge Worker:
Run this command from the root of the backend directory whenever updating index logic, moderation lists, or keyword patterns:
```bash
cd cloudflare-worker && pnpm wrangler deploy
```

#### B. Executing Live Queries Against Your Production Database:
To inspect lead statuses, query the Cloudflare D1 edge database directly from your terminal:
```bash
pnpm wrangler d1 execute angel-solutions-db --remote --command="SELECT leads.name, lead_state.qualification_state, lead_state.target_product FROM leads JOIN lead_state ON leads.id = lead_state.lead_id LIMIT 10;"
```

#### C. Setting Secure Production Secrets:
Avoid hardcoding any API credentials in your source files. Use wrangler's secure vaults:
```bash
pnpm wrangler secret put OPENROUTER_API_KEY
pnpm wrangler secret put META_PAGE_ACCESS_TOKEN
pnpm wrangler secret put GOHIGHLEVEL_API_KEY
```

---

## 💅 PART B: THE CLIENT OPERATIONS PLAYBOOK
*Designed for Jordynn Miller / Business Owner & Staff*

Dear Rick,  
Welcome to your new enterprise-grade client acquisition engine! This playbook outlines how your automated assistant operates under your direct persona, filters out negative comments on your social posts, and syncs high-value leads directly into your GoHighLevel CRM.

---

### 1. How Your Automated Persona Qualifies Leads
The system processes conversations by analyzing your client's specific financial situation. It determines who is a fit for your **$67/mo DIY Skool Community** versus your premium **$795 - $1,250 1-on-1 Advanced Restoral Program**.

#### The Decision Machine:
*   **The DIY Skool Path ($67/mo)**:  
    If a user has **less than 10 collections**, a low budget, or simply wants a do-it-yourself guide, the AI smoothly routes them to register inside your Skool community:  
    👉 **Link Delivered**: `https://www.skool.com/creditsolution/about`
*   **The Premium 1-on-1 Consulting Path ($795 - $1,250)**:  
    If a user is a business owner looking for commercial funding, or has **10 or more negative collections** requiring urgent professional intervention, the AI elevates them:  
    👉 **Link Delivered**: `https://angelsolutionsatl.com/book-online`

---

### 2. Daily Workspace Dashboard: Monitoring Your Leads

Your leads are automatically synchronized into your GoHighLevel CRM under Location ID `Sfvt5kBZ3EUOws7MDWa3`. To monitor them daily:

1.  **Log into GoHighLevel** and navigate to your active **Contacts** list.
2.  Inspect the custom **Lead Tags** assigned to each contact:
    *   `Qualified-DIY`: Customer fits the Skool Monthly tier and was sent the Skool checkout link.
    *   `Qualified-Consultation`: Customer requires full-service restoral and was sent your booking scheduler.
    *   `Needs Human Interaction`: The bot has detected an escalation and is waiting for your team to reply.

---

### 3. Comment Moderation & Brand Shield
To protect your public brand image 24/7, the system acts as a digital security guard on your Instagram posts:

*   **Spam & Negative Comments**: If a bad actor leaves a comment containing words like *scam, refund, lawyer, sue, or fake*, the system **automatically hides the comment from public view within milliseconds** via the Meta API. Your public feed remains clean and prestigious.
*   **High-Value Questions**: If a client asks a positive question or requests help on a post, the system automatically replies in your brand voice:  
    *"Hey! Jordynn here. I just sent you a direct message so we can look into this for you right away! 📲"*  
    It then instantly sends them a personalized Direct Message (DM) to begin the intake flow.

---

### 4. Taking Over a Chat (Human Override Gate)
If a user asks a complex question that requires your personal touch, or if they express frustration, the system activates its **Handoff Mechanism**:

1.  **AI Silenced**: The bot instantly turns itself off for that specific lead in the database (`bot_active` is set to `0`).
2.  **Notification Dispatched**: An escalation alert is routed to your team, and the user's GoHighLevel tag is updated to `Needs Human Interaction`.
3.  **Human Chat**: You can open your standard Instagram Inbox, Twilio Portal, or GHL Conversation tab and type naturally. The bot will *never* interrupt a manual conversation.
4.  **Re-activating the Bot**: If you wish to let the bot take over the conversation again, simply click the "Re-Activate Assistant" button inside your GHL workflow or run a database update setting `bot_active = 1`.

---

### 5. Quick Links Cheatsheet

| Target Resource | Direct URL Link | Purpose |
| :--- | :--- | :--- |
| **Live Main Website** | [angelsolutionsatl.com](https://fafae8b1.angelsolutionsatl.com) | Public brand presence & package booking. |
| **DIY Community Offer** | [Join Skool Community](https://www.skool.com/creditsolution/about) | Automatic link sent to DIY/budget leads. |
| **Premium Consultation** | [Book 1-on-1 Consultation](https://angelsolutionsatl.com/book-online) | Booking link sent to Advanced Restoral leads. |
| **Client Success Proof** | [Success Reviews Directory](https://share.google/FTVB6seubNwgSVDnd) | Sent to users asking for proof of results. |
