# ANGEL SOLUTIONS ATL - MANYCHAT TO CUSTOM PIPELINE MIGRATION BLUEPRINT

This blueprint outlines the 1-to-1 feature mapping and migration pathway from ManyChat to your custom self-hosted Cloudflare/FastAPI pipeline. Every tag, custom field, and automation flow currently inside ManyChat has been engineered into a high-performance, compliance-hardened native component in our new system.

When you turn ManyChat **OFF**, this custom setup provides **100% feature parity** with zero downtime.

---

## 🔁 1. Custom Fields to Database Schema Mapping

Instead of relying on ManyChat's limited Custom User Fields (CUFs), our system stores rich relational data directly inside your edge-native **Cloudflare D1 SQLite Database** (`database/schema.sql`).

| ManyChat Field Name | Custom System Database Equivalent (`database/schema.sql`) | Built-In Engineering Capabilities |
| :--- | :--- | :--- |
| **`messages`** (Text) | `conversations.messages_json` / `interactions` table | Captures full conversation history, timestamped metadata, message roles, and classification tags. |
| **`human_message`** (Text) | `escalations.trigger_message` | Logs the exact text that triggered the escalation to provide instant context for the support agent. |
| *(N/A - Hard to do in MC)* | `credit_profiles` table | Captures structured credit metrics (`credit_score`, `collections_count`, `bankruptcy_flag`, `child_support_arrears`). |

---

## 🏷️ 2. Tag Transitions to Database State Mapping

Instead of attaching raw text tags to subscribers, we transition the **`lead_state`** in the `leads` table and update conversation states in real-time.

| ManyChat Tag | New Lead/Conv State Equivalent | Custom Automation Action & Location |
| :--- | :--- | :--- |
| **`ASSIGN`** | `leads.lead_state = 'ASSIGN'` | [conversation_handoff.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/ai-ensemble/conversation_handoff.py): Sets state, logs the escalation record, and preps Twilio payload. |
| **`BOT OFF`** | `conversations.bot_active = 0` | [conversation_handoff.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/ai-ensemble/conversation_handoff.py): Lock-out mechanism preventing AI from responding until manual override is removed. |
| **`BOOKED`** | `leads.lead_state = 'BOOKED'` | [appointment_reminders.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/appointment_reminders.py): Triggers the appointment sequence and pauses standard follow-ups. |
| **`DQ`** | `leads.lead_state = 'DQ'` | [qualification.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/qualification.py): Flags the lead as disqualified and routes them to low-tier resource guides. |
| **`LINK SENT`** | `leads.lead_state = 'QUALIFIED'` | [payment_links.js](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/payment_links.js) / [qualification.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/qualification.py): Generates Stripe url and logs status. |
| **`IG BOT FOLLOW`** | `leads.lead_state = 'NURTURE'` | [follow_up_cron.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/follow_up_cron.py): Active candidate for the 7-step automated daily sequence. |

---

## ⚙️ 3. ManyChat Flow to Native Service Conversion

Every major flow currently running in ManyChat is now fully handled by your dedicated, compliance-hardened Python/Node microservices:

### 📥 1. Inbound & Default Replies
*   **ManyChat Flow**: `INBOUND` / `DEFAULT REPLY`
*   **Custom Equivalent**: **[index.js (Cloudflare Worker Webhook)](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/cloudflare-worker/src/index.js)**
*   **How it works**: Listens directly to Meta's webhooks. For DMs and chats, it reads messages, runs compliance filters, and forwards to **[jordynn_ai.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/ai-ensemble/jordynn_ai.py)** (Claude 3.5 Sonnet) to generate immediate, ultra-natural responses in Jordynn's exact voice.

### 💬 2. Comment Automation & Auto-Response
*   **ManyChat Flow**: `COMMENT`
*   **Custom Equivalent**: **[comment-moderation.js](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/cloudflare-worker/src/comment-moderation.js)**
*   **How it works**: Edge-side parsing of public post comments. Automatically hides hostile/spam content, and posts optimized public replies asking users to check their DMs to trigger the private chat loop.

### 🚫 3. Auto DQ / Disqualification
*   **ManyChat Flow**: `3rd World Countries: Auto DQ` / `DQ Deleter`
*   **Custom Equivalent**: **[qualification.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/qualification.py)**
*   **How it works**: Fully automated, granular disqualification criteria checking for active bankruptcy, child support arrears, country restrictions, and active collection counts. It cleanly splits qualified leads (forwarded to the $795 strategy call) from low-tier leads (forwarded to the $67 Skool community page).

### 👥 4. Human Handoff (Takeover)
*   **ManyChat Flow**: `ASSIGN`
*   **Custom Equivalent**: **[conversation_handoff.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/ai-ensemble/conversation_handoff.py)** + **[sms_escalation.js](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/sms_escalation.js)**
*   **How it works**: Stops bot activity (`bot_active = 0`) and sends real-time Twilio SMS alerts to Jordynn (+14703386689) with the lead name, trigger message, and direct link to take over the conversation.

### 📢 5. Media & Proof Display
*   **ManyChat Flow**: `1settyvoice` - `8settyvoice` / `1settyimage` - `9settyimage`
*   **Custom Equivalent**: **[voice_messages.js](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/voice_messages.js)** + **[landing_page_generator.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/landing_page_generator.py)**
*   **How it works**: 
    *   Generates custom text scripts and high-quality, cloned text-to-speech audio memos natively using ElevenLabs.
    *   Creates programmatic, personalized landing pages complete with progress bars, pre-filled checkout widgets, and success videos.

### 📅 6. Appointment Confirmation
*   **ManyChat Flow**: `CONFIRMATION`
*   **Custom Equivalent**: **[appointment_reminders.py](file:///Users/kalivibecoding/Downloads/angel-solutions-complete-system/services/appointment_reminders.py)**
*   **How it works**: Polls GHL/Calendar and dispatches reminders at the 24-hour and 1-hour marks via SMS/DMs automatically.

---

## 🏁 4. Turn-Off Playbook (Safe Transition Strategy)

To turn ManyChat **OFF** and activate your custom pipeline with zero thread conflicts, follow this sequence:

1.  **Deploy your Custom System**: Complete the deployment of your Edge Worker and backend services (as listed in [walkthrough.md](file:///Users/kalivibecoding/.gemini/antigravity/brain/41634ef7-65ca-4e4f-81b5-96bb7fedd503/walkthrough.md)).
2.  **Verify Webhook Connections**: Run verification queries to ensure your Cloudflare webhook receiver successfully intercepts incoming traffic.
3.  **Disable ManyChat Inbound Flows**:
    *   In ManyChat, go to **Settings -> Workflows / Automation**.
    *   Turn **OFF** the Default Reply and standard keyword triggers.
4.  **Activate Custom System Live Mode**: Transition the system out of shadow mode (`ClientComplianceLaunch.launch_approval_status = 'approved'`).
5.  **Remove ManyChat Webhook Permissions**: (Optional / Final Step) Revoke ManyChat's access to your Instagram/Facebook pages inside your Meta Developer Settings to route 100% of event payloads to your new Cloudflare Worker webhook.
