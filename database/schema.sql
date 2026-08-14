-- =====================================================================
-- ANGEL SOLUTIONS ATL - D1 DATABASE SCHEMA
-- =====================================================================
-- Target Database: Cloudflare D1 (SQLite)
-- Version: 1.0.0
-- Client Intake ID: 6a46c0696b95e7dc9dd6251c (Angel Solutions ATL)
-- =====================================================================

PRAGMA foreign_keys = ON;

-- 1. Users (Admin Auth)
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Client Intake Records
CREATE TABLE IF NOT EXISTS client_intakes (
    id TEXT PRIMARY KEY,
    business_name TEXT NOT NULL,
    business_email TEXT NOT NULL,
    website_url TEXT,
    service_regions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Client Offers (Pricing, Tiers, Positioning)
CREATE TABLE IF NOT EXISTS client_offers (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    service_name TEXT NOT NULL,
    price REAL NOT NULL,
    ideal_buyer TEXT,
    objection_scripts TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 4. Client Social Accounts Configuration
CREATE TABLE IF NOT EXISTS client_social_accounts (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    platform TEXT CHECK(platform IN ('instagram', 'facebook', 'whatsapp', 'threads')) NOT NULL,
    handle TEXT NOT NULL,
    facebook_page_id TEXT,
    ai_should_reply_comments INTEGER DEFAULT 1,
    ai_should_reply_dms INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 5. Client Brand Voice Rules
CREATE TABLE IF NOT EXISTS client_brand_voice (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    voice_traits TEXT NOT NULL, -- JSON/Comma-separated (e.g. Friendly, warm, motivational)
    phrases_to_avoid TEXT NOT NULL, -- JSON/Comma-separated (e.g. "credit sweep", "guarantees")
    ai_speaks_as TEXT NOT NULL, -- e.g. "Jordynn's AI assistant" or "Jordynn Miller"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 6. Client Automation & Follow-Up Configuration
CREATE TABLE IF NOT EXISTS client_automation_rules (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    dm_escalation_triggers TEXT NOT NULL, -- JSON/Comma-separated keywords
    followup_cadence TEXT DEFAULT '1,3,5,8,12,16,18', -- Day offsets
    followup_message_1 TEXT,
    followup_message_2 TEXT,
    followup_message_3 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 7. Client Compliance & Launch Status (Launch Gate)
CREATE TABLE IF NOT EXISTS client_compliance_launch (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    launch_approval_status TEXT CHECK(launch_approval_status IN ('approved', 'shadow_mode', 'paused')) DEFAULT 'shadow_mode',
    approved_ai_disclosure_script TEXT,
    require_ai_disclosure_dms INTEGER DEFAULT 1,
    can_say_guaranteed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 8. Lead Directory (One row per unique prospect)
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    lead_state TEXT CHECK(lead_state IN ('NEW', 'QUALIFIED', 'VAFOLLOWUP', 'LINK_SENT', 'BOOKED', 'ASSIGN', 'COLLAB', 'DQ', 'ACTIVE_CLIENT')) DEFAULT 'NEW',
    platform TEXT CHECK(platform IN ('instagram', 'facebook', 'whatsapp', 'threads', 'meta_leadgen')) NOT NULL,
    platform_user_id TEXT,               -- NULL allowed for leadgen form submissions (no PSID)
    name TEXT,
    email TEXT,                          -- Captured from leadgen forms and DM parsing
    phone TEXT,                          -- Captured from leadgen forms and DM parsing
    service_needed TEXT, -- e.g. "credit_repair" or "business_funding"
    credit_goal TEXT,
    timeline TEXT,
    lead_score REAL DEFAULT 0.0,
    bankruptcy INTEGER DEFAULT 0, -- 1 = Yes, 0 = No
    child_support INTEGER DEFAULT 0, -- 1 = Yes, 0 = No
    collections_count INTEGER DEFAULT 0,
    paused_until TIMESTAMP, -- Handoff mute timestamp
    follow_up_step INTEGER DEFAULT 0, -- Progress tracker in nurture sequence [0-7]
    last_contact_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE,
    UNIQUE(intake_id, platform, platform_user_id)
);

-- 9. Chat Conversations
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    lead_id TEXT NOT NULL,
    platform TEXT CHECK(platform IN ('instagram', 'facebook', 'whatsapp', 'threads')) NOT NULL,
    bot_active INTEGER DEFAULT 1, -- 1 = Bot responds, 0 = Paused / Human takeover
    within_24h_window INTEGER DEFAULT 1, -- 1 = within Meta 24h messaging window, 0 = expired
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

-- 10. Chat Message Interactions
CREATE TABLE IF NOT EXISTS interactions (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    sender_type TEXT CHECK(sender_type IN ('user', 'bot', 'human')) NOT NULL,
    platform_message_id TEXT,
    message_text TEXT NOT NULL,
    sentiment_score REAL DEFAULT 0.0,
    compliance_flag INTEGER DEFAULT 0, -- 1 = Violates policy, 0 = Clear
    compliance_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- 11. Comment Moderation Logs
CREATE TABLE IF NOT EXISTS comment_logs (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    platform TEXT CHECK(platform IN ('instagram', 'facebook')) NOT NULL,
    comment_id TEXT NOT NULL UNIQUE,
    post_id TEXT NOT NULL,
    username TEXT,
    message_text TEXT NOT NULL,
    action_taken TEXT CHECK(action_taken IN ('none', 'hidden', 'deleted', 'replied')) DEFAULT 'none',
    action_reason TEXT,
    reply_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 12. Human Escalation Handoff Records
CREATE TABLE IF NOT EXISTS escalations (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    trigger_message TEXT NOT NULL,
    sms_sent INTEGER DEFAULT 0, -- 1 = SMS sent to Jordynn, 0 = pending/failed
    sms_status TEXT,
    human_resolved INTEGER DEFAULT 0, -- 1 = Resolved, 0 = Active
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

-- 13. Follow-up Nurture Sequence Progress
CREATE TABLE IF NOT EXISTS follow_ups (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    message_text TEXT NOT NULL,
    scheduled_for TIMESTAMP NOT NULL,
    sent INTEGER DEFAULT 0, -- 1 = Sent, 0 = Pending/Skipped
    sent_at TIMESTAMP,
    skipped_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

-- 14. CRM GoHighLevel Sync Logs
CREATE TABLE IF NOT EXISTS ghl_sync_log (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    ghl_contact_id TEXT,
    sync_status TEXT CHECK(sync_status IN ('success', 'failed', 'pending')) DEFAULT 'pending',
    error_message TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

-- 15. Whitelisted Approved Links
CREATE TABLE IF NOT EXISTS approved_links (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    label TEXT NOT NULL,
    url TEXT NOT NULL,
    use_case TEXT,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 16. Disqualification Rules (DQ Criteria)
CREATE TABLE IF NOT EXISTS dq_rules (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    rule_type TEXT NOT NULL, -- e.g. "bankruptcy", "child_support", "collections"
    criteria TEXT NOT NULL, -- Threshold rules
    action TEXT DEFAULT 'disqualify',
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- 17. Reusable Media Assets (Images, Voice Clips)
CREATE TABLE IF NOT EXISTS media_assets (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    asset_key TEXT NOT NULL,
    media_type TEXT CHECK(media_type IN ('image', 'audio', 'video')) NOT NULL,
    caption TEXT,
    url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE
);

-- =====================================================================
-- PERFORMANCE INDICES FOR MASS SCALE & COMPLEX FILTERS
-- =====================================================================
CREATE INDEX IF NOT EXISTS idx_leads_intake_state ON leads(intake_id, lead_state);
CREATE INDEX IF NOT EXISTS idx_leads_platform_user ON leads(platform, platform_user_id);
CREATE INDEX IF NOT EXISTS idx_leads_paused_until ON leads(paused_until);
CREATE INDEX IF NOT EXISTS idx_conversations_lead ON conversations(lead_id);
CREATE INDEX IF NOT EXISTS idx_interactions_conv ON interactions(conversation_id);
CREATE INDEX IF NOT EXISTS idx_interactions_conv_created ON interactions(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_comment_logs_intake ON comment_logs(intake_id, comment_id);
CREATE INDEX IF NOT EXISTS idx_escalations_lead ON escalations(lead_id, human_resolved);
CREATE INDEX IF NOT EXISTS idx_follow_ups_lead ON follow_ups(lead_id, step_number);
CREATE INDEX IF NOT EXISTS idx_approved_links_active ON approved_links(intake_id, active);
