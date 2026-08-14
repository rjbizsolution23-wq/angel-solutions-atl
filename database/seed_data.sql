-- =====================================================================
-- ANGEL SOLUTIONS ATL - SEED DATA DEFINITIONS
-- =====================================================================
-- Target Database: Cloudflare D1 (SQLite)
-- Version: 1.0.0
-- Client Intake ID: 6a46c0696b95e7dc9dd6251c (Angel Solutions ATL)
-- =====================================================================

-- 1. Insert Client Intake
INSERT INTO client_intakes (id, business_name, business_email, website_url, service_regions)
VALUES (
    '6a46c0696b95e7dc9dd6251c',
    'Angel Solutions ATL',
    'jordynn@angelsolutionsatl.com',
    'https://angelsolutionsatl.com',
    'National (USA)'
) ON CONFLICT(id) DO UPDATE SET
    business_name=excluded.business_name,
    business_email=excluded.business_email,
    website_url=excluded.website_url;

-- 2. Insert Client Offers
INSERT INTO client_offers (id, intake_id, service_name, price, ideal_buyer, objection_scripts)
VALUES 
(
    'offer_67_skool',
    '6a46c0696b95e7dc9dd6251c',
    'Credit Repair Monthly (Skool Community)',
    67.0,
    'Not in a rush, DIY-minded, low collections count (<10), no bankruptcy/child support, wants interactive community disputes.',
    'Objection: "Too expensive." Script: "Our monthly program is only $67/mo (less than $2.25/day) which gives you up to 5 dispute letters every single month and a community supporting you."'
),
(
    'offer_795_advanced',
    '6a46c0696b95e7dc9dd6251c',
    'Advanced Credit Restoral (1-on-1)',
    795.0,
    'Urgent timeline (<=60 days), business owner blocked from funding, needs active legal dispute intervention and 1-on-1 calls.',
    'Objection: "I want a guarantee." Script: "Legally, credit repair companies cannot guarantee specific score increases. But our 1-on-1 team disputes all collections simultaneously using legal channels to get rapid results."'
)
ON CONFLICT(id) DO NOTHING;

-- 3. Insert Client Social Accounts
INSERT INTO client_social_accounts (id, intake_id, platform, handle, facebook_page_id, ai_should_reply_comments, ai_should_reply_dms)
VALUES 
(
    'social_ig_angel',
    '6a46c0696b95e7dc9dd6251c',
    'instagram',
    'jordynnpatrice',
    NULL,
    1,
    1
),
(
    'social_fb_page',
    '6a46c0696b95e7dc9dd6251c',
    'facebook',
    'Angel Solutions ATL',
    '107318795356062',
    1,
    1
)
ON CONFLICT(id) DO NOTHING;

-- 4. Insert Brand Voice
INSERT INTO client_brand_voice (id, intake_id, voice_traits, phrases_to_avoid, ai_speaks_as)
VALUES (
	'voice_angel',
	'6a46c0696b95e7dc9dd6251c',
	'friendly, warm, premium, professional, expert, motivational, direct',
	'credit sweep, guarantee, guaranteed, best, yo, bet',
	'Jordynn Miller'
)
ON CONFLICT(id) DO NOTHING;

-- 5. Insert Automation Rules
INSERT INTO client_automation_rules (id, intake_id, dm_escalation_triggers, followup_cadence, followup_message_1, followup_message_2, followup_message_3)
VALUES (
    'rules_angel',
    '6a46c0696b95e7dc9dd6251c',
    'refund, scam, lawyer, attorney, court, sue, lawsuit, fraud, call me, speak to human',
    '1,3,5,8,12,16,18',
    'Hey! Just checking in on you. Were you able to review the credit solutions link I sent over yesterday?',
    'Hey, I know life gets super busy! Just wanted to see if you had any questions on how we dispute collections for you?',
    'Happy Friday! Our dispute team has open slots for next week. If you are ready to clear those credit roadblocks, let me know!'
)
ON CONFLICT(id) DO NOTHING;

-- 6. Insert Compliance & Launch Settings
INSERT INTO client_compliance_launch (id, intake_id, launch_approval_status, approved_ai_disclosure_script, require_ai_disclosure_dms, can_say_guaranteed)
VALUES (
    'launch_angel',
    '6a46c0696b95e7dc9dd6251c',
    'approved', -- Bot is live and actively sending messages
    'Hey! Jordynn here. I am here to help you quickly pre-qualify and answer any credit repair or business funding questions you have!',
    1,
    0
)
ON CONFLICT(id) DO NOTHING;

-- 7. Insert Approved Links
INSERT INTO approved_links (id, intake_id, label, url, use_case, active)
VALUES 
(
    'link_skool',
    '6a46c0696b95e7dc9dd6251c',
    'Skool Credit Solution Community',
    'https://www.skool.com/creditsolution/about',
    'Used for leads wanting DIY, low budget, or the $67/mo monthly tier.',
    1
),
(
    'link_booking',
    '6a46c0696b95e7dc9dd6251c',
    'Discovery Consultation Booking',
    'https://angelsolutionsatl.com/book-online',
    'Used for advanced leads wanting 1-on-1 full service starting from $795.',
    1
),
(
    'link_website',
    '6a46c0696b95e7dc9dd6251c',
    'Main Official Website',
    'https://angelsolutionsatl.com',
    'General educational and information requests.',
    1
),
(
    'link_reviews',
    '6a46c0696b95e7dc9dd6251c',
    'Google Success Reviews',
    'https://share.google/FTVB6seubNwgSVDnd',
    'Social proof requests and case studies.',
    1
)
ON CONFLICT(id) DO NOTHING;

-- 8. Insert Disqualification Rules
INSERT INTO dq_rules (id, intake_id, rule_type, criteria, action, active)
VALUES 
(
    'dq_bankruptcy',
    '6a46c0696b95e7dc9dd6251c',
    'bankruptcy',
    'active',
    'disqualify_to_manual',
    1
),
(
    'dq_child_support',
    '6a46c0696b95e7dc9dd6251c',
    'child_support',
    'arrears_active',
    'disqualify_to_manual',
    1
),
(
    'dq_collections',
    '6a46c0696b95e7dc9dd6251c',
    'collections',
    '>= 10',
    'route_to_advanced',
    1
)
ON CONFLICT(id) DO NOTHING;

-- 9. Create Default Admin User
-- Password: "ChangeThisPassword123!" (Using pbkdf2_sha256 format for reference/mock check)
INSERT INTO users (id, email, password_hash, role)
VALUES (
    'usr_admin_01',
    'admin@angelsolutionsatl.com',
    'pbkdf2_sha256$260000$mock_salt$f2824df9ea0b15b3c37254bd03923c58bdf03b4142f361251e604f3bb9b7a372',
    'admin'
) ON CONFLICT(email) DO NOTHING;
