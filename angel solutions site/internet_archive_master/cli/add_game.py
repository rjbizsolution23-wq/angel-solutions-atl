import sys
import json
import urllib.parse
import urllib.request
import requests

BASE44_API_KEY = "e3bf3c7cc79044f58d69edfa2a2a7e63"
BASE44_APP_ID = "6a51e1fe45074c4d50be5dea"
BASE44_API_URL = f"https://app.base44.com/api/apps/{BASE44_APP_ID}"

headers = {
    "api_key": BASE44_API_KEY,
    "Content-Type": "application/json"
}

PLATFORM_CONFIG = {
    "nes": {
        "retrogame_platform": "nes",
        "game_platform": "NES",
        "emulator_core": "nes",
        "extensions": [".nes", ".zip"],
        "default_genre": "Platformer",
        "default_dev": "Nintendo",
        "cover_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=600&auto=format&fit=crop"
    },
    "snes": {
        "retrogame_platform": "snes",
        "game_platform": "SNES",
        "emulator_core": "snes",
        "extensions": [".smc", ".sfc", ".zip"],
        "default_genre": "Platformer",
        "default_dev": "Nintendo",
        "cover_url": "https://images.unsplash.com/photo-1612287230202-1bf1d85d1bdf?q=80&w=600&auto=format&fit=crop"
    },
    "genesis": {
        "retrogame_platform": "genesis",
        "game_platform": "Genesis",
        "emulator_core": "segaMD",
        "extensions": [".bin", ".md", ".smd", ".gen", ".zip"],
        "default_genre": "Action",
        "default_dev": "Sega",
        "cover_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=600&auto=format&fit=crop"
    },
    "gba": {
        "retrogame_platform": "gba",
        "game_platform": "GameBoy",
        "emulator_core": "gba",
        "extensions": [".gba", ".zip"],
        "default_genre": "RPG",
        "default_dev": "Game Freak",
        "cover_url": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=600&auto=format&fit=crop"
    }
}

def search_ia(query, platform):
    print(f"[*] Querying Internet Archive for: '{query}' on console '{platform}'...")
    cfg = PLATFORM_CONFIG[platform]
    
    # Target search query
    query_str = f'title:("{query}") AND format:(ROM OR "ZIP" OR "NES" OR "SMC" OR "SFC" OR "GBA")'
    params = {
        "q": query_str,
        "fl[]": "identifier,title",
        "output": "json",
        "rows": 10
    }
    
    encoded_params = urllib.parse.urlencode(params)
    search_url = f"https://archive.org/advancedsearch.php?{encoded_params}"
    
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            docs = data.get("response", {}).get("docs", [])
            return docs
    except Exception as e:
        print(f"[!] IA Search failed: {e}")
        return []

def get_ia_files(identifier, platform):
    url = f"https://archive.org/metadata/{identifier}"
    cfg = PLATFORM_CONFIG[platform]
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            files = data.get("files", [])
            
            # Filter matching extensions
            rom_files = []
            for f in files:
                name = f.get("name", "")
                if any(name.lower().endswith(ext) for ext in cfg["extensions"]):
                    # Ignore manuals, text, images, corrupt files
                    if not any(x in name.lower() for x in ["manual", "boxart", "image", "txt", "cheat"]):
                        rom_files.append(name)
            return rom_files
    except Exception as e:
        print(f"[!] Failed fetching metadata for {identifier}: {e}")
        return []

def add_game(query, platform):
    platform = platform.lower()
    if platform not in PLATFORM_CONFIG:
        print(f"[!] Error: Supported platforms are {list(PLATFORM_CONFIG.keys())}")
        return
        
    cfg = PLATFORM_CONFIG[platform]
    docs = search_ia(query, platform)
    
    if not docs:
        print("[!] No matching collections found on Internet Archive.")
        return
        
    # Walk docs and look for matching files
    for doc in docs:
        identifier = doc["identifier"]
        title = doc["title"]
        files = get_ia_files(identifier, platform)
        
        if files:
            # Pick the first suitable file
            target_file = files[0]
            encoded_file = urllib.parse.quote(target_file)
            download_url = f"https://archive.org/download/{identifier}/{encoded_file}"
            
            print(f"\n[+] Match Found!")
            print(f"    Identifier: {identifier}")
            print(f"    Collection Title: {title}")
            print(f"    Target File: {target_file}")
            print(f"    Download Stream URL: {download_url}")
            
            # Post to Base44
            clean_title = query.title()
            
            retro_payload = {
                "title": clean_title,
                "description": f"Classic {clean_title} played instantly in the browser.",
                "platform": cfg["retrogame_platform"],
                "rom_url": download_url,
                "emulator_core": cfg["emulator_core"],
                "cover_image_url": cfg["cover_url"],
                "genre": cfg["default_genre"],
                "year": 1995,
                "developer": cfg["default_dev"],
                "save_state_enabled": True,
                "is_embedded": True,
                "source": "internet_archive"
            }
            
            game_payload = {
                "title": clean_title,
                "platform": cfg["game_platform"],
                "genre": cfg["default_genre"],
                "year": 1995,
                "developer": cfg["default_dev"],
                "rom_file_url": download_url,
                "cover_art_url": cfg["cover_url"],
                "description": f"Classic {clean_title} played instantly in the browser.",
                "rating": 5,
                "is_favorite": True
            }
            
            print("\n[*] Synchronizing records to Base44 Cloud...")
            r_rg = requests.post(f"{BASE44_API_URL}/entities/RetroGame", json=retro_payload, headers=headers)
            r_g = requests.post(f"{BASE44_API_URL}/entities/Game", json=game_payload, headers=headers)
            
            print(f"[RetroGame] Server response: {r_rg.status_code}")
            print(f"[Game] Server response: {r_g.status_code}")
            
            print(f"\n🚀 SUCCESS! '{clean_title}' added and immediately available in your cabinet!")
            return
            
    print("[!] No clean playable files found in any matching collections.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 add_game.py \"[Game Name]\" [nes/snes/genesis/gba]")
        sys.exit(1)
        
    game_name = sys.argv[1]
    console = sys.argv[2]
    add_game(game_name, console)
