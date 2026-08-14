-- =====================================================================
-- ANGEL SOLUTIONS ATL - D1 DATABASE EXTENSION FOR META ADS TRACKING
-- =====================================================================

CREATE TABLE IF NOT EXISTS meta_campaigns (
    id TEXT PRIMARY KEY, -- Meta's campaign ID
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    objective TEXT,
    budget REAL DEFAULT 0.0,
    spend REAL DEFAULT 0.0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
