-- Migration to add website platform support and email/phone columns
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS leads;

CREATE TABLE leads (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    lead_state TEXT CHECK(lead_state IN ('NEW', 'QUALIFIED', 'VAFOLLOWUP', 'LINK_SENT', 'BOOKED', 'ASSIGN', 'COLLAB', 'DQ', 'ACTIVE_CLIENT')) DEFAULT 'NEW',
    platform TEXT CHECK(platform IN ('instagram', 'facebook', 'whatsapp', 'threads', 'website')) NOT NULL,
    platform_user_id TEXT NOT NULL,
    name TEXT,
    service_needed TEXT,
    email TEXT,
    phone TEXT,
    credit_goal TEXT,
    timeline TEXT,
    lead_score REAL DEFAULT 0.0,
    bankruptcy INTEGER DEFAULT 0,
    child_support INTEGER DEFAULT 0,
    collections_count INTEGER DEFAULT 0,
    paused_until TIMESTAMP,
    follow_up_step INTEGER DEFAULT 0,
    last_contact_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE,
    UNIQUE(intake_id, platform, platform_user_id)
);

CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    intake_id TEXT NOT NULL,
    lead_id TEXT NOT NULL,
    platform TEXT CHECK(platform IN ('instagram', 'facebook', 'whatsapp', 'threads', 'website')) NOT NULL,
    bot_active INTEGER DEFAULT 1,
    within_24h_window INTEGER DEFAULT 1,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intake_id) REFERENCES client_intakes(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

PRAGMA foreign_keys = ON;
