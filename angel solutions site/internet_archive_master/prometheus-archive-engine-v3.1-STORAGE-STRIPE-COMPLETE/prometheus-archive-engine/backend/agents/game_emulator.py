"""
Game & Emulator Getter Agent
Discovers, downloads, and packages retro games with emulators
"""
import asyncio
import logging
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import zipfile

logger = logging.getLogger(__name__)


# Platform-to-Emulator mapping
EMULATOR_MAP = {
    'nes': {
        'name': 'RetroArch (FCEUmm)',
        'core': 'fceumm',
        'extensions': ['.nes'],
        'ia_collection': 'consolelivingroom'
    },
    'snes': {
        'name': 'RetroArch (Snes9x)',
        'core': 'snes9x',
        'extensions': ['.smc', '.sfc'],
        'ia_collection': 'consolelivingroom'
    },
    'genesis': {
        'name': 'RetroArch (Genesis Plus GX)',
        'core': 'genesis_plus_gx',
        'extensions': ['.md', '.bin'],
        'ia_collection': 'consolelivingroom'
    },
    'gameboy': {
        'name': 'RetroArch (Gambatte)',
        'core': 'gambatte',
        'extensions': ['.gb', '.gbc'],
        'ia_collection': 'consolelivingroom'
    },
    'arcade': {
        'name': 'RetroArch (MAME)',
        'core': 'mame',
        'extensions': ['.zip'],
        'ia_collection': 'internetarcade'
    },
    'dos': {
        'name': 'DOSBox-X',
        'core': 'dosbox',
        'extensions': ['.exe', '.com', '.bat'],
        'ia_collection': 'softwarelibrary_msdos_games'
    }
}

GAME_COLLECTIONS = {
    'arcade': 'internetarcade',
    'console': 'consolelivingroom',
    'dos': 'softwarelibrary_msdos_games',
    'windows': 'softwarelibrary_win3_games',
    'c64': 'softwarelibrary_c64',
    'amiga': 'softwarelibrary_amiga'
}


@dataclass
class GamePackage:
    identifier: str
    title: str
    platform: str
    year: Optional[int]
    publisher: str
    genre: str
    description: str
    rom_files: List[str]
    screenshot_urls: List[str]


@dataclass
class GameBundle:
    name: str
    description: str
    platform: str
    games: List[GamePackage]
    emulator_info: Dict
    total_size_mb: float


