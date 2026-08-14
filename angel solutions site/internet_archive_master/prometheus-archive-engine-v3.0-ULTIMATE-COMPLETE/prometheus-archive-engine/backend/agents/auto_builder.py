"""
AUTO BUILDER AGENT - The Most Powerful Agent
Downloads source code from Internet Archive and BUILDS it.

This agent can:
- Retrieve source code for any software
- Compile C/C++, Rust, Go, Java, Python, Node.js projects
- Package binaries (deb, rpm, msi, dmg, apk, appimage)
- Test builds automatically
- Sign and distribute packages

Author: RJ PROMETHEUS APEX
Date: 2026-07-11
Version: 3.0.0
"""

import asyncio
import os
import tempfile
import hashlib
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import docker
from loguru import logger

# ═══════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════

class BuildStatus(Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    BUILDING = "building"
    TESTING = "testing"
    PACKAGING = "packaging"
    COMPLETED = "completed"
    FAILED = "failed"


class TargetPlatform(Enum):
    LINUX_X64 = "linux-x64"
    LINUX_ARM64 = "linux-arm64"
    WINDOWS_X64 = "windows-x64"
    MACOS_X64 = "macos-x64"
    MACOS_ARM64 = "macos-arm64"
    ANDROID_ARM64 = "android-arm64"
    WEB_WASM = "web-wasm"


class SourceLanguage(Enum):
    C = "c"
    CPP = "cpp"
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    PYTHON = "python"
    NODEJS = "nodejs"
    DOTNET = "dotnet"


@dataclass
class BuildConfig:
    optimization: str = "release"  # debug, release, production
    strip_symbols: bool = True
    static_linking: bool = False
    cross_compile: bool = False
    custom_flags: List[str] = None
    dependencies: List[str] = None


@dataclass
class BuildResult:
    status: BuildStatus
    artifact_path: Optional[Path] = None
    artifact_size: Optional[int] = None
    checksum: Optional[str] = None
    build_log: str = ""
    test_results: Optional[Dict] = None
    error: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════
# DOCKER BUILD ENVIRONMENTS
# ═══════════════════════════════════════════════════════════════════

BUILD_CONTAINERS = {
    SourceLanguage.C: "gcc:13-bullseye",
    SourceLanguage.CPP: "gcc:13-bullseye",
    SourceLanguage.RUST: "rust:1.78-slim",
    SourceLanguage.GO: "golang:1.22-alpine",
    SourceLanguage.JAVA: "eclipse-temurin:21-jdk",
    SourceLanguage.PYTHON: "python:3.12-slim",
    SourceLanguage.NODEJS: "node:22-alpine",
    SourceLanguage.DOTNET: "mcr.microsoft.com/dotnet/sdk:8.0"
}

BUILD_COMMANDS = {
    SourceLanguage.C: "gcc {flags} -o {output} {sources}",
    SourceLanguage.CPP: "g++ {flags} -o {output} {sources}",
    SourceLanguage.RUST: "cargo build --release",
    SourceLanguage.GO: "go build -o {output} {sources}",
    SourceLanguage.JAVA: "javac {sources} && jar cvfe {output} Main *.class",
    SourceLanguage.PYTHON: "pyinstaller --onefile {entry}",
    SourceLanguage.NODEJS: "npm install && npm run build",
    SourceLanguage.DOTNET: "dotnet publish -c Release -o {output}"
}


# ═══════════════════════════════════════════════════════════════════
# AUTO BUILDER AGENT
# ═══════════════════════════════════════════════════════════════════

class AutoBuilderAgent:
    """
    The ultimate agent - downloads source and BUILDS it.
    """
    
    def __init__(self, ia_client, llm_service, storage_manager):
        self.ia_client = ia_client
        self.llm = llm_service
        self.storage = storage_manager
        self.docker_client = docker.from_env()
        logger.info("🔧 AutoBuilderAgent initialized")
    
    # ───────────────────────────────────────────────────────────────
    # MAIN AUTO-BUILD WORKFLOW
    # ───────────────────────────────────────────────────────────────
    
    async def auto_build(
        self,
        request: str,
        source_identifier: Optional[str] = None,
        target_platform: TargetPlatform = TargetPlatform.LINUX_X64,
        build_config: Optional[BuildConfig] = None
    ) -> BuildResult:
        """
        Main entry point: natural language request -> compiled binary.
        
        Example:
            "Build a PDF reader"
            "Create a text editor for Linux"
            "Compile RetroArch with NES core"
        """
        logger.info(f"🎯 Auto-build request: {request}")
        
        try:
            # Step 1: If no identifier provided, search for source
            if not source_identifier:
                logger.info("🔍 Searching for source code...")
                source_identifier = await self._search_source(request)
            
            # Step 2: Download source from Internet Archive
            logger.info(f"⬇️ Downloading source: {source_identifier}")
            source_path = await self._download_source(source_identifier)
            
            # Step 3: Analyze source structure
            logger.info("🔬 Analyzing source structure...")
            analysis = await self._analyze_source(source_path)
            
            # Step 4: Compile source
            logger.info(f"🏗️ Building for {target_platform.value}...")
            build_result = await self._compile_source(
                source_path,
                analysis,
                target_platform,
                build_config or BuildConfig()
            )
            
            # Step 5: Test the build
            if build_result.status == BuildStatus.COMPLETED:
                logger.info("🧪 Testing build...")
                test_results = await self._test_build(build_result.artifact_path)
                build_result.test_results = test_results
            
            # Step 6: Package artifact
            if build_result.status == BuildStatus.COMPLETED:
                logger.info("📦 Packaging artifact...")
                package_path = await self._package_artifact(
                    build_result.artifact_path,
                    target_platform
                )
                build_result.artifact_path = package_path
                build_result.artifact_size = package_path.stat().st_size
                build_result.checksum = self._calculate_checksum(package_path)
            
            logger.info(f"✅ Build completed: {build_result.artifact_path}")
            return build_result
        
        except Exception as e:
            logger.error(f"❌ Build failed: {str(e)}")
            return BuildResult(
                status=BuildStatus.FAILED,
                error=str(e)
            )
    
    # ───────────────────────────────────────────────────────────────
    # SEARCH FOR SOURCE CODE
    # ───────────────────────────────────────────────────────────────
    
    async def _search_source(self, query: str) -> str:
        """
        Use LLM to understand request and search IA for source code.
        """
        # Use LLM to extract search terms
        prompt = f"""
        User wants to build: "{query}"
        
        What software are they looking for? Extract:
        1. Software name
        2. Category (editor, viewer, game, tool, etc.)
        3. Preferred language (C, C++, Rust, Go, etc.)
        
        Return JSON:
        {{"name": "...", "category": "...", "language": "..."}}
        """
        
        analysis = await self.llm.analyze(prompt)
        
        # Search Internet Archive for source code
        search_query = f"{analysis['name']} source code {analysis['language']}"
        results = await self.ia_client.search(
            query=search_query,
            mediatype="software",
            subject=["source code", "open source"]
        )
        
        if not results:
            raise Exception(f"No source code found for: {query}")
        
        # Return the top result
        return results[0].identifier
    
    # ───────────────────────────────────────────────────────────────
    # DOWNLOAD SOURCE CODE
    # ───────────────────────────────────────────────────────────────
    
    async def _download_source(self, identifier: str) -> Path:
        """
        Download source code from Internet Archive.
        """
        # Get metadata
        metadata = await self.ia_client.get_metadata(identifier)
        
        # Find source archive (tar.gz, zip, tar.bz2, etc.)
        source_files = [
            f for f in metadata.files
            if any(f.name.endswith(ext) for ext in [
                ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz",
                ".zip", ".7z"
            ])
        ]
        
        if not source_files:
            raise Exception(f"No source archive found in {identifier}")
        
        # Download largest archive (usually the complete source)
        source_file = max(source_files, key=lambda f: f.size)
        
        download_url = f"https://archive.org/download/{identifier}/{source_file.name}"
        
        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix="ia_build_"))
        archive_path = temp_dir / source_file.name
        
        # Download
        logger.info(f"Downloading {source_file.name} ({source_file.size} bytes)...")
        await self.ia_client.download_file(download_url, archive_path)
        
        # Extract
        logger.info("Extracting archive...")
        extract_dir = temp_dir / "source"
        extract_dir.mkdir()
        
        if archive_path.suffix == ".zip":
            subprocess.run(["unzip", "-q", str(archive_path), "-d", str(extract_dir)], check=True)
        else:
            subprocess.run(["tar", "xf", str(archive_path), "-C", str(extract_dir)], check=True)
        
        # Find the actual source directory (often nested)
        source_dirs = list(extract_dir.iterdir())
        if len(source_dirs) == 1 and source_dirs[0].is_dir():
            return source_dirs[0]
        else:
            return extract_dir
    
    # ───────────────────────────────────────────────────────────────
    # ANALYZE SOURCE STRUCTURE
    # ───────────────────────────────────────────────────────────────
    
    async def _analyze_source(self, source_path: Path) -> Dict[str, Any]:
        """
        Analyze source code structure to determine:
        - Programming language
        - Build system (make, cmake, cargo, npm, etc.)
        - Dependencies
        - Entry point
        """
        analysis = {
            "language": None,
            "build_system": None,
            "dependencies": [],
            "entry_point": None,
            "requires_deps_install": False
        }
        
        # Detect language and build system
        if (source_path / "Cargo.toml").exists():
            analysis["language"] = SourceLanguage.RUST
            analysis["build_system"] = "cargo"
        
        elif (source_path / "go.mod").exists():
            analysis["language"] = SourceLanguage.GO
            analysis["build_system"] = "go"
        
        elif (source_path / "package.json").exists():
            analysis["language"] = SourceLanguage.NODEJS
            analysis["build_system"] = "npm"
            analysis["requires_deps_install"] = True
        
        elif (source_path / "pom.xml").exists():
            analysis["language"] = SourceLanguage.JAVA
            analysis["build_system"] = "maven"
        
        elif (source_path / "CMakeLists.txt").exists():
            analysis["language"] = SourceLanguage.CPP
            analysis["build_system"] = "cmake"
        
        elif (source_path / "Makefile").exists():
            # Could be C or C++
            cpp_files = list(source_path.rglob("*.cpp"))
            analysis["language"] = SourceLanguage.CPP if cpp_files else SourceLanguage.C
            analysis["build_system"] = "make"
        
        elif (source_path / "setup.py").exists() or (source_path / "pyproject.toml").exists():
            analysis["language"] = SourceLanguage.PYTHON
            analysis["build_system"] = "pip"
        
        else:
            # Fallback: count file extensions
            extensions = {}
            for f in source_path.rglob("*"):
                if f.is_file():
                    ext = f.suffix
                    extensions[ext] = extensions.get(ext, 0) + 1
            
            # Most common extension
            if extensions:
                common_ext = max(extensions, key=extensions.get)
                lang_map = {
                    ".c": SourceLanguage.C,
                    ".cpp": SourceLanguage.CPP,
                    ".rs": SourceLanguage.RUST,
                    ".go": SourceLanguage.GO,
                    ".java": SourceLanguage.JAVA,
                    ".py": SourceLanguage.PYTHON,
                    ".js": SourceLanguage.NODEJS,
                    ".cs": SourceLanguage.DOTNET
                }
                analysis["language"] = lang_map.get(common_ext, SourceLanguage.C)
        
        logger.info(f"Detected: {analysis['language'].value} with {analysis['build_system']}")
        
        return analysis
    
    # ───────────────────────────────────────────────────────────────
    # COMPILE SOURCE CODE
    # ───────────────────────────────────────────────────────────────
    
    async def _compile_source(
        self,
        source_path: Path,
        analysis: Dict[str, Any],
        target_platform: TargetPlatform,
        config: BuildConfig
    ) -> BuildResult:
        """
        Compile source code inside Docker container.
        """
        language = analysis["language"]
        build_system = analysis["build_system"]
        
        # Get appropriate Docker image
        image = BUILD_CONTAINERS[language]
        
        # Create output directory
        output_dir = source_path.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Build command based on build system
        if build_system == "cargo":
            build_cmd = "cargo build --release"
            artifact_path = "target/release/*"
        
        elif build_system == "cmake":
            build_cmd = """
                mkdir -p build && cd build &&
                cmake -DCMAKE_BUILD_TYPE=Release .. &&
                cmake --build . --config Release
            """
            artifact_path = "build/*"
        
        elif build_system == "make":
            build_cmd = "make"
            artifact_path = "./*"
        
        elif build_system == "npm":
            build_cmd = "npm install && npm run build"
            artifact_path = "dist/*"
        
        elif build_system == "go":
            build_cmd = "go build -o app"
            artifact_path = "app"
        
        else:
            build_cmd = "make"  # Default
            artifact_path = "./*"
        
        # Run build in Docker
        try:
            logger.info(f"Running build in {image}...")
            
            container = self.docker_client.containers.run(
                image=image,
                command=f"sh -c '{build_cmd}'",
                volumes={
                    str(source_path.absolute()): {"bind": "/workspace", "mode": "rw"}
                },
                working_dir="/workspace",
                detach=True,
                remove=True
            )
            
            # Stream logs
            build_log = ""
            for line in container.logs(stream=True):
                log_line = line.decode("utf-8")
                build_log += log_line
                logger.debug(log_line.strip())
            
            # Wait for container
            result = container.wait()
            
            if result["StatusCode"] != 0:
                return BuildResult(
                    status=BuildStatus.FAILED,
                    build_log=build_log,
                    error=f"Build failed with exit code {result['StatusCode']}"
                )
            
            # Find the built artifact
            artifacts = self._find_artifacts(source_path, language, build_system)
            
            if not artifacts:
                return BuildResult(
                    status=BuildStatus.FAILED,
                    build_log=build_log,
                    error="No artifacts found after build"
                )
            
            # Copy to output directory
            main_artifact = artifacts[0]
            output_file = output_dir / main_artifact.name
            import shutil
            shutil.copy2(main_artifact, output_file)
            
            return BuildResult(
                status=BuildStatus.COMPLETED,
                artifact_path=output_file,
                build_log=build_log
            )
        
        except Exception as e:
            logger.error(f"Docker build failed: {str(e)}")
            return BuildResult(
                status=BuildStatus.FAILED,
                error=str(e)
            )
    
    # ───────────────────────────────────────────────────────────────
    # FIND BUILD ARTIFACTS
    # ───────────────────────────────────────────────────────────────
    
    def _find_artifacts(
        self,
        source_path: Path,
        language: SourceLanguage,
        build_system: str
    ) -> List[Path]:
        """
        Find compiled binaries/executables.
        """
        artifacts = []
        
        # Common artifact locations by build system
        search_paths = {
            "cargo": ["target/release"],
            "cmake": ["build", "build/Release"],
            "make": ["."],
            "npm": ["dist", "build"],
            "go": ["."]
        }
        
        paths = search_paths.get(build_system, ["."])
        
        for p in paths:
            search_dir = source_path / p
            if not search_dir.exists():
                continue
            
            # Find executables
            for f in search_dir.rglob("*"):
                if f.is_file() and os.access(f, os.X_OK):
                    # Skip test files, scripts
                    if "test" not in f.name.lower() and not f.suffix in [".sh", ".py", ".pl"]:
                        artifacts.append(f)
        
        return sorted(artifacts, key=lambda f: f.stat().st_size, reverse=True)
    
    # ───────────────────────────────────────────────────────────────
    # TEST BUILD
    # ───────────────────────────────────────────────────────────────
    
    async def _test_build(self, artifact_path: Path) -> Dict[str, Any]:
        """
        Basic smoke tests on the built artifact.
        """
        tests = {
            "exists": artifact_path.exists(),
            "executable": os.access(artifact_path, os.X_OK),
            "size": artifact_path.stat().st_size,
            "runs": False,
            "help_works": False
        }
        
        # Try running with --help
        try:
            result = subprocess.run(
                [str(artifact_path), "--help"],
                capture_output=True,
                timeout=5
            )
            tests["runs"] = True
            tests["help_works"] = result.returncode == 0
        except Exception as e:
            logger.warning(f"Test execution failed: {e}")
        
        return tests
    
    # ───────────────────────────────────────────────────────────────
    # PACKAGE ARTIFACT
    # ───────────────────────────────────────────────────────────────
    
    async def _package_artifact(
        self,
        artifact_path: Path,
        target_platform: TargetPlatform
    ) -> Path:
        """
        Package the artifact for distribution.
        
        Formats:
        - Linux: .deb, .rpm, .appimage
        - Windows: .msi, .exe installer
        - macOS: .dmg, .pkg
        - Android: .apk
        """
        package_dir = artifact_path.parent / "package"
        package_dir.mkdir(exist_ok=True)
        
        if "linux" in target_platform.value:
            # Create .tar.gz for now
            # TODO: Implement .deb, .rpm, .appimage
            package_path = package_dir / f"{artifact_path.stem}.tar.gz"
            subprocess.run([
                "tar", "czf",
                str(package_path),
                "-C", str(artifact_path.parent),
                artifact_path.name
            ], check=True)
            return package_path
        
        elif "windows" in target_platform.value:
            # TODO: Implement .msi installer
            # For now, just return the .exe
            return artifact_path
        
        elif "macos" in target_platform.value:
            # TODO: Implement .dmg
            return artifact_path
        
        else:
            return artifact_path
    
    # ───────────────────────────────────────────────────────────────
    # UTILITIES
    # ───────────────────────────────────────────────────────────────
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    # ───────────────────────────────────────────────────────────────
    # HIGH-LEVEL API METHODS
    # ───────────────────────────────────────────────────────────────
    
    async def search_and_build(
        self,
        query: str,
        filters: Dict[str, Any],
        build_config: BuildConfig
    ) -> BuildResult:
        """
        Search for software and build it in one call.
        """
        return await self.auto_build(
            request=query,
            build_config=build_config
        )
    
    async def retrieve_source(self, identifier: str) -> Path:
        """
        Just download source code without building.
        """
        return await self._download_source(identifier)
    
    async def compile_existing_source(
        self,
        source_path: Path,
        target_platform: TargetPlatform = TargetPlatform.LINUX_X64,
        config: Optional[BuildConfig] = None
    ) -> BuildResult:
        """
        Build from existing source directory.
        """
        analysis = await self._analyze_source(source_path)
        return await self._compile_source(
            source_path,
            analysis,
            target_platform,
            config or BuildConfig()
        )


# ═══════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════

"""
# Initialize agent
auto_builder = AutoBuilderAgent(ia_client, llm_service, storage_manager)

# Example 1: Natural language build request
result = await auto_builder.auto_build(
    request="Build a PDF reader for Linux",
    target_platform=TargetPlatform.LINUX_X64
)

# Example 2: Build from known identifier
result = await auto_builder.auto_build(
    source_identifier="evince-3.45-source",
    target_platform=TargetPlatform.LINUX_X64
)

# Example 3: Just download source
source_path = await auto_builder.retrieve_source("mupdf-1.23-source")

# Example 4: Build existing source
result = await auto_builder.compile_existing_source(
    source_path=Path("/path/to/source"),
    target_platform=TargetPlatform.WINDOWS_X64,
    config=BuildConfig(optimization="release", static_linking=True)
)

print(f"Status: {result.status}")
print(f"Artifact: {result.artifact_path}")
print(f"Size: {result.artifact_size} bytes")
print(f"Checksum: {result.checksum}")
"""
