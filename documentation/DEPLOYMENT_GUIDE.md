# Angel Solutions ATL - Complete Deployment Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Account Setup](#account-setup)
3. [Database Deployment](#database-deployment)
4. [Service Deployment](#service-deployment)
5. [Meta Platform Configuration](#meta-platform-configuration)
6. [Testing & Validation](#testing--validation)
7. [Go-Live Checklist](#go-live-checklist)
8. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Software
```bash
# Install Node.js 18+ (LTS recommended)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.10+
sudo apt-get install python3.10 python3-pip

# Install Wrangler CLI (Cloudflare)
npm install -g wrangler

# Install Railway CLI (optional but recommended)
npm install -g @railway/cli
```

### Required API Keys & Accounts

| Service | Purpose | Sign Up URL | Est. Cost |
|---------|---------|-------------|-----------|
| Meta Developer | Messenger/Instagram/WhatsApp APIs | https://developers.facebook.com | Free |
| Anthropic | Claude AI (primary) | https://console.anthropic.com | $100/mo |
| GoHighLevel | CRM & Pipeline | https://app.gohighlevel.com | $97-297/mo |
| Twilio | SMS Alerts | https://www.twilio.com/try-twilio | $20/mo |
| Stripe | Payment Processing | https://dashboard.stripe.com/register | 2.9% + $0.30 |
| Cloudflare | Edge Compute & Database | https://dash.cloudflare.com/sign-up | $5-10/mo |
| ElevenLabs | Voice Messages | https://elevenlabs.io | $22/mo |
| Railway (optional) | Hosting | https://railway.app | $20/mo |

**Total Estimated Cost**: $264-449/month (scales with usage)

---

## 2. Account Setup

### Step 2.1: Meta Business Suite Access

1. **Have Rick grant Partner Access**:
   - Go to https://business.facebook.com/settings/partners
   - Click "Add Partners"
   - Enter your email address
   - Grant permissions:
     - ✅ Manage Pages
     - ✅ Manage Instagram accounts
     - ✅ View and edit Page inbox and messages
     - ✅ Send messages from Pages
     - ✅ Manage ads

2. **Accept the invitation** from your email

3. **Verify access**:
   - Facebook Page: Angel Solutions ATL (ID: 107318795356062)
   - Instagram: @jordynnpatrice

### Step 2.2: Create Meta App

1. Go to https://developers.facebook.com/apps
2. Click **Create App** → **Business** type
3. App name: "Angel Solutions ATL Automation"
4. Business Portfolio: Select Jordynn's business
5. Add Products:
   - ✅ Messenger
   - ✅ Instagram
   - ✅ WhatsApp Business API

### Step 2.3: Generate Access Tokens

**Page Access Token** (never expires):
```bash
# In Meta App Dashboard → Messenger → Settings
1. Select Page: "Angel Solutions ATL"
2. Click "Generate Token"
3. Grant all permissions:
   - pages_messaging
   - pages_read_engagement
   - pages_manage_metadata
   - instagram_basic
   - instagram_manage_messages
4. Copy token → Save securely
```

**WhatsApp Access Token**:
```bash
# In Meta App Dashboard → WhatsApp → Getting Started
1. Add phone number: +14703386689
2. Verify via SMS
3. Copy Phone Number ID
4. Generate access token
```

### Step 2.4: GoHighLevel Setup

1. Log in to https://app.gohighlevel.com
2. Navigate to **Settings → API**
3. Create new API key: "Angel Solutions ATL Automation"
4. Copy API key and Location ID

**Create Pipeline**:
```
Settings → Pipelines → New Pipeline
Name: "Angel Solutions ATL Credit Repair"

Stages:
1. New Lead (entry point)
2. Discovery Call Booked
3. Discovery Call Complete
4. Active Client
5. Lost/Dead
```

**Create Workflows**:
```
Automation → Workflows → Create Workflow

Workflow 1: "$67 Plan Nurture"
- Trigger: Tag added "qualified_67_plan"
- Actions: 7-email sequence + SMS reminders

Workflow 2: "Advanced Plan Follow-Up"
- Trigger: Tag added "qualified_advanced"
- Actions: Book call reminder + VIP nurture
```

**Add Custom Fields**:
```
Settings → Custom Fields → Contact

Fields:
- sender_id (text)
- platform (text) - messenger/instagram/whatsapp
- recommended_plan (text) - 67_plan/advanced
- credit_goal (text)
- timeline (text)
- lead_score (number)
- bankruptcy (yes/no)
- child_support (yes/no)
- collections_count (number)
```

### Step 2.5: Twilio Setup

1. Sign up at https://www.twilio.com/try-twilio
2. **Buy a phone number** (US recommended): ~$1.15/month
3. Go to Console → Account → Keys & Credentials
4. Copy:
   - Account SID
   - Auth Token
   - Your Twilio phone number

**Test SMS**:
```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
--data-urlencode "Body=Test from Angel Solutions ATL system" \
--data-urlencode "From=$TWILIO_PHONE_NUMBER" \
--data-urlencode "To=+14703386689" \
-u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

### Step 2.6: Stripe Setup

1. Log in to https://dashboard.stripe.com
2. **Create Products**:

**Product 1: Credit Repair $67/month**
```
Products → Add Product
Name: "Angel Solutions ATL - Credit Repair Monthly"
Type: Recurring
Price: $67 USD
Billing: Monthly
```

**Product 2: Advanced Repair**
```
Products → Add Product
Name: "Angel Solutions ATL - Advanced Credit Restoration"
Type: One-time
Price: $795 USD (or custom)
```

3. **Get API Keys**:
   - Developers → API Keys
   - Copy "Secret key" (starts with `sk_live_` or `sk_test_`)

4. **Set up Webhook**:
   - Developers → Webhooks → Add endpoint
   - URL: `https://YOUR_WORKER.workers.dev/stripe-webhook`
   - Events: `checkout.session.completed`, `checkout.session.expired`

---

## 3. Database Deployment

### Step 3.1: Create Cloudflare D1 Database

```bash
cd cloudflare-worker

# Authenticate with Cloudflare
wrangler login

# Create database
wrangler d1 create angel-solutions-atl

# Output will show database_id - SAVE THIS!
# Example: database_id = "abc123-def456-ghi789"
```

### Step 3.2: Update wrangler.toml

Edit `cloudflare-worker/wrangler.toml`:
```toml
[[d1_databases]]
binding = "ANGEL_DB"
database_name = "angel-solutions-atl"
database_id = "YOUR_DATABASE_ID_HERE"  # ← Replace with your ID
```

### Step 3.3: Run Schema Migration

```bash
# Execute main schema
wrangler d1 execute angel-solutions-atl --file=../database/schema.sql

# Verify tables created
wrangler d1 execute angel-solutions-atl --command="SELECT name FROM sqlite_master WHERE type='table';"

# Expected output:
# users, keywords, interactions, conversations, credit_profiles, 
# follow_ups, escalations, ghl_sync_log, comment_moderation, etc.
```

### Step 3.4: Load Seed Data

```bash
# Load initial keywords and config
wrangler d1 execute angel-solutions-atl --file=../database/seed_data.sql

# Verify keywords loaded
wrangler d1 execute angel-solutions-atl --command="SELECT COUNT(*) FROM keywords;"

# Expected: 150+ keywords
```

---

## 4. Service Deployment

### Step 4.1: Deploy Cloudflare Worker

```bash
cd cloudflare-worker

# Install dependencies
npm install

# Set secrets (one by one)
wrangler secret put META_PAGE_ACCESS_TOKEN
# → Paste your token when prompted

wrangler secret put META_VERIFY_TOKEN
# → Enter: ANGEL_SOLUTIONS_VERIFY_TOKEN_2026

wrangler secret put ANTHROPIC_API_KEY
# → Paste your Anthropic key

wrangler secret put GHL_API_KEY
# → Paste your GoHighLevel key

wrangler secret put TWILIO_AUTH_TOKEN
# → Paste your Twilio auth token

wrangler secret put STRIPE_SECRET_KEY
# → Paste your Stripe secret key

# Deploy to production
wrangler deploy

# Output will show your worker URL:
# ✨ https://angel-solutions-webhook.YOUR_SUBDOMAIN.workers.dev
```

### Step 4.2: Deploy AI Ensemble (Railway)

**Option A: Railway (Recommended)**
```bash
cd ../ai-ensemble

# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set ANTHROPIC_API_KEY=your_key_here
railway variables set OPENAI_API_KEY=your_key_here
railway variables set CLOUDFLARE_D1_API_URL=your_worker_url/api

# Deploy
railway up

# Get your service URL
railway status
# → https://your-ai-ensemble.up.railway.app
```

**Option B: Docker + Any Host**
```bash
# Build image
docker build -t angel-ai-ensemble .

# Run locally to test
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  angel-ai-ensemble

# Deploy to your preferred host (Fly.io, Render, etc.)
```

### Step 4.3: Deploy Admin Panel

```bash
cd ../admin-panel

# Railway deployment
railway init
railway variables set CLOUDFLARE_WORKER_URL=your_worker_url
railway variables set ADMIN_USERNAME=rick
railway variables set ADMIN_PASSWORD=ChangeThisPassword123!
railway up

# Get URL
railway status
# → https://your-admin-panel.up.railway.app
```

### Step 4.4: Set Up Follow-Up Cron

**Option A: Cloudflare Cron Trigger**
```bash
# Create new worker for cron
cd ../services
wrangler init angel-followup-cron

# Add to wrangler.toml:
[triggers]
crons = ["0 * * * *"]  # Every hour

# Deploy
wrangler deploy
```

**Option B: GitHub Actions** (see `.github/workflows/followup-cron.yml`)

**Option C: AWS EventBridge** (for existing AWS users)

---

## 5. Meta Platform Configuration

### Step 5.1: Configure Webhooks

1. Go to https://developers.facebook.com/apps/YOUR_APP_ID
2. Navigate to **Messenger → Settings**

**Webhook Configuration**:
```
Callback URL: https://angel-solutions-webhook.YOUR_SUBDOMAIN.workers.dev/webhook
Verify Token: ANGEL_SOLUTIONS_VERIFY_TOKEN_2026

Webhook Fields (subscribe to all):
✅ messages
✅ messaging_postbacks
✅ messaging_optins
✅ messaging_reads
✅ messaging_deliveries
✅ message_echoes
```

3. Click **Verify and Save**

4. **Subscribe App to Page**:
   - Messenger → Settings → Webhooks
   - Select Page: "Angel Solutions ATL"
   - Click Subscribe

### Step 5.2: Instagram Configuration

1. **Messenger → Settings → Instagram**
2. Click "Add Instagram Account"
3. Connect @jordynnpatrice
4. Enable "Allow Access to Messages"
5. Webhook should auto-subscribe

### Step 5.3: WhatsApp Configuration

1. **WhatsApp → Getting Started**
2. Add recipient phone number (test with Jordynn's: +14703386689)
3. Send test message from dashboard
4. Configure webhook:
   - URL: Same as above
   - Verify token: Same as above
   - Subscribe to: `messages`, `message_status`

### Step 5.4: Test Webhook Connection

```bash
# Send test message to your Page
# Then check worker logs:
wrangler tail

# You should see:
# "Received webhook event"
# "Processing message from sender: ..."
```

---

## 6. Testing & Validation

### Test 1: Webhook Verification
```bash
curl "https://YOUR_WORKER.workers.dev/webhook?hub.mode=subscribe&hub.verify_token=ANGEL_SOLUTIONS_VERIFY_TOKEN_2026&hub.challenge=test_challenge_123"

# Expected output: test_challenge_123
```

### Test 2: Message Handling
```bash
# Send test DM to Facebook Page or Instagram
# Message: "I need help fixing my credit"

# Check logs
wrangler tail

# Expected flow:
# 1. Webhook received ✓
# 2. Keyword matched: "credit" ✓
# 3. AI response generated ✓
# 4. Message sent back ✓
# 5. Logged to D1 ✓
```

### Test 3: Qualification Flow
```bash
# Continue conversation:
User: "I want to buy a house in 6 months"
# → System should route to $67 plan

User: "I need funding for my business ASAP"
# → System should route to Advanced plan

User: "I want a refund"
# → System should escalate to Rick via SMS
```

### Test 4: Compliance Engine
```bash
cd tests
python compliance_testing_suite.py

# All 30 tests should pass:
# ✅ test_prohibited_language - PASSED
# ✅ test_guarantee_promises - PASSED
# ... (all tests)
# 
# 30/30 tests passed (100% success rate)
```

### Test 5: CRM Sync
```bash
# Send qualifying message
# Then check GoHighLevel:
# 1. New contact created ✓
# 2. Added to pipeline (New Lead stage) ✓
# 3. Custom fields populated ✓
# 4. Workflow triggered ✓
```

### Test 6: SMS Escalation
```bash
# Send VIP trigger:
User: "I need a refund immediately"

# Rick should receive SMS within 30 seconds:
# "🚨 URGENT: Refund Request from John Doe..."
```

---

## 7. Go-Live Checklist

### Pre-Launch (1 Week Before)
- [ ] All API keys obtained and configured
- [ ] Cloudflare Worker deployed and tested
- [ ] AI Ensemble deployed and responding
- [ ] Database schema created with seed data
- [ ] Meta webhooks verified (Messenger + Instagram + WhatsApp)
- [ ] GoHighLevel pipeline configured
- [ ] SMS escalation tested (received on +14703386689)
- [ ] Compliance tests 100% passing
- [ ] Admin panel accessible
- [ ] Analytics dashboard live
- [ ] Backup procedures documented

### Launch Day
- [ ] Switch META_PAGE_ACCESS_TOKEN to production
- [ ] Enable Stripe live mode
- [ ] Activate follow-up cron
- [ ] Set `TEST_MODE=false` in environment
- [ ] Monitor logs for first 2 hours
- [ ] Test with 5 real conversations
- [ ] Verify GHL sync working
- [ ] Confirm SMS alerts arriving

### Post-Launch (First Week)
- [ ] Daily log reviews
- [ ] Response time monitoring (<2 seconds target)
- [ ] Compliance violation checks (should be 0)
- [ ] Lead qualification accuracy (>85% target)
- [ ] Escalation response times (<5 min target)
- [ ] User satisfaction check (review conversations)
- [ ] Performance optimization if needed

---

## 8. Troubleshooting

### Issue: Webhook Not Receiving Messages

**Symptoms**: No logs in `wrangler tail` when sending DMs

**Solutions**:
1. Verify webhook subscription:
   ```bash
   # Check Meta App Dashboard → Messenger → Webhooks
   # Should show green checkmark next to "messages"
   ```

2. Test webhook manually:
   ```bash
   curl -X POST https://YOUR_WORKER.workers.dev/webhook \
     -H "Content-Type: application/json" \
     -d '{"object":"page","entry":[{"messaging":[{"sender":{"id":"12345"},"message":{"text":"test"}}]}]}'
   ```

3. Check worker logs for errors:
   ```bash
   wrangler tail --format pretty
   ```

### Issue: AI Not Responding

**Symptoms**: Messages received but no reply sent

**Solutions**:
1. Check Anthropic API key:
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-3-5-sonnet-20241022","messages":[{"role":"user","content":"test"}],"max_tokens":10}'
   ```

2. Check AI Ensemble URL is correct in worker env
3. Review AI service logs (Railway dashboard)

### Issue: GHL Sync Failing

**Symptoms**: Leads not appearing in GoHighLevel

**Solutions**:
1. Test GHL API directly:
   ```bash
   curl -X POST "https://rest.gohighlevel.com/v1/contacts/" \
     -H "Authorization: Bearer $GHL_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"firstName":"Test","lastName":"User","email":"test@example.com","locationId":"'"$GHL_LOCATION_ID"'"}'
   ```

2. Verify GHL_LOCATION_ID matches your account
3. Check pipeline stage IDs are correct
4. Review `ghl_sync_log` table for errors:
   ```bash
   wrangler d1 execute angel-solutions-atl \
     --command="SELECT * FROM ghl_sync_log WHERE status='failed' ORDER BY synced_at DESC LIMIT 10;"
   ```

### Issue: SMS Not Sending

**Symptoms**: No SMS received when escalation triggered

**Solutions**:
1. Verify Twilio account has positive balance
2. Check phone number format (+14703386689)
3. Test Twilio directly:
   ```bash
   curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
     --data-urlencode "Body=Test" \
     --data-urlencode "From=$TWILIO_PHONE_NUMBER" \
     --data-urlencode "To=+14703386689" \
     -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
   ```

### Issue: Compliance Violations

**Symptoms**: Test suite failing or prohibited language detected

**Solutions**:
1. Review failed test output
2. Check `interactions` table for flagged messages:
   ```bash
   wrangler d1 execute angel-solutions-atl \
     --command="SELECT * FROM interactions WHERE compliance_flag=TRUE ORDER BY timestamp DESC LIMIT 20;"
   ```
3. Retrain AI with additional compliance examples
4. Add new prohibited phrases to keyword engine

### Issue: High Response Times

**Symptoms**: Messages taking >5 seconds to respond

**Solutions**:
1. Check AI Ensemble response times (should be <2s)
2. Optimize database queries (add indexes)
3. Enable Cloudflare caching for static responses
4. Consider upgrading Railway plan (more CPU/memory)
5. Implement response queue for burst traffic

---

## Emergency Contacts

**For System Issues**:
- Check status: `wrangler tail` (live logs)
- Review docs: `/documentation` folder
- Emergency fallback: Pause automation, manual handling

**For Business/Client Issues**:
- Jordynn Miller: (470) 338-6689
- Email: jordynn@angelsolutionsatl.com

---

## Next Steps After Deployment

1. **Train Rick on Admin Panel**: Walk through conversation management, override features
2. **Set Up Monitoring**: Configure Sentry/Datadog for production alerting
3. **Schedule Weekly Reviews**: Check analytics, optimize messaging, review compliance
4. **Gradual Rollout**: Start with 10% traffic, increase as confidence grows
5. **Collect Feedback**: User satisfaction surveys, conversation quality reviews

---

**System is now production-ready! 🚀**

For additional support or questions, refer to the main README.md or contact the development team.
