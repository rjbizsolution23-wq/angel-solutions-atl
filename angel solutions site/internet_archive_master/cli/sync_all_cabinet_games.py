import sys
import os
import json
import urllib.parse
import requests

BASE44_API_KEY = "e3bf3c7cc79044f58d69edfa2a2a7e63"
BASE44_APP_ID = "6a51e1fe45074c4d50be5dea"
BASE44_API_URL = f"https://app.base44.com/api/apps/{BASE44_APP_ID}"

headers = {
    "api_key": BASE44_API_KEY,
    "Content-Type": "application/json"
}

PLATFORMS = {
    "nes": {
        "retro_platform": "nes",
        "game_platform": "NES",
        "core": "nes",
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=600&auto=format&fit=crop"
    },
    "snes": {
        "retro_platform": "snes",
        "game_platform": "SNES",
        "core": "snes",
        "cover": "https://images.unsplash.com/photo-1612287230202-1bf1d85d1bdf?q=80&w=600&auto=format&fit=crop"
    },
    "genesis": {
        "retro_platform": "genesis",
        "game_platform": "Genesis",
        "core": "segaMD",
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=600&auto=format&fit=crop"
    },
    "gba": {
        "retro_platform": "gba",
        "game_platform": "GameBoy",
        "core": "gba",
        "cover": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600&auto=format&fit=crop"
    }
}

def make_proxy_url(url):
    prefix = "https://archive.org/download/"
    if url.startswith(prefix):
        subpath = url[len(prefix):]
        parts = subpath.split("/", 1)
        if len(parts) == 2:
            identifier = parts[0]
            filename = urllib.parse.unquote(parts[1])
            quoted_file = urllib.parse.quote(filename)
            return f"https://prometheus-cloudflare-backend.rickjefferson.workers.dev/api/games/proxy?id={identifier}&file={quoted_file}"
    return url

# Append internet_archive_master directory to sys.path so we can import from cli
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
try:
    from cli.install_rpgs import rpg_database
except ImportError:
    # Fallback to loading the file manually if import fails
    print("Direct import failed. Reading file manually...")
    rpg_database = []

def get_existing_entities(entity_name):
    url = f"{BASE44_API_URL}/entities/{entity_name}"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return []
    except Exception as e:
        print(f"Error fetching {entity_name}: {e}")
        return []

def clean_duplicates(title):
    for entity in ["RetroGame", "Game"]:
        url = f"{BASE44_API_URL}/entities/{entity}"
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                for item in r.json():
                    if item.get("title", "").strip().lower() == title.strip().lower():
                        del_url = f"{url}/{item['id']}"
                        requests.delete(del_url, headers=headers)
                        print(f" -> Purged duplicate {entity} record for '{title}'")
        except Exception as e:
            print(f" -> Error cleaning duplicates for '{title}': {e}")

def sync_games():
    print("====================================================")
    print("🚀 BASE44 DATABASE SYNCHRONIZER - RETRO CABINET 🚀")
    print("====================================================\n")
    
    if not rpg_database:
        print("[!] No games loaded from install_rpgs.py. Exiting.")
        return
        
    print(f"Loaded {len(rpg_database)} total games from master catalog.\n")
    
    synced_count = 0
    for i, g in enumerate(rpg_database, 1):
        title = g["title"]
        platform = g["platform"]
        year = g["year"]
        developer = g["developer"]
        description = g["description"]
        raw_url = g["url"]
        
        cfg = PLATFORMS.get(platform)
        if not cfg:
            print(f"[{i}/{len(rpg_database)}] Unknown platform '{platform}' for '{title}'. Skipping.")
            continue
            
        print(f"[{i}/{len(rpg_database)}] Syncing: '{title}' ({platform.upper()})")
        
        # 1. Clean existing records to avoid duplicate IDs/corruption
        clean_duplicates(title)
        
        # 2. Formulate correct edge-proxied streaming URL
        proxied_url = make_proxy_url(raw_url)
        print(f" -> Edge Proxy URL: {proxied_url}")
        
        # 3. Create RetroGame Payload
        retro_payload = {
            "title": title,
            "description": description,
            "platform": cfg["retro_platform"],
            "rom_url": proxied_url,
            "emulator_core": cfg["core"],
            "cover_image_url": cfg["cover"],
            "genre": "RPG" if "Dragon Ball" not in title else "Fighting",
            "year": int(year),
            "developer": developer,
            "save_state_enabled": True,
            "is_embedded": True,
            "source": "internet_archive"
        }
        
        # 4. Create Game Payload
        game_payload = {
            "title": title,
            "platform": cfg["game_platform"],
            "genre": "RPG" if "Dragon Ball" not in title else "Fighting",
            "year": int(year),
            "developer": developer,
            "rom_file_url": proxied_url,
            "cover_art_url": cfg["cover"],
            "description": description,
            "rating": 5.0,
            "is_favorite": True,
            "favorites": 0,
            "play_count": 0
        }
        
        # 5. POST to Base44 app backend
        r_rg = requests.post(f"{BASE44_API_URL}/entities/RetroGame", json=retro_payload, headers=headers)
        r_g = requests.post(f"{BASE44_API_URL}/entities/Game", json=game_payload, headers=headers)
        
        if r_rg.status_code in [200, 201] and r_g.status_code in [200, 201]:
            print(f" -> Successfully synced '{title}' to Base44 app backend!")
            synced_count += 1
        else:
            print(f" -> [FAIL] Sync status: RetroGame={r_rg.status_code}, Game={r_g.status_code}")
            
    print(f"\n🚀 Database Synchronization Complete! Synced {synced_count}/{len(rpg_database)} items.")

if __name__ == "__main__":
    sync_games()
