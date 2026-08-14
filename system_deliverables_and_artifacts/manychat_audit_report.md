# ANGEL SOLUTIONS ATL - MANYCHAT AUDIT REPORT

This report provides a detailed breakdown of the configurations, custom user fields, tags, and automation flows fetched in real-time from the active ManyChat page (`AngelSolutionsATL`) using your API key.

---

## 🏛️ Account & Page Profile

*   **Page Name**: ✨️Credit | Business Funding | Tax Resolution✨️
*   **Instagram Username**: `@AngelSolutionsATL`
*   **Page ID**: `107318795356062`
*   **Account Category**: `Business Consultant`
*   **Timezone**: `America/New_York`
*   **Account Level**: `PRO` (Active Subscription)
*   **About Section**: 
    > *"We help entrepreneurs clear credit blemishes, secure capital, & resolve IRS tax debts. Book your Discovery Call to learn more ➡️ AngelSolutionsATL.com/book-online"*

---

## 🗂️ Folders Structure

Your flows are organized inside the main **`AI`** master category under these subfolders:
*   📁 **`1. DEMO`** — Main automation demos
    *   📁 **`Facebook`** — Facebook-specific workflows
    *   📁 **`Auto DQ`** — Disqualification routines
    *   📁 **`MEDIA FOLDER`** — Media-related interactions
        *   📁 **`IMAGE`** — Image cards/proof displays
        *   📁 **`VOICE`** — ElevenLabs voice file displays
    *   📁 **`Booking Confirmation`** — Appointment feedback flows

---

## 🤖 Active Custom User Fields (CUFs)

These are the active custom fields stored on subscriber profiles:

| Field ID | Name | Type | Description / Intent |
| :--- | :--- | :--- | :--- |
| `14509568` | `messages` | `text` | Main text log or raw thread memory |
| `14509569` | `human_message` | `text` | Captured message intended for a human agent |

---

## 🏷️ System Tags

These tags coordinate transitions between different bot stages, human takeovers, and lead categorizations:

*   `ASSIGN` — Lead handoff triggered (bot is locked out)
*   `BOT OFF` — Automation disabled globally for thread
*   `BOOKED` — Strategy call booking confirmed in GHL/Calendar
*   `DQ` — Disqualified lead (not matching minimum credit/capital thresholds)
*   `LINK SENT` — Checkout link or Skool invite dispatched
*   `IG BOT INBOUND FB` — Instagram inbound lead converted to FB
*   `IG BOT INBOUND` — General Instagram inbound hook
*   `IG BOT GENERAL` — General engagement campaign active
*   `IG BOT FOLLOW` — Follow-up nurture campaign active
*   `IG BOT FLOW` — Flow active sequence
*   `IG BOT GENERAL OFF` — General engagement paused
*   `VAFOLLOWUP` — Handed over to VA follow-up pool
*   `COLLAB` — Partnership/collaboration conversation
*   `CUSTOMFU` — Custom follow-up triggers
*   `SETY` / `SETY VOICE` — Custom media status tracking

---

## ⚙️ Configured Automation Flows

Below is the exhaustive list of active flows currently configured in your ManyChat account, categorized by their folder grouping. We will use these identifiers (`ns` values) when trigger-calling flows or updating actions:

### Inbound & Default Replying
*   **`INBOUND`** (`content20260119153719_331535`) — Handles incoming initial queries
*   **`DEFAULT REPLY`** (`content20251114140512_396887`) — Baseline fallback automated responder
*   **`DEFAULT REPLY copy`** (`content20260511153544_411703`) — Backup responder flow
*   **`NEW FOLLOWER FLOW`** (`content20251013163002_607385`) — Welcomes and nurtures new followers

### Facebook-Specific
*   **`INBOUND converted to Facebook`** (`content20260421154252_603660`)
*   **`PROOF converted to Facebook`** (`content20260421151351_505169`)

### Lead Management & Compliance
*   **`ASSIGN`** (`content20260405120550_597100`) — Locks bot and alerts support
*   **`DQ Deleter`** (`content20260129084648_802669`) — Reset / cleanup disqualified leads
*   **`3rd World Countries: Auto DQ`** (`content20240515124320_980248`) — Handles geographic DQ compliance
*   **`RESET MEMORY`** (`content20251014160539_207214`) — Clears custom field arrays

### Media, Voice & Proof Sequences
*   🔊 **Voice Flows (ElevenLabs Audio Links)**:
    *   `1settyvoice` (`content20260204161919_514345`)
    *   `2settyvoice` (`content20260204161930_263216`)
    *   `3settyvoice` (`content20260204161932_348672`)
    *   `4settyvoice` (`content20260204161933_399618`)
    *   `5settyvoice` (`content20260204161934_374709`)
    *   `6settyoice` (`content20260204161938_536284`)
    *   `7settyvoice` (`content20260204161940_188998`)
    *   `8settyvoice` (`content20260204161942_647362`)

*   🖼️ **Image Flows (Proof cards & Results Graphics)**:
    *   `1settyimage` (`content20260130080136_893837`)
    *   `2settyimage` (`content20260204161802_735329`)
    *   `3settyimage` (`content20260204161803_978261`)
    *   `4settyimage` (`content20260204161805_168340`)
    *   `5settyimage` (`content20260204161806_548307`)
    *   `6settyimage` (`content20260204161807_576356`)
    *   `7settyimage` (`content20260204161808_567978`)
    *   `8settyimage` (`content20260204161809_849171`)
    *   `9settyimage` (`content20260204161812_327339`)

*   **`COMMENT`** (`content20260421131610_952426`) — Auto-response sequence for posts/comments
*   **`CONFIRMATION`** (`content20260411084549_794589`) — Booking/strategy call reminders
*   **`PROOF`** (`content20260421133955_182714`) — Results showcase flow
*   **`SETY`** (`content20260211155851_745794`)

---

## 🎯 Next Steps & Editing Strategy

Because we have logged the exact custom fields, tags, and flows, we can seamlessly connect and coordinate the custom Python/Hono services we built with ManyChat.

For example, when our advanced **AI Ensemble** or **Lead Qualification Engine** detects a state transition (such as a lead qualifying or triggering a human handoff):
1. We can push updates directly to ManyChat custom fields (like setting `human_message` to capture handoff context).
2. We can apply standard ManyChat tags like `ASSIGN`, `DQ`, or `BOT OFF` via the API.
3. We can trigger specific ManyChat flows (such as launching a ElevenLabs `settyvoice` flow or the `CONFIRMATION` flow) programmatically.
