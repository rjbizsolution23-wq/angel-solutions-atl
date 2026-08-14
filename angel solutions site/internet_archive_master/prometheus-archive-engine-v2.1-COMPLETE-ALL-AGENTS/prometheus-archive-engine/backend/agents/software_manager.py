"""
Software Manager Agent - Desktop Software Discovery & Packaging
Downloads and bundles software from Internet Archive software collections
"""
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import zipfile
import json

logger = logging.getLogger(__name__)


# Software collection mappings
SOFTWARE_COLLECTIONS = {
    'windows': 'softwarelibrary_win',
    'mac': 'softwarelibrary_mac',
    'dos': 'softwarelibrary_msdos',
    'linux': 'open_source_software',
    'win3': 'softwarelibrary_win3',
    'win95': 'softwarelibrary_win_games'  # Windows games
}

PLATFORM_EXTENSIONS = {
    'windows': ['.exe', '.msi', '.zip'],
    'mac': ['.dmg', '.pkg', '.app.zip'],
    'dos': ['.exe', '.com', '.bat', '.zip'],
    'linux': ['.deb', '.rpm', '.tar.gz', '.appimage']
}


@dataclass
class SoftwarePackage:
    identifier: str
    title: str
    platform: str
    category: str  # productivity, development, multimedia, etc.
    publisher: str
    version: str
    year: Optional[int]
    description: str
    file_urls: List[str]
    file_sizes: List[int]  # bytes
    screenshot_urls: List[str]
    license: str


@dataclass
class SoftwareBundle:
    name: str
    description: str
    platform: str
    category: str
    packages: List[SoftwarePackage]
    total_size_mb: float
    installation_guide: str


