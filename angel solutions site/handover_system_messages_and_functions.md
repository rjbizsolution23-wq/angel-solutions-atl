# 📝 SYSTEM DICTIONARY: GREETINGS, TEMPLATES & REGEX HANDLERS
## Production-Grade Message Matrices & Code Walkthroughs
**Prepared For**: Angel Solutions ATL | Founder & CEO Jordynn Miller  
**Target Client**: Angel Solutions ATL | Founder & CEO Jordynn Miller  
**Date**: July 11, 2026  

---

> [!NOTE]
> This system dictionary provides the exact copy, variables, and code logic running your automated messenger, spam shields, and automated SMS campaigns. Use this file to copy-paste template configurations or debug triggers in the future.

---

## 💬 SECTION 1: THE JORDYNN MILLER BRAND PROMPT (GREETINGS & CORE RULES)
*   **File Reference**: [jordynn_ai.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/ai-ensemble/jordynn_ai.py)
*   **System Persona**: Anthropic Claude 3.5 Sonnet parses incoming chats under these strict behavioral parameters:

### The Persona Guidelines:
```text
You are Jordynn Miller, the elite financial strategist and founder of Angel Solutions ATL.
You speak directly in the first person ('I', 'my team', 'my business'). Never say you are an assistant, automated agent, or acting on behalf of Rick. You ARE Jordynn Miller.
Your voice is highly professional, warm, motivational, premium, and direct. You treat clients like family but maintain expert authority.
You represent a premium financial consultancy based in Atlanta, GA with 5.5 years of industry excellence, serving clients nationwide.
```

### Whitelisted Outbound Hyperlinks (Secondary Link Strip Enforced):
*   **DIY Skool Community**: `https://www.skool.com/creditsolution/about`
*   **1-on-1 Consultation Booking**: `https://angelsolutionsatl.com/book-online`
*   **Official Main Site**: `https://angelsolutionsatl.com`
*   **Client Success Proof Directory**: `https://share.google/FTVB6seubNwgSVDnd`

### Banned Terms and Censors:
The AI is strictly prohibited from using the following sales jargon. If generated, secondary python parsing replaces them automatically:
*   `credit sweep` $\rightarrow$ *"comprehensive legal disputing"*
*   `guarantee` / `guaranteed` $\rightarrow$ *"strive for"* / *"committed to"*
*   `best` $\rightarrow$ *"premium"*
*   `yo` $\rightarrow$ *"hello"*
*   `bet` $\rightarrow$ *"absolutely"*

---

## ✉️ SECTION 2: THE 7-STEP FOLLOW-UP NURTURE CADENCE (SMS & DMS)
*   **File Reference**: [follow_up_cron.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/follow_up_cron.py)
*   **Schedule**: Runs on a scheduled Cloudflare cron daily at 8:00 AM.
*   **Tracking Intervals**: Checks elapsed days since last touch: `CADENCE_DAYS = [1, 3, 5, 8, 12, 16, 18]`

### The Follow-Up Text Dictionary:

```
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| CADENCE STEP  | TIMING DELAY  | EXACT MESSAGE VALUE SENT                                                                                                           |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 1        | Day 1         | "Hey! Just checking in on you. Were you able to review the credit solutions link I sent over yesterday? Let me know! 😊"            |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 2        | Day 3         | "Hey, I know life gets super busy! Just wanted to see if you had any questions on how we dispute collections for you? We're here!" |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 3        | Day 5         | [Dynamic AI Variant]: Focuses specifically on the negative collection accounts holding them back from corporate funding.           |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 4        | Day 8         | [Dynamic AI Variant]: Delivers a motivational legal dispute insight (e.g. rights under FCRA 15 U.S.C. § 1681).                     |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 5        | Day 12        | [Dynamic AI Variant]: Invites them to schedule a personal 15-minute Strategy Call directly on Jordynn's line.                      |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 6        | Day 16        | [Dynamic AI Variant]: Pulls and highlights an approved client testimonial/success case study from your database directory.        |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
| Step 7        | Day 18        | "Happy Friday! Our dispute team has open slots for next week. If you're ready to clear those credit roadblocks, let me know! 🚀"   |
+---------------+---------------+------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 🔍 SECTION 3: INTENT CLASSIFIER, SPAM SHIELD & ESCALATION KEYWORDS
*   **File Reference**: [keyword-engine.js](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/cloudflare-worker/src/keyword-engine.js)

### 1. Intent Classification Keywords
Incoming texts are automatically categorized into one of four operational databases to streamline routing metrics:
*   `BUSINESS_FUNDING`: *funding, capital, business loan, loan, credit line, lines of credit, secure capital, grant*
*   `TAX_RESOLVE`: *tax debt, irs, tax resolution, irs relief, back taxes, unpaid taxes, tax lien, tax audit*
*   `CREDIT_REPAIR`: *credit repair, fix credit, dispute, clear credit, collections, credit score, bankruptcy, inquiries, late payments*
*   `GENERAL_INQUIRY`: Default catch-all when no matches occur.

### 2. High-Priority Escalation & Human Takeover Keywords
If any of these exact strings are detected in a message, **the bot instantly deactivates itself** and flags the lead for manual team takeover:
```javascript
const triggers = [
  "refund", "scam", "lawyer", "attorney", "court", "sue", 
  "lawsuit", "fraud", "call me", "speak to human", "speak with a person"
];
```

### 3. Immediate Disqualification (DQ) Triggers
The system automatically identifies and tags high-risk leads as "Disqualified" to protect your dispute team's bandwidth:
*   **Bankruptcy Trigger**: Mention of `bankruptcy` alongside words indicating it is open/active (`active`, `current`, `open`, `haven't discharged`).
*   **Child Support Trigger**: Mention of `child support` or `back child support` along with delinquency status (`arrears`, `behind`, `owe`, `active`).
*   **Massive Collections Count**: Mention of collections matching the pattern `[Number] collections` where the number is **10 or greater** (e.g. *"I have 14 collections"*).

---

## 🛠️ SECTION 4: THE COMPLIANCE CENSOR & LINK STRIPPER FUNCTIONS
To protect the firm from FTC/CFPB audits, a secondary safety filter processes every outbound message, sanitizing text and removing unauthorized outbound links.

### The JavaScript Handler (`cloudflare-worker/src/keyword-engine.js`):
```javascript
export function stripUnapprovedLinks(text) {
  if (!text) return "";

  const urlRegex = /(https?:\/\/[^\s]+)/gi;
  const approvedLinks = [
    "https://www.skool.com/creditsolution/about",
    "https://angelsolutionsatl.com/book-online",
    "https://angelsolutionsatl.com",
    "https://share.google/FTVB6seubNwgSVDnd"
  ];

  return text.replace(urlRegex, (url) => {
    const cleanUrl = url.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]+$/, "");
    const isApproved = approvedLinks.some(approved => cleanUrl.toLowerCase().startsWith(approved.toLowerCase()));
    return isApproved ? url : "[link removed for security]";
  });
}
```
