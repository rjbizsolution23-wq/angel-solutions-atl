"""
APK Manager Agent - Android Application Management
Downloads and manages Android APK files from Internet Archive
"""
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import zipfile
import json

logger = logging.getLogger(__name__)


@dataclass
class APKPackage:
    identifier: str
    app_name: str
    package_name: str  # e.g., com.example.app
    version: str
    version_code: int
    min_sdk: int
    target_sdk: int
    permissions: List[str]
    category: str
    publisher: str
    description: str
    file_url: str
    file_size: int
    icon_url: Optional[str]
    screenshots: List[str]


@dataclass
class APKBundle:
    name: str
    description: str
    category: str
    apks: List[APKPackage]
    total_size_mb: float


class APKManagerAgent:
    """
    Autonomous agent for Android APK discovery and management
    
    Features:
    - Search IA for Android apps
    - Download APK files with version history
    - Extract app metadata (permissions, SDK, etc.)
    - Create themed APK bundles
    - Generate installation guides
    
    Note: Requires 'androguard' for APK analysis
    """
    
    def __init__(self, ia_client):
        self.ia = ia_client
        self._androguard_available = self._check_androguard()
    
    def _check_androguard(self) -> bool:
        """Check if androguard is available"""
        try:
            import androguard
            return True
        except ImportError:
            logger.warning("androguard not available - APK analysis will be limited")
            return False
    
    async def search_apks(
        self,
        query: str,
        category: Optional[str] = None,
        year_range: Optional[tuple] = None,
        max_results: int = 50
    ) -> List[Dict]:
        """
        Search Internet Archive for Android APKs
        
        Args:
            query: Search keywords
            category: Category filter (games, productivity, social, etc.)
            year_range: (min_year, max_year)
            max_results: Maximum results
        """
        logger.info(f"Searching APKs: query='{query}', category={category}")
        
        # Build search query
        # Note: IA doesn't have a unified APK collection, apps are scattered
        # We search for APK files in various collections
        search_parts = ["format:APK"]
        
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
            fields=['identifier', 'title', 'creator', 'year', 'subject', 'description'],
            max_results=max_results
        )
        
        apk_list = []
        for result in results:
            apk_list.append({
                'identifier': result.get('identifier'),
                'app_name': result.get('title', 'Unknown'),
                'publisher': result.get('creator', ['Unknown'])[0] if result.get('creator') else 'Unknown',
                'year': result.get('year'),
                'subjects': result.get('subject', []),
                'description': result.get('description', '')
            })
        
        logger.info(f"Found {len(apk_list)} APKs")
        return apk_list
    
    async def download_apk(
        self,
        identifier: str,
        dest_dir: str = "/tmp",
        analyze: bool = True
    ) -> APKPackage:
        """
        Download APK and extract metadata
        
        Args:
            identifier: IA item identifier
            dest_dir: Destination directory
            analyze: Whether to analyze APK with androguard
        """
        logger.info(f"Downloading APK: {identifier}")
        
        item = await asyncio.to_thread(self.ia.get_item, identifier)
        metadata = item.metadata
        
        # Find APK files
        apk_files = [f for f in item.files if f['name'].endswith('.apk')]
        
        if not apk_files:
            raise ValueError(f"No APK files found in {identifier}")
        
        # Use the first/largest APK
        apk_file = max(apk_files, key=lambda f: int(f.get('size', 0)))
        apk_filename = apk_file['name']
        
        # Download APK
        await asyncio.to_thread(item.download, files=[apk_filename], destdir=dest_dir)
        apk_path = Path(dest_dir) / identifier / apk_filename
        
        # Extract metadata
        if analyze and self._androguard_available:
            apk_meta = await self._analyze_apk(str(apk_path))
        else:
            apk_meta = await self._basic_apk_info(str(apk_path), metadata)
        
        # Get icon and screenshots
        icon_url = None
        screenshots = []
        
        for file in item.files:
            fname = file['name']
            if 'icon' in fname.lower() and fname.endswith(('.png', '.jpg')):
                icon_url = f"https://archive.org/download/{identifier}/{fname}"
            elif 'screenshot' in fname.lower() and fname.endswith(('.png', '.jpg')):
                screenshots.append(f"https://archive.org/download/{identifier}/{fname}")
        
        package = APKPackage(
            identifier=identifier,
            app_name=apk_meta.get('app_name', metadata.get('title', 'Unknown')),
            package_name=apk_meta.get('package_name', 'unknown'),
            version=apk_meta.get('version', metadata.get('version', '1.0')),
            version_code=apk_meta.get('version_code', 1),
            min_sdk=apk_meta.get('min_sdk', 14),
            target_sdk=apk_meta.get('target_sdk', 28),
            permissions=apk_meta.get('permissions', []),
            category=self._categorize_app(metadata.get('subject', [])),
            publisher=metadata.get('creator', ['Unknown'])[0] if metadata.get('creator') else 'Unknown',
            description=metadata.get('description', ''),
            file_url=f"https://archive.org/download/{identifier}/{apk_filename}",
            file_size=int(apk_file.get('size', 0)),
            icon_url=icon_url,
            screenshots=screenshots
        )
        
        logger.info(f"Downloaded: {package.app_name} v{package.version}")
        return package
    
    async def _analyze_apk(self, apk_path: str) -> Dict:
        """Analyze APK using androguard"""
        from androguard.core.apk import APK
        
        def _parse():
            apk = APK(apk_path)
            return {
                'app_name': apk.get_app_name(),
                'package_name': apk.get_package(),
                'version': apk.get_androidversion_name(),
                'version_code': apk.get_androidversion_code(),
                'min_sdk': int(apk.get_min_sdk_version() or 14),
                'target_sdk': int(apk.get_target_sdk_version() or 28),
                'permissions': apk.get_permissions()
            }
        
        return await asyncio.to_thread(_parse)
    
    async def _basic_apk_info(self, apk_path: str, metadata: Dict) -> Dict:
        """Extract basic info without androguard"""
        return {
            'app_name': metadata.get('title', 'Unknown'),
            'package_name': 'unknown',
            'version': metadata.get('version', '1.0'),
            'version_code': 1,
            'min_sdk': 14,
            'target_sdk': 28,
            'permissions': []
        }
    
    def _categorize_app(self, subjects: List[str]) -> str:
        """Categorize app based on subjects"""
        subjects_lower = [s.lower() for s in subjects]
        
        categories = {
            'games': ['game', 'gaming', 'puzzle', 'arcade'],
            'social': ['social', 'chat', 'messaging', 'communication'],
            'productivity': ['office', 'productivity', 'business', 'work'],
            'media': ['music', 'video', 'photo', 'media', 'player'],
            'utilities': ['utility', 'tool', 'calculator', 'file'],
            'education': ['education', 'learning', 'reference', 'book'],
            'lifestyle': ['lifestyle', 'health', 'fitness', 'food']
        }
        
        for category, keywords in categories.items():
            if any(keyword in subject for subject in subjects_lower for keyword in keywords):
                return category
        
        return 'other'
    
    async def create_bundle(
        self,
        apks: List[APKPackage],
        theme: str,
        output_path: str
    ) -> APKBundle:
        """
        Create an APK bundle collection
        
        Args:
            apks: List of APKPackage objects
            theme: Bundle theme/name
            output_path: Path to save bundle ZIP
        """
        logger.info(f"Creating APK bundle: {theme} with {len(apks)} apps")
        
        # Create bundle directory
        bundle_dir = Path(output_path).parent / theme
        bundle_dir.mkdir(exist_ok=True)
        
        # Group by category
        category_groups = {}
        for apk in apks:
            if apk.category not in category_groups:
                category_groups[apk.category] = []
            category_groups[apk.category].append(apk)
        
        # Organize by category
        total_size = 0
        for category, category_apks in category_groups.items():
            category_dir = bundle_dir / category
            category_dir.mkdir(exist_ok=True)
            
            for apk in category_apks:
                apk_dir = category_dir / apk.package_name
                apk_dir.mkdir(exist_ok=True)
                
                # Create app info file
                info_file = apk_dir / "app_info.json"
                info_file.write_text(json.dumps({
                    'app_name': apk.app_name,
                    'package_name': apk.package_name,
                    'version': apk.version,
                    'version_code': apk.version_code,
                    'category': apk.category,
                    'publisher': apk.publisher,
                    'description': apk.description,
                    'min_sdk': apk.min_sdk,
                    'target_sdk': apk.target_sdk,
                    'permissions': apk.permissions,
                    'download_url': apk.file_url,
                    'icon_url': apk.icon_url,
                    'screenshots': apk.screenshots
                }, indent=2))
                
                total_size += apk.file_size
        
        # Create master README
        readme = bundle_dir / "README.md"
        readme_content = f"""# {theme}

This APK bundle contains {len(apks)} Android applications organized by category.

## Categories Included
"""
        for category, apks_cat in category_groups.items():
            readme_content += f"- **{category.title()}**: {len(apks_cat)} apps\n"
        
        readme_content += f"""
## Installation Instructions

### Method 1: Direct Installation (Recommended)
1. Transfer the APK files to your Android device
2. Enable "Install from Unknown Sources" in Settings
3. Use a file manager to locate and tap the APK file
4. Follow the installation prompts

### Method 2: ADB Installation (Developer)
1. Enable USB Debugging on your device
2. Connect device to computer
3. Run: `adb install path/to/app.apk`

## Bundle Details

Total Size: {total_size / (1024**2):.1f} MB
Number of Apps: {len(apks)}
Categories: {', '.join(category_groups.keys())}

## Permissions Notice

Each app requests specific permissions. Check the app_info.json file in each app folder for the complete list of permissions.

## Compatibility

- Minimum Android version varies by app (check app_info.json)
- Most apps support Android 4.0+ (API 14)
- Some modern apps require Android 7.0+ (API 24)

## Important Notes

1. **Unknown Sources**: You must enable installation from unknown sources in your device settings
2. **Security**: All APKs sourced from Internet Archive - verify integrity before installation
3. **Updates**: These are archived versions - newer versions may be available from official sources
4. **Compatibility**: Check min_sdk in app_info.json to ensure device compatibility

## Licensing

Each application has its own license. Check the app_info.json file for publisher and licensing information.

All APKs sourced from Internet Archive (archive.org) and distributed for preservation and educational purposes.

Enjoy your Android app collection!
"""
        readme.write_text(readme_content)
        
        # Create installation guide
        install_guide = bundle_dir / "INSTALL_GUIDE.md"
        install_guide_content = """# Android APK Installation Guide

## Prerequisites

- Android device (phone or tablet)
- File manager app
- OR computer with ADB tools

## Method 1: Direct Installation on Device

### Step 1: Enable Unknown Sources

**Android 8.0+ (Oreo and newer):**
1. Go to Settings > Apps & notifications
2. Tap Advanced > Special app access
3. Tap Install unknown apps
4. Select your file manager app
5. Enable "Allow from this source"

**Android 7.1 and older:**
1. Go to Settings > Security
2. Enable "Unknown sources"
3. Confirm the warning dialog

### Step 2: Transfer APK Files

**Option A: USB Cable**
1. Connect device to computer
2. Copy APK files to device storage (e.g., Downloads folder)
3. Safely disconnect device

**Option B: Cloud Storage**
1. Upload APKs to Google Drive / Dropbox
2. Download on your Android device

### Step 3: Install APKs

1. Open your file manager app
2. Navigate to folder with APK files
3. Tap on an APK file
4. Review permissions (if shown)
5. Tap "Install"
6. Wait for installation to complete
7. Tap "Open" to launch or "Done" to finish

## Method 2: ADB Installation (Advanced)

### Setup ADB

**Windows:**
1. Download Android Platform Tools
2. Extract to C:\\platform-tools
3. Add to PATH environment variable

**macOS/Linux:**
```bash
# macOS (Homebrew)
brew install android-platform-tools

# Linux (apt)
sudo apt-get install android-tools-adb
```

### Enable USB Debugging

1. Go to Settings > About phone
2. Tap "Build number" 7 times to enable Developer mode
3. Go back to Settings > System > Developer options
4. Enable "USB debugging"
5. Connect device via USB
6. Allow USB debugging when prompted

### Install via ADB

```bash
# Install single APK
adb install path/to/app.apk

# Install multiple APKs
for apk in *.apk; do adb install "$apk"; done

# Reinstall/upgrade existing app
adb install -r path/to/app.apk
```

## Troubleshooting

**"App not installed" error:**
- Check Android version compatibility (min_sdk in app_info.json)
- Ensure sufficient storage space
- Try uninstalling previous version first

**"Parse error":**
- APK file may be corrupted - re-download
- Device architecture mismatch (arm vs x86)

**"Unknown source" error:**
- Verify "Install unknown apps" is enabled for your file manager

**App crashes on launch:**
- Check target_sdk compatibility
- Clear app data: Settings > Apps > [App Name] > Storage > Clear Data
- Some older apps may not work on modern Android versions

## Security Best Practices

1. ✅ Only install APKs from trusted sources (like this archive bundle)
2. ✅ Review permissions before installing
3. ✅ Keep Android OS updated
4. ✅ Use antivirus if concerned
5. ✅ Disable "Unknown sources" after installation complete

## Uninstalling Apps

1. Long-press app icon on home screen
2. Drag to "Uninstall"
OR
1. Go to Settings > Apps
2. Select app
3. Tap "Uninstall"

"""
        install_guide.write_text(install_guide_content)
        
        # Create ZIP bundle
        await self._create_zip(bundle_dir, output_path)
        
        bundle = APKBundle(
            name=theme,
            description=f"Collection of {len(apks)} Android applications",
            category='mixed' if len(category_groups) > 1 else list(category_groups.keys())[0],
            apks=apks,
            total_size_mb=total_size / (1024**2)
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
        agent = APKManagerAgent(ia_client=ia)
        
        # Search for APKs
        apk_meta = await agent.search_apks(
            query="android game",
            category="games",
            max_results=20
        )
        
        # Download APKs
        apks = []
        for meta in apk_meta[:10]:
            try:
                apk = await agent.download_apk(meta['identifier'], download_files=False)
                apks.append(apk)
            except Exception as e:
                logger.error(f"Failed to download {meta['identifier']}: {e}")
        
        if apks:
            # Create bundle
            bundle = await agent.create_bundle(
                apks,
                theme="Android_Games_Collection",
                output_path="/tmp/android_games_bundle.zip"
            )
            
            print(f"Created bundle: {bundle.name}")
            print(f"Total size: {bundle.total_size_mb:.1f} MB")
            print(f"Apps: {len(bundle.apks)}")
    
    asyncio.run(main())