class SoftwareManagerAgent:
    """
    Autonomous agent for desktop software discovery and packaging
    
    Features:
    - Search IA software libraries
    - Download installers and portable apps
    - Create themed software bundles
    - Generate installation guides
    - Extract metadata and screenshots
    
    Supported Platforms:
    - Windows (XP, 7, 8, 10, 11)
    - macOS (Classic through modern)
    - DOS / MS-DOS
    - Linux (Debian, RPM, AppImage)
    """
    
    def __init__(self, ia_client):
        self.ia = ia_client
    
    async def search_software(
        self,
        query: str,
        platform: str = 'windows',
        category: Optional[str] = None,
        year_range: Optional[tuple] = None,
        max_results: int = 50
    ) -> List[Dict]:
        """
        Search Internet Archive for software
        
        Args:
            query: Search keywords (e.g., "office", "photoshop", "games")
            platform: Platform (windows, mac, dos, linux)
            category: Category filter (productivity, development, games, etc.)
            year_range: (min_year, max_year)
            max_results: Maximum results
        """
        logger.info(f"Searching software: query='{query}', platform={platform}")
        
        # Get collection for platform
        collection = SOFTWARE_COLLECTIONS.get(platform.lower())
        if not collection:
            raise ValueError(f"Unknown platform: {platform}")
        
        # Build search query
        search_parts = [f"collection:{collection}"]
        
        if query:
            search_parts.append(f"({query})")
        
        if category:
            search_parts.append(f"subject:({category})")
        
        if year_range:
            search_parts.append(f"year:[{year_range[0]} TO {year_range[1]}]")
        
        search_query = " AND ".join(search_parts)
        
        # Execute search
        results = await asyncio.to_thread(
            self.ia.search_items,
            search_query,
            fields=['identifier', 'title', 'creator', 'year', 'subject', 'description', 'licenseurl'],
            max_results=max_results
        )
        
        software_list = []
        for result in results:
            software_list.append({
                'identifier': result.get('identifier'),
                'title': result.get('title', 'Unknown'),
                'publisher': result.get('creator', ['Unknown'])[0] if result.get('creator') else 'Unknown',
                'year': result.get('year'),
                'subjects': result.get('subject', []),
                'description': result.get('description', ''),
                'license': result.get('licenseurl', 'Unknown')
            })
        
        logger.info(f"Found {len(software_list)} software packages")
        return software_list
    
    async def download_software(
        self,
        identifier: str,
        dest_dir: str = "/tmp",
        download_files: bool = True
    ) -> SoftwarePackage:
        """
        Download software package from Internet Archive
        
        Args:
            identifier: IA item identifier
            dest_dir: Destination directory
            download_files: Whether to actually download files (or just metadata)
        """
        logger.info(f"Downloading software: {identifier}")
        
        item = await asyncio.to_thread(self.ia.get_item, identifier)
        metadata = item.metadata
        
        # Detect platform from metadata or files
        platform = self._detect_platform(metadata, item.files)
        
        # Identify software files
        software_files = []
        file_urls = []
        file_sizes = []
        
        extensions = PLATFORM_EXTENSIONS.get(platform, ['.zip'])
        
        for file in item.files:
            name = file['name']
            if any(name.lower().endswith(ext) for ext in extensions):
                software_files.append(name)
                file_urls.append(f"https://archive.org/download/{identifier}/{name}")
                file_sizes.append(int(file.get('size', 0)))
        
        # Download files if requested
        if download_files and software_files:
            await asyncio.to_thread(item.download, files=software_files, destdir=dest_dir)
        
        # Get screenshots
        screenshot_urls = []
        for file in item.files:
            if file['name'].endswith(('.png', '.jpg', '.gif')) and 'screenshot' in file['name'].lower():
                screenshot_urls.append(f"https://archive.org/download/{identifier}/{file['name']}")
        
        # Extract category from subjects
        subjects = metadata.get('subject', [])
        category = self._categorize_software(subjects)
        
        package = SoftwarePackage(
            identifier=identifier,
            title=metadata.get('title', 'Unknown'),
            platform=platform,
            category=category,
            publisher=metadata.get('creator', ['Unknown'])[0] if metadata.get('creator') else 'Unknown',
            version=metadata.get('version', 'Unknown'),
            year=metadata.get('year'),
            description=metadata.get('description', ''),
            file_urls=file_urls,
            file_sizes=file_sizes,
            screenshot_urls=screenshot_urls,
            license=metadata.get('licenseurl', 'Unknown')
        )
        
        logger.info(f"Downloaded: {package.title} ({len(software_files)} files)")
        return package
    
    def _detect_platform(self, metadata: Dict, files: List) -> str:
        """Detect platform from metadata and file extensions"""
        # Check subjects
        subjects = [s.lower() for s in metadata.get('subject', [])]
        
        platform_keywords = {
            'windows': ['windows', 'win32', 'win64', 'microsoft windows'],
            'mac': ['macos', 'mac os', 'macintosh', 'apple'],
            'dos': ['dos', 'ms-dos', 'msdos'],
            'linux': ['linux', 'ubuntu', 'debian', 'fedora']
        }
        
        for platform, keywords in platform_keywords.items():
            if any(keyword in ' '.join(subjects) for keyword in keywords):
                return platform
        
        # Check file extensions
        for file in files:
            name = file['name'].lower()
            if name.endswith(('.exe', '.msi')):
                return 'windows'
            elif name.endswith(('.dmg', '.pkg')):
                return 'mac'
            elif name.endswith(('.deb', '.rpm')):
                return 'linux'
        
        return 'windows'  # Default
    
    def _categorize_software(self, subjects: List[str]) -> str:
        """Categorize software based on subjects"""
        subjects_lower = [s.lower() for s in subjects]
        
        categories = {
            'productivity': ['office', 'word processor', 'spreadsheet', 'presentation'],
            'development': ['programming', 'ide', 'compiler', 'development'],
            'multimedia': ['graphics', 'audio', 'video', 'media', 'photo'],
            'games': ['game', 'gaming', 'arcade', 'puzzle'],
            'utilities': ['utility', 'tool', 'system', 'backup'],
            'internet': ['browser', 'email', 'web', 'chat', 'network'],
            'education': ['educational', 'learning', 'tutorial', 'reference']
        }
        
        for category, keywords in categories.items():
            if any(keyword in subject for subject in subjects_lower for keyword in keywords):
                return category
        
        return 'other'
    
    async def create_bundle(
        self,
        packages: List[SoftwarePackage],
        theme: str,
        output_path: str,
        include_guides: bool = True
    ) -> SoftwareBundle:
        """
        Create a software bundle collection
        
        Args:
            packages: List of SoftwarePackage objects
            theme: Bundle theme/name
            output_path: Path to save bundle ZIP
            include_guides: Include installation guides
        """
        logger.info(f"Creating bundle: {theme} with {len(packages)} packages")
        
        # Create bundle directory structure
        bundle_dir = Path(output_path).parent / theme
        bundle_dir.mkdir(exist_ok=True)
        
        # Group by category
        category_groups = {}
        for pkg in packages:
            if pkg.category not in category_groups:
                category_groups[pkg.category] = []
            category_groups[pkg.category].append(pkg)
        
        # Organize by category
        total_size = 0
        for category, category_pkgs in category_groups.items():
            category_dir = bundle_dir / category
            category_dir.mkdir(exist_ok=True)
            
            for pkg in category_pkgs:
                pkg_dir = category_dir / pkg.identifier
                pkg_dir.mkdir(exist_ok=True)
                
                # Create package info file
                info_file = pkg_dir / "info.json"
                info_file.write_text(json.dumps({
                    'title': pkg.title,
                    'publisher': pkg.publisher,
                    'version': pkg.version,
                    'year': pkg.year,
                    'platform': pkg.platform,
                    'category': pkg.category,
                    'description': pkg.description,
                    'license': pkg.license,
                    'download_urls': pkg.file_urls
                }, indent=2))
                
                total_size += sum(pkg.file_sizes)
        
        # Create master README
        installation_guide = self._generate_installation_guide(packages, category_groups)
        
        readme = bundle_dir / "README.md"
        readme_content = f"""# {theme}

This software bundle contains {len(packages)} applications organized by category.

## Categories Included
"""
        for category, pkgs in category_groups.items():
            readme_content += f"- **{category.title()}**: {len(pkgs)} applications\n"
        
        readme_content += f"""
## Installation Instructions

See INSTALL_GUIDE.md for detailed installation instructions for each application.

## Bundle Contents

Total Size: {total_size / (1024**2):.1f} MB
Number of Applications: {len(packages)}
Platform: {packages[0].platform if packages else 'Multiple'}

## Usage Notes

1. Navigate to the category folder
2. Select the application you want to install
3. Read the info.json file for details
4. Follow the installation instructions in INSTALL_GUIDE.md

## Licensing

Each application has its own license. Check the info.json file in each application folder for license information.

All software sourced from Internet Archive (archive.org) and distributed for preservation and educational purposes.

Enjoy your software collection!
"""
        readme.write_text(readme_content)
        
        # Create installation guide
        if include_guides:
            guide_file = bundle_dir / "INSTALL_GUIDE.md"
            guide_file.write_text(installation_guide)
        
        # Create ZIP bundle
        await self._create_zip(bundle_dir, output_path)
        
        bundle = SoftwareBundle(
            name=theme,
            description=f"Collection of {len(packages)} software applications",
            platform=packages[0].platform if packages else 'multi',
            category='mixed' if len(category_groups) > 1 else list(category_groups.keys())[0],
            packages=packages,
            total_size_mb=total_size / (1024**2),
            installation_guide=installation_guide
        )
        
        logger.info(f"Bundle created: {output_path}")
        return bundle
    
    def _generate_installation_guide(
        self,
        packages: List[SoftwarePackage],
        category_groups: Dict
    ) -> str:
        """Generate comprehensive installation guide"""
        
        guide = f"""# Software Installation Guide

## General Information

This bundle contains {len(packages)} software applications from Internet Archive.

## Platform-Specific Instructions

"""
        
        # Windows instructions
        guide += """### Windows Applications

**Requirements:**
- Windows XP or later (most applications)
- Administrator privileges may be required

**Installation Steps:**
1. Extract the software archive if it's a .zip file
2. Locate the .exe or .msi installer
3. Right-click and "Run as Administrator"
4. Follow the installation wizard
5. Accept license agreements
6. Choose installation directory
7. Complete installation

**Portable Applications:**
Some applications are portable (.exe files that run without installation).
Simply extract and run the .exe file.

"""
        
        # macOS instructions
        guide += """### macOS Applications

**Requirements:**
- macOS version as specified in each app's info.json
- May require disabling Gatekeeper for older software

**Installation Steps:**
1. Mount .dmg files by double-clicking
2. Drag application to Applications folder
3. For .pkg installers, double-click and follow wizard
4. If "Unidentified Developer" error: System Preferences > Security & Privacy > Open Anyway

"""
        
        # DOS instructions
        guide += """### DOS Applications

**Requirements:**
- DOSBox emulator (download from dosbox.com)

**Installation Steps:**
1. Install DOSBox
2. Mount the software folder: `mount c /path/to/software`
3. Navigate to drive: `c:`
4. Run the .exe or .com file: `program.exe`

"""
        
        # Category-specific notes
        guide += "\n## Category-Specific Notes\n\n"
        
        for category, pkgs in category_groups.items():
            guide += f"### {category.title()} ({len(pkgs)} applications)\n\n"
            for pkg in pkgs:
                guide += f"**{pkg.title}** (v{pkg.version})\n"
                guide += f"- Publisher: {pkg.publisher}\n"
                guide += f"- Year: {pkg.year or 'Unknown'}\n"
                guide += f"- Files: {len(pkg.file_urls)}\n"
                if pkg.description:
                    guide += f"- Description: {pkg.description[:100]}...\n"
                guide += "\n"
        
        guide += """
## Troubleshooting

**Windows:**
- Compatibility mode: Right-click > Properties > Compatibility
- Run as Administrator
- Disable antivirus temporarily if false positive

**macOS:**
- Reset Gatekeeper: `sudo spctl --master-disable`
- Allow unsigned apps temporarily

**DOS:**
- Adjust cycles in DOSBox: `Ctrl+F11` (slower) / `Ctrl+F12` (faster)
- Fullscreen: `Alt+Enter`

## Support

For specific application issues, consult the original documentation or Internet Archive item page.

Bundle created by Prometheus Archive Engine v2.0
"""
        
        return guide
    
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
        agent = SoftwareManagerAgent(ia_client=ia)
        
        # Search for productivity software
        software_meta = await agent.search_software(
            query="office productivity",
            platform='windows',
            year_range=(1995, 2005),
            max_results=20
        )
        
        # Download packages (metadata only for demo)
        packages = []
        for sw_meta in software_meta[:10]:
            pkg = await agent.download_software(
                sw_meta['identifier'],
                download_files=False  # Metadata only
            )
            packages.append(pkg)
        
        # Create bundle
        bundle = await agent.create_bundle(
            packages,
            theme="Windows_Productivity_Suite_1995-2005",
            output_path="/tmp/productivity_bundle.zip"
        )
        
        print(f"Created bundle: {bundle.name}")
        print(f"Total size: {bundle.total_size_mb:.1f} MB")
        print(f"Packages: {len(bundle.packages)}")
    
    asyncio.run(main())
