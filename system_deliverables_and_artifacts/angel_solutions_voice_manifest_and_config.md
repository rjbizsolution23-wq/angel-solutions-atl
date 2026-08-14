# 🎙️ ANGEL SOLUTIONS ATL - THE DEFINITIVE VOICE & CONVERSATIONAL MANIFEST

This document is the master repository and technical guide for all conversational "voice" systems configured within the Angel Solutions ATL automation suite. This includes the AI's literal **conversational brand voice (DM/SMS)**, **TwelveLabs/ElevenLabs Cloned TTS Voice Generation**, and **GoHighLevel (GHL) Smart Call Routing & Whisper Greetings**.

---

## 💬 SECTION 1: THE AI CONVERSATIONAL BRAND VOICE

To ensure Jordynn’s AI twin sounds like a natural, highly supportive human business owner rather than a generic robot, the Cloudflare Worker implements strict linguistic filters and prompting rules.

### 🎭 Conversational Styling Rules
*   **Casual LowercaseHabit:** Writes in relaxed, organic lowercase structures for casual words, standard contractions (`i'm`, `can't`, `don't`, `let's`), and conversational terms to match real-time mobile texting patterns.
*   **Ultra-Short Delivery:** Restricts responses to **1 to 2 sentences (maximum of 3)**. Busy owners do not text long, clinical paragraphs.
*   **Variety-First Openings:** Banned from starting messages with repetitive generic phrases (e.g., *"hey!"* or *"hey there!"*). It uses contextual, empathetic hook phrases (e.g., *"oh wow"*, *"absolutely"*, *"i got you"*, *"let's look at this"*).
*   **Natural Run-on Phrasing:** Allowed to utilize casual run-on pacing to preserve an authentic live-written feel (e.g., *"yeah we see that all the time with trucking companies but honestly we can get those off in like 30 to 45 days so don't sweat it"*).

### 🛑 Compliance Censors (Banned Terms)
Under strict FTC and CFPB compliance parameters, the AI automatically replaces or censors any high-risk phrases before transmission:
*   `credit sweep` $\rightarrow$ *Censored to:* `"comprehensive legal disputing"`
*   `guarantee` / `guaranteed` $\rightarrow$ *Censored to:* `"strive for"` / `"committed to"`
*   `best` $\rightarrow$ *Censored to:* `"premium"`
*   `yo` $\rightarrow$ *Censored to:* `"hello"`
*   `bet` $\rightarrow$ *Censored to:* `"absolutely"`
*   *No specific credit score point increases or time-bound guarantees are ever permitted.*

---

## 🔊 SECTION 2: ELEVENLABS CLONED TTS VOICE GENERATION

For high-converting audio voice notes inside Messenger and Instagram DMs, the system features a dedicated ElevenLabs Text-to-Speech integration mimicking Jordynn’s cloned vocal profile.

*   **Service File Location:** [services/voice_messages.js](file:///Users/kalivibecoding/Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/services/voice_messages.js)
*   **Cloned Speech Engine Model:** `eleven_monolingual_v1`
*   **Stability Settings:** `0.75` (high consistency)
*   **Clarity Boost:** `0.85` (optimum voice matching)

### ⚙️ Environment Variables Required:
```ini
# Add these secrets to Wrangler or your active environment to enable live cloning:
ELEVENLABS_API_KEY="your_elevenlabs_api_key"
ELEVENLABS_VOICE_ID="your_jordynn_voice_clone_id" # Default: 21m00Tcm4TlvDq8ikWAM (Rachel)
```

---

## 📞 SECTION 3: GOHIGHLEVEL NATIVE SMART CALL ROUTING & WHISPER

Configures your GoHighLevel (LeadConnector) business tracking line to play a warm, professional greeting whisper or your actual recorded voice note before instantly forwarding the call to your mobile line.

*   **Main GHL Office Line:** `+14705230689`
*   **Target Mobile Phone:** `+14705230674` (Jordynn Miller)
*   **Greeting / Whisper Audio File:** `https://angel-solutions-atl.pages.dev/assets/audio/Initial_Response.m4a`

### ⚙️ Quick Configuration in your GoHighLevel Dashboard:
1. Log into your **GoHighLevel Subaccount** (Angel Solutions ATL).
2. Go to **Settings** (bottom-left gear icon) ➔ **Phone Numbers**.
3. Under the **Numbers** tab, find **Default Office Number** (`+14705230689`) and click **Edit**.
4. In the editing modal:
   * **Forward Calls To:** Enter your personal mobile line `+14705230674`.
   * **Call Whisper:** Type in a text announcement (e.g., *"You have a new lead calling from Angel Solutions. Press any key to connect."*).
   * **Incoming Call Whisper Audio:** To play your authentic voice note instead of computer text, upload or paste your welcome greeting audio file:
     `https://angel-solutions-atl.pages.dev/assets/audio/Initial_Response.m4a`
5. Click **Save**.

---

## 🔁 SECTION 4: AUTOMATED MISSED-CALL TEXT-BACK (GHL WORKFLOW)

To capture every single missed call and convert them instantly via warm, personal SMS texting:
1. Navigate to **Automation** ➔ **Workflows** in GoHighLevel.
2. Click **Create Workflow** ➔ Select **Start from Scratch**.
3. Add a Workflow Trigger: **Call Status**
   * Filter: **Direction** = `Inbound`
   * Filter: **Phone Number** = `+14705230689`
4. Add an Action: **Forward Call**
   * Forward to: `+14705230674` (your mobile line)
   * Check **Enable Call Whisper** and select your greeting.
5. Add an **If/Else Condition** action immediately following the call:
   * If Call Status is: `Busy`, `No Answer`, `Failed`, or `Voicemail`.
6. Under the "Yes" branch (Missed Call), add a **Send SMS** action with your signature conversational tone:
   *"hey, this is jordynn with angel solutions! i'm with a client right now but just saw your call—how can I help you today?"*
7. Set the workflow to **Publish** and click **Save**.
