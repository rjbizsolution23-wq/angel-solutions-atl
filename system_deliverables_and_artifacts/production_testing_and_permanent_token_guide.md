# 🛡️ Production Testing & Permanent Token Guide

This guide details exactly how to verify and test the live integration, explains the serverless 24/7 operational model, and provides a step-by-step walkthrough to generate a **never-expiring** Meta Page Access Token via Facebook Business Manager.

---

## 🧪 Phase 1: How to Test the Fully Live System

Now that **ManyChat is deactivated** and your Cloudflare Worker is **fully approved (`launch_approval_status = 'approved'`)**, there are two primary ways to test and observe the system:

### Method A: High-Fidelity Sandbox Simulator (Recommended for Safety)
The Admin Panel contains a built-in sandbox testing suite that simulates inbound Meta DM payloads, allowing you to trace exactly how the system reacts without messing up live accounts.

1. **Start the Admin Panel locally**:
   ```bash
   cd /Users/kalivibecoding/Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/admin-panel
   ../venv/bin/python3 admin_panel.py
   ```
2. **Open the Dashboard**: Navigate to `http://127.0.0.1:8000` in your web browser.
3. **Use the Webhook Simulator Card**:
   * Scroll down on the **Leads & Conversations** tab to find the **Sandbox Webhook Simulator**.
   * Pick or create a test profile (e.g. *Marcus Aurelius*).
   * Enter a test query (e.g. *"Can you delete my bankruptcy and get me business funding?"*).
   * Press **Send Simulated DM Webhook**.
   * Observe the immediate output! The history log will show:
     * 📥 **User DM Inbound**
     * 🤖 **Jordynn AI Outbound reply** (fully scrubbed of uncompliant words and restricted to approved links).
     * 📊 **Lead Qualifying State & Computed Lead Score** updated.
     * ⚙️ **GHL CRM Sync** diagnostic logs indicating whether it synchronized automatically.

### Method B: Live End-to-End Direct Message Test
To see the system run under raw real-world conditions:
1. **Access a separate personal account**: Log into a personal, non-business Facebook or Instagram profile (you cannot test by messaging your own business page from the business page itself).
2. **Send a Direct Message**: Find Jordynn's Facebook Page (`Page ID: 107318795356062`) or connected Instagram account and send a DM like:
   * *"hey! can you help me fix my credit? i have a couple collections"*
3. **Observe the Instant Response Flow**:
   * Since this is a first-time contact, the Edge Worker will instantly register the lead in D1 and deliver **Jordynn's Welcome Audio Note** (`Initial_Response.m4a`) paired with a casual, low-key introductory greeting.
   * If you mention specific items like `"bankruptcy"`, it will instantly respond with her **Bankruptcy Deletion Proof** image before writing a contextual reply!
4. **Tail the Live Server Logs**:
   To see payloads and CRM operations streaming in real-time, keep this terminal command running:
   ```bash
   cd /Users/kalivibecoding/Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/cloudflare-worker
   npx wrangler tail
   ```

---

## ⚡ Phase 2: Natively Running 24/7 with Cloudflare Workers

Because the system is deployed to **Cloudflare's serverless edge infrastructure (Cloudflare Workers)**, it runs **24/7/365 with absolute zero manual maintenance**:

* **Zero Servers to Manage**: There is no computer or script that you need to keep running on your laptop. Even if your MacBook is completely turned off or disconnected from the internet, the edge worker remains fully active.
* **Instantaneous Global Compute**: The worker code is replicated across **330+ edge data centers** worldwide. When Meta dispatches a DM webhook, the closest physical server to Meta’s data center handles the request in sub-milliseconds.
* **No Idle Costs**: Unlike a traditional VPS (like AWS EC2 or DigitalOcean) which bills you every single second it is turned on, Cloudflare serverless isolates only bill for actual processing requests (with 100,000 free requests per day on the free tier).

---

## 🔑 Phase 3: Generating a Never-Expiring Meta Token

Standard Page Access Tokens generated through the Meta App Dashboard are **temporary long-lived tokens** that expire after **60 days**. If the token expires, the bot will silently stop responding until you swap it out.

To make the system bulletproof, you must create a **System User Token** in Facebook Business Manager. **These tokens never expire.**

### Step-by-Step Instructions:

#### Step 1: Create a System User
1. Go to your **[Meta Business Suite Settings](https://business.facebook.com/settings)**.
2. In the left sidebar, click **Users** $\rightarrow$ **System Users**.
3. Click **Add**.
4. Give the system user a descriptive name (e.g., `angel_solutions_agent_bot`).
5. Select **Admin** as the System User Role.
6. Click **Create System User**.

#### Step 2: Assign Assets to the System User
1. Select your newly created System User.
2. Click **Assign Assets**.
3. Under the asset selector, choose **Pages**.
4. Select Jordynn Miller's active business Facebook Page (`Page ID: 107318795356062`).
5. Toggle on **Full Control** (Manage Page / Everything).
6. Click **Save Changes**.

#### Step 3: Generate the Never-Expiring Token
1. On the same System Users page, select your system user and click **Generate New Token**.
2. Select your Meta App from the dropdown (the app you registered for the webhook).
3. Under **Permissions / Scopes**, check the following boxes:
   * `pages_messaging` (Crucial for receiving/sending DMs)
   * `pages_show_list`
   * `pages_manage_metadata`
   * `instagram_basic` (If Instagram is connected)
   * `instagram_manage_messages` (If Instagram DMs are connected)
4. Click **Generate Token**.
5. **CRITICAL**: Copy the token immediately and save it somewhere secure (it will only be displayed once).

#### Step 4: Add the New Token to Your Live Worker
Now that you have your permanent, never-expiring token, deploy it straight to your live Cloudflare Worker:
1. Open your terminal on your MacBook and run:
   ```bash
   cd /Users/kalivibecoding/Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/cloudflare-worker
   echo "YOUR_GENERATED_SYSTEM_USER_TOKEN" | npx wrangler secret put META_PAGE_ACCESS_TOKEN
   ```
2. Wrangler will encrypt and upload the secret straight to your live worker instance.
3. Your system is now **100% permanent** and will continue running 24/7/365 without ever expiring!

---

> [!TIP]
> To verify that the token was added successfully, you can run `npx wrangler secret list`. The list should show `META_PAGE_ACCESS_TOKEN`, `GHL_API_KEY`, and `GHL_LOCATION_ID` as active encrypted edge variables.