class GameEmulatorAgent:
    """
    Autonomous agent for retro game collection and emulator packaging
    
    Features:
    - Search IA game collections
    - Download ROMs and disk images
    - Match with appropriate emulators
    - Create ready-to-play bundles
    - Generate documentation
    """
    
    def __init__(self, ia_client):
        self.ia = ia_client
    
    async def search_games(
        self,
        platform: str,
        genre: Optional[str] = None,
        year_range: Optional[tuple] = None,
        max_results: int = 50
    ) -> List[Dict]:
        """
        Search Internet Archive for games
        
        Args:
            platform: Platform (nes, snes, genesis, arcade, dos, etc.)
            genre: Genre filter (action, rpg, puzzle, etc.)
            year_range: (min_year, max_year)
            max_results: Maximum results
        """
        logger.info(f"Searching games: platform={platform}, genre={genre}")
        
        # Get collection for platform
        collection = GAME_COLLECTIONS.get(platform.lower())
        if not collection:
            # Try platform-specific mapping
            emulator_info = EMULATOR_MAP.get(platform.lower())
            if emulator_info:
                collection = emulator_info['ia_collection']
            else:
                raise ValueError(f"Unknown platform: {platform}")
        
        # Build search query
        search_parts = [f"collection:{collection}"]
        
        if genre:
            search_parts.append(f"subject:({genre})")
        
        if year_range:
            search_parts.append(f"year:[{year_range[0]} TO {year_range[1]}]")
        
        search_query = " AND ".join(search_parts)
        
        # Execute search
        results = await asyncio.to_thread(
            self.ia.search_items,
            search_query,
            fields=['identifier', 'title', 'creator', 'year', 'subject', 'description'],
            max_results=max_results
        )
        
        games = []
        for result in results:
            games.append({
                'identifier': result.get('identifier'),
                'title': result.get('title', 'Unknown'),
                'publisher': result.get('creator', ['Unknown'])[0] if result.get('creator') else 'Unknown',
                'year': result.get('year'),
                'subjects': result.get('subject', []),
                'description': result.get('description', '')
            })
        
        logger.info(f"Found {len(games)} games")
        return games
    
    async def download_game(self, identifier: str, dest_dir: str = "/tmp") -> GamePackage:
        """Download game files from Internet Archive"""
        logger.info(f"Downloading game: {identifier}")
        
        item = await asyncio.to_thread(self.ia.get_item, identifier)
        metadata = item.metadata
        
        # Identify ROM files
        rom_files = []
        for file in item.files:
            name = file['name']
            # Common ROM extensions
            if any(name.endswith(ext) for ext in ['.zip', '.nes', '.smc', '.sfc', '.md', '.bin', '.gb', '.gbc', '.n64', '.iso']):
                rom_files.append(name)
        
        # Download ROM files
        if rom_files:
            await asyncio.to_thread(item.download, files=rom_files, destdir=dest_dir)
        
        # Get screenshots
        screenshot_urls = []
        for file in item.files:
            if file['name'].endswith(('.png', '.jpg', '.gif')) and 'screenshot' in file['name'].lower():
                screenshot_urls.append(f"https://archive.org/download/{identifier}/{file['name']}")
        
        package = GamePackage(
            identifier=identifier,
            title=metadata.get('title', 'Unknown'),
            platform=self._detect_platform(metadata, rom_files),
            year=metadata.get('year'),
            publisher=metadata.get('creator', ['Unknown'])[0] if metadata.get('creator') else 'Unknown',
            genre=metadata.get('subject', ['Unknown'])[0] if metadata.get('subject') else 'Unknown',
            description=metadata.get('description', ''),
            rom_files=rom_files,
            screenshot_urls=screenshot_urls
        )
        
        logger.info(f"Downloaded: {package.title} ({len(rom_files)} files)")
        return package
    
    def _detect_platform(self, metadata: Dict, rom_files: List[str]) -> str:
        """Detect platform from metadata and file extensions"""
        # Check subjects
        subjects = [s.lower() for s in metadata.get('subject', [])]
        
        platform_keywords = {
            'nes': ['nes', 'nintendo entertainment system'],
            'snes': ['snes', 'super nintendo'],
            'genesis': ['genesis', 'mega drive', 'sega genesis'],
            'gameboy': ['game boy', 'gameboy'],
            'arcade': ['arcade', 'mame'],
            'dos': ['dos', 'ms-dos']
        }
        
        for platform, keywords in platform_keywords.items():
            if any(keyword in ' '.join(subjects) for keyword in keywords):
                return platform
        
        # Check file extensions
        for rom_file in rom_files:
            if rom_file.endswith('.nes'):
                return 'nes'
            elif rom_file.endswith(('.smc', '.sfc')):
                return 'snes'
            elif rom_file.endswith(('.md', '.bin')):
                return 'genesis'
            elif rom_file.endswith(('.gb', '.gbc')):
                return 'gameboy'
        
        return 'unknown'
    
    async def get_emulator_info(self, platform: str) -> Dict:
        """Get emulator information for platform"""
        emulator = EMULATOR_MAP.get(platform.lower())
        if not emulator:
            raise ValueError(f"No emulator mapping for platform: {platform}")
        
        return {
            'platform': platform,
            'emulator_name': emulator['name'],
            'core': emulator['core'],
            'download_url': f"https://www.retroarch.com/index.php?page=platforms",  # Generic RetroArch download
            'setup_instructions': self._generate_setup_instructions(platform, emulator)
        }
    
    def _generate_setup_instructions(self, platform: str, emulator: Dict) -> str:
        """Generate setup instructions for emulator"""
        return f"""# {emulator['name']} Setup Instructions

## Installation
1. Download RetroArch from: https://www.retroarch.com/
2. Install RetroArch on your system
3. Launch RetroArch
4. Go to: Main Menu > Online Updater > Core Downloader
5. Download the '{emulator['core']}' core

## Playing Games
1. In RetroArch, go to: Main Menu > Load Content
2. Navigate to the games folder
3. Select a game file ({', '.join(emulator['extensions'])})
4. The game will launch automatically with the appropriate core

## Controls
- Default keyboard controls can be configured in: Settings > Input
- For gamepad support, connect your controller before launching RetroArch
- RetroArch supports Xbox, PlayStation, and most USB gamepads

## Tips
- Save states: F2 (save), F4 (load)
- Fast forward: Space bar
- Fullscreen: F (toggle)
- Screenshot: F8
"""
    
    async def create_bundle(
        self,
        games: List[GamePackage],
        theme: str,
        output_path: str
    ) -> GameBundle:
        """
        Create a bundled game collection
        
        Args:
            games: List of GamePackage objects
            theme: Bundle theme/name
            output_path: Path to save bundle ZIP
        """
        logger.info(f"Creating bundle: {theme} with {len(games)} games")
        
        # Group games by platform
        platform_groups = {}
        for game in games:
            if game.platform not in platform_groups:
                platform_groups[game.platform] = []
            platform_groups[game.platform].append(game)
        
        # Create bundle directory structure
        bundle_dir = Path(output_path).parent / theme
        bundle_dir.mkdir(exist_ok=True)
        
        total_size = 0
        
        # Organize by platform
        for platform, platform_games in platform_groups.items():
            platform_dir = bundle_dir / platform
            platform_dir.mkdir(exist_ok=True)
            
            # Copy game files (simulated - in real implementation, copy actual files)
            for game in platform_games:
                game_dir = platform_dir / game.identifier
                game_dir.mkdir(exist_ok=True)
                
                # Create game info file
                info_file = game_dir / "game_info.json"
                info_file.write_text(json.dumps({
                    'title': game.title,
                    'publisher': game.publisher,
                    'year': game.year,
                    'genre': game.genre,
                    'description': game.description
                }, indent=2))
            
            # Add emulator info
            emulator_info = await self.get_emulator_info(platform)
            emulator_file = platform_dir / "EMULATOR_SETUP.md"
            emulator_file.write_text(emulator_info['setup_instructions'])
        
        # Create master README
        readme = bundle_dir / "README.md"
        readme_content = f"""# {theme}

This collection contains {len(games)} classic games organized by platform.

## Platforms Included
"""
        for platform, platform_games in platform_groups.items():
            readme_content += f"- **{platform.upper()}**: {len(platform_games)} games\n"
        
        readme_content += """
## How to Play
1. Navigate to the platform folder (e.g., `nes/`, `snes/`)
2. Read the EMULATOR_SETUP.md file for setup instructions
3. Install the recommended emulator
4. Load the game files

## Collection Info
- All games sourced from Internet Archive (archive.org)
- Games are preserved for historical and educational purposes
- Check individual game folders for detailed information

Enjoy your retro gaming experience!
"""
        readme.write_text(readme_content)
        
        # Create ZIP bundle
        await self._create_zip(bundle_dir, output_path)
        
        bundle = GameBundle(
            name=theme,
            description=f"Collection of {len(games)} retro games",
            platform="multi" if len(platform_groups) > 1 else list(platform_groups.keys())[0],
            games=games,
            emulator_info={p: await self.get_emulator_info(p) for p in platform_groups.keys()},
            total_size_mb=total_size / (1024 * 1024)
        )
        
        logger.info(f"Bundle created: {output_path}")
        return bundle
    
    async def _create_zip(self, source_dir: Path, output_zip: str):
        """Create ZIP file from directory"""
        def _zip():
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in source_dir.rglob('*'):
                    if file.is_file():
                        zipf.write(file, file.relative_to(source_dir.parent))
        
        await asyncio.to_thread(_zip)


# Example usage
if __name__ == "__main__":
    import internetarchive as ia
    
    async def main():
        agent = GameEmulatorAgent(ia_client=ia)
        
        # Search for NES games
        games_meta = await agent.search_games(
            platform='nes',
            genre='action',
            year_range=(1985, 1995),
            max_results=10
        )
        
        # Download games
        games = []
        for game_meta in games_meta[:5]:  # First 5
            game = await agent.download_game(game_meta['identifier'])
            games.append(game)
        
        # Create bundle
        bundle = await agent.create_bundle(
            games,
            theme="Ultimate_NES_Action_Collection",
            output_path="/tmp/nes_bundle.zip"
        )
        
        print(f"Created bundle: {bundle.name} with {len(bundle.games)} games")
    
    asyncio.run(main())
