-- 🎮 RJ VAULT FLOW - COMPLETE SQL DATABASE STRUCTURE
-- Target App ID: 6a51e1fe45074c4d50be5dea
-- Created exclusively for Rick Jefferson | RJ Business Solutions

-- 1. games Table (Curated Vintage Catalog)
CREATE TABLE IF NOT EXISTS games (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  title TEXT NOT NULL,
  platform TEXT NOT NULL CHECK (platform IN ('NES', 'SNES', 'Genesis', 'PlayStation', 'N64', 'GameBoy', 'GameBoy Color', 'GameBoy Advance', 'Dreamcast', 'Arcade', 'Atari', 'Other')),
  genre TEXT CHECK (genre IN ('Action', 'Adventure', 'RPG', 'Sports', 'Racing', 'Puzzle', 'Fighting', 'Shooter', 'Strategy', 'Simulation')),
  year INTEGER,
  publisher TEXT,
  developer TEXT,
  rom_file_url TEXT NOT NULL, -- Direct Cloudflare R2 binary cache URL
  cover_art_url TEXT,         -- Thumbnail cover image
  screenshots TEXT,           -- JSON array of screenshot URLs
  description TEXT,
  rating REAL DEFAULT 0.0 CHECK (rating >= 0.0 AND rating <= 5.0),
  play_count INTEGER DEFAULT 0,
  favorites INTEGER DEFAULT 0,
  tags TEXT,                  -- Comma-separated or JSON array list
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. game_projects Table (AI Generative Game Studio builds)
CREATE TABLE IF NOT EXISTS game_projects (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  user_id TEXT NOT NULL,
  project_name TEXT NOT NULL,
  game_idea TEXT,
  platform TEXT CHECK (platform IN ('Unity', 'Godot', 'Phaser', 'Pygame', 'HTML5')),
  status TEXT DEFAULT 'Planning' CHECK (status IN ('Planning', 'In Development', 'Testing', 'Published')),
  generated_specification TEXT, -- Detailed MD architecture document
  code_files TEXT,              -- JSON containing complete Phaser sources
  asset_prompts TEXT,           -- JSON showing sprite prompt maps
  build_url TEXT,               -- Subdomain link of generated iframe sandboxes
  github_repo TEXT,
  total_cost REAL DEFAULT 0.0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. collections Table (White-Labeled Custom Playlists)
CREATE TABLE IF NOT EXISTS collections (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  user_id TEXT NOT NULL,
  collection_name TEXT NOT NULL,
  game_ids TEXT,               -- JSON array string of contained Game IDs
  is_public INTEGER DEFAULT 0,  -- 0 = False, 1 = True
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. game_assets Table (Sprites, Textures, Sound FX, and Voice tracks)
CREATE TABLE IF NOT EXISTS game_assets (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  asset_name TEXT NOT NULL,
  asset_type TEXT NOT NULL CHECK (asset_type IN ('sprite', 'background', 'audio', 'code', 'ui')),
  file_url TEXT NOT NULL,
  thumbnail_url TEXT,
  dimensions TEXT,
  file_size INTEGER DEFAULT 0,
  file_format TEXT,
  tags TEXT,
  ai_generated INTEGER DEFAULT 1,
  ai_prompt TEXT,
  game_id TEXT,                 -- Connected Game or Project ID
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. ai_generation_history Table (Token usages and prompt logs)
CREATE TABLE IF NOT EXISTS ai_generation_history (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  user_id TEXT NOT NULL,
  generation_type TEXT NOT NULL CHECK (generation_type IN ('code', 'sprite', 'sound_fx', 'spec')),
  input_prompt TEXT NOT NULL,
  token_usage INTEGER DEFAULT 0,
  service_used TEXT NOT NULL,   -- OpenRouter, ElevenLabs, FLUX.1
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 6. job_logs Table (Durable execution task traces)
CREATE TABLE IF NOT EXISTS job_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  agent_type TEXT NOT NULL,
  params TEXT,
  success INTEGER NOT NULL CHECK (success IN (0, 1)),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for Lightning Fast Searches
CREATE INDEX IF NOT EXISTS idx_games_title ON games(title);
CREATE INDEX IF NOT EXISTS idx_games_platform ON games(platform);
CREATE INDEX IF NOT EXISTS idx_game_projects_user ON game_projects(user_id);
CREATE INDEX IF NOT EXISTS idx_collections_user ON collections(user_id);
CREATE INDEX IF NOT EXISTS idx_game_assets_game ON game_assets(game_id);
