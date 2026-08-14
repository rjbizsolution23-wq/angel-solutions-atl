# 🔥 PROMETHEUS ARCHIVE ENGINE V3.0 - ULTIMATE SYSTEM BUILDER PROMPT
## The PERFECT Meta-Prompt for Building Complete Internet Archive Master Platform

**Generated**: 2026-07-11  
**System**: RJ PROMETHEUS APEX  
**Version**: 3.0.0 (PRODUCTION-READY)

═══════════════════════════════════════════════════════════════════
## 🎯 MISSION: BUILD THE ULTIMATE INTERNET ARCHIVE PLATFORM
═══════════════════════════════════════════════════════════════════

You are building **PROMETHEUS ARCHIVE ENGINE v3.0** - a complete, production-ready platform that:

✅ **Searches, Views, Downloads** ALL Internet Archive content types  
✅ **Auto-Builds Anything** - Agents retrieve source AND compile/package on demand  
✅ **Full Monetization** - Stripe integration, licensing, bundles, courses  
✅ **Production Infrastructure** - Auth, DB, caching, background jobs, monitoring  
✅ **Professional UI** - Next.js 16.2 dashboard with real-time search/preview  
✅ **12 Specialized Agents** - Complete Internet Archive API coverage  

═══════════════════════════════════════════════════════════════════
## 🏗️ SYSTEM ARCHITECTURE OVERVIEW
═══════════════════════════════════════════════════════════════════

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js 16.2)                     │
│  • Universal Search Interface (all content types)               │
│  • Real-time Preview (books, videos, audio, games, software)    │
│  • Download Manager (queue, progress, history)                  │
│  • Collection Builder UI (drag-drop bundling)                   │
│  • Course Creator (structured learning paths)                   │
│  • Admin Dashboard (analytics, users, revenue)                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI 0.136)                  │
│  • JWT Authentication (RS256)                                   │
│  • Rate Limiting (per-user, per-IP)                            │
│  • Request Validation (Pydantic v2)                            │
│  • Prometheus Metrics                                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│             MASTER ORCHESTRATOR (LangGraph + Claude Opus 4.7)   │
│  Routes user requests to specialized agents                     │
└─────────────────────────────────────────────────────────────────┘
       ↓         ↓         ↓         ↓         ↓         ↓
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Book     │ │ Game     │ │ Software │ │ APK      │ │ Video    │
│ Rebrander│ │ Emulator │ │ Manager  │ │ Manager  │ │ Movies   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Audio    │ │ AutoBuild│ │ Wayback  │ │ Reviews  │ │ OCR      │
│ Music    │ │ Agent    │ │ Machine  │ │ Manager  │ │ Processor│
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
┌──────────┐ ┌──────────┐
│ Views    │ │ Tasks    │
│ Analytics│ │ Monitor  │
└──────────┘ └──────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                      CORE SERVICES LAYER                        │
│  • Internet Archive Client (S3-like API + all endpoints)       │
│  • LLM Service (Claude Opus 4.7 + GPT-4o fallback)            │
│  • Storage Manager (S3 + AI Drive + local cache)               │
│  • Build System (Docker-based compilation for software/games)   │
│  • Collection Builder (bundle creation, pricing)                │
│  • Course Generator (structured learning content)               │
│  • Stripe Client (products, checkout, webhooks, subscriptions)  │
│  • License Manager (key generation, validation, DRM)            │
│  • Email Service (SendGrid - transactional + marketing)         │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
│  • PostgreSQL 18.3 (primary DB + vector search pgvector)       │
│  • Redis 7.4 (cache + session + rate limiting + queues)        │
│  • Celery Workers (background jobs - downloads, builds, OCR)    │
│  • S3 Storage (artifacts, user uploads, generated content)      │
│  • Prometheus + Grafana (metrics + alerting)                   │
│  • Sentry 10.51 (error tracking + performance monitoring)       │
└─────────────────────────────────────────────────────────────────┘
```

═══════════════════════════════════════════════════════════════════
## 📦 AGENT SPECIFICATIONS - ALL 13 AGENTS
═══════════════════════════════════════════════════════════════════

### 1. **BookRebranderAgent** ✅ (IMPLEMENTED)
Search books, download PDFs/EPUBs, rebrand with AI (new cover, intro, updates), bundle into collections.

### 2. **GameEmulatorAgent** ✅ (IMPLEMENTED)
Search ROMs (NES, SNES, Genesis, etc.), download games, package with emulators (RetroArch), create bundles.

### 3. **SoftwareManagerAgent** ✅ (IMPLEMENTED)
Search desktop software (Windows/Mac/Linux), download installers, verify checksums, create developer toolkits.

### 4. **APKManagerAgent** ✅ (IMPLEMENTED)
Search Android APKs, download apps, analyze permissions, create themed collections (productivity, games, dev tools).

### 5. **VideoMoviesAgent** ⚠️ (PRIORITY 1 - IMPLEMENT THIS)
**Purpose**: Search and download movies, documentaries, educational videos from IA.

**Core Methods**:
```python
async def search_videos(
    query: str,
    mediatype: str = "movies",  # movies, television, education
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
    year_range: Optional[tuple] = None,
    language: Optional[str] = None,
    license: Optional[str] = None
) -> List[VideoResult]

async def download_video(
    identifier: str,
    format: str = "mp4",  # mp4, ogv, mpeg4
    quality: str = "720p"  # 480p, 720p, 1080p
) -> VideoFile

async def create_video_collection(
    video_ids: List[str],
    title: str,
    description: str,
    add_intro_outro: bool = True,
    generate_subtitles: bool = True
) -> VideoCollection

async def extract_metadata(
    identifier: str
) -> VideoMetadata  # Title, duration, format, codec, bitrate, runtime, credits
```

**IA API Integration**:
- Search: `https://archive.org/advancedsearch.php?q=mediatype:movies&output=json`
- Download: `https://archive.org/download/{identifier}/{filename}.mp4`
- Metadata: `https://archive.org/metadata/{identifier}`

**Monetization**:
- Single video download: $2.99
- Curated collection (10 videos): $19.99
- Documentary series bundle: $49.99
- Educational course with videos: $99.99

### 6. **AudioMusicAgent** ⚠️ (PRIORITY 1 - IMPLEMENT THIS)
**Purpose**: Search and download music, podcasts, audio books, live concerts from IA.

**Core Methods**:
```python
async def search_audio(
    query: str,
    mediatype: str = "audio",  # audio, etree (live concerts)
    format: Optional[str] = None,  # mp3, flac, ogg
    genre: Optional[str] = None,
    year_range: Optional[tuple] = None,
    duration_range: Optional[tuple] = None
) -> List[AudioResult]

async def download_audio(
    identifier: str,
    format: str = "mp3",  # mp3, flac, ogg, m4a
    bitrate: str = "320"  # 128, 192, 256, 320 kbps
) -> AudioFile

async def create_playlist(
    audio_ids: List[str],
    title: str,
    description: str,
    crossfade: bool = True,
    normalize_volume: bool = True
) -> Playlist

async def extract_audio_metadata(
    identifier: str
) -> AudioMetadata  # Artist, album, track, year, genre, duration, bitrate
```

**IA API Integration**:
- Search: `https://archive.org/advancedsearch.php?q=mediatype:audio&output=json`
- Download: `https://archive.org/download/{identifier}/{filename}.mp3`
- Live concerts (etree): `https://archive.org/details/etree?sort=-publicdate`

**Monetization**:
- Single track: $0.99
- Album download: $9.99
- Curated playlist (50 tracks): $24.99
- Audio book collection: $49.99

### 7. **AutoBuilderAgent** 🔥 (PRIORITY 0 - CRITICAL NEW AGENT)
**Purpose**: The MOST POWERFUL agent - retrieves source code, compiles, builds, packages anything user requests.

**Core Methods**:
```python
async def auto_build(
    request: str,  # Natural language: "Build a text editor", "Create a game engine"
    source_identifier: Optional[str] = None,  # IA identifier if known
    target_platform: str = "linux",  # linux, windows, macos, android, web
    optimization_level: str = "release"  # debug, release, production
) -> BuildResult

async def search_and_build(
    query: str,
    filters: BuildFilters,
    build_config: BuildConfig
) -> BuildResult

async def retrieve_source(
    identifier: str
) -> SourcePackage  # Downloads source code from IA

async def compile_source(
    source_path: Path,
    language: str,  # c, cpp, rust, go, java, python
    build_system: str,  # make, cmake, gradle, cargo, npm
    dependencies: List[str],
    flags: List[str]
) -> CompiledBinary

async def package_artifact(
    binary_path: Path,
    target_format: str,  # deb, rpm, msi, dmg, apk, appimage, flatpak
    include_dependencies: bool = True,
    sign_package: bool = True
) -> PackagedArtifact

async def test_build(
    artifact_path: Path,
    test_suite: str = "basic"  # basic, full, security
) -> TestReport
```

**Build System Architecture**:
```python
# Docker-based isolated build environment
# Supports: C/C++, Rust, Go, Java, Python, Node.js, .NET

BUILD_CONTAINERS = {
    "c_cpp": "gcc:13-bullseye",
    "rust": "rust:1.78-slim",
    "go": "golang:1.22-alpine",
    "java": "eclipse-temurin:21-jdk",
    "python": "python:3.12-slim",
    "node": "node:22-alpine",
    "dotnet": "mcr.microsoft.com/dotnet/sdk:8.0"
}
```

**Example Workflows**:
1. User: "Build me a PDF reader from Internet Archive source"
   - Agent searches IA for PDF reader source code
   - Downloads source (e.g., Evince, Okular, MuPDF)
   - Compiles with dependencies
   - Packages as .deb, .rpm, .exe, .dmg
   - Returns downloadable binaries + installer

2. User: "Create a retro game bundle with emulator"
   - Searches IA for game ROMs
   - Downloads RetroArch source
   - Compiles emulator cores
   - Packages games + emulator + config
   - Returns single-click installer

3. User: "Build a custom Linux distro with these tools"
   - Retrieves source for requested software
   - Compiles all components
   - Creates bootable ISO
   - Returns download link

**Security**:
- Sandboxed Docker builds (no network access during compilation)
- Checksum verification of all downloads
- Static analysis before execution
- Virus scanning of final artifacts
- Digital signature of packages

**Monetization**:
- Simple build (single binary): $4.99
- Complex build (multi-component): $14.99
- Custom package with installer: $29.99
- Full software bundle: $99.99

### 8. **WaybackAgent** ⚠️ (PRIORITY 2)
Search historical web snapshots, download archived pages, create time-series analyses.

**Core Methods**:
```python
async def search_snapshots(url: str, year: Optional[int]) -> List[Snapshot]
async def get_closest_snapshot(url: str, timestamp: str) -> Snapshot
async def download_snapshot(url: str, timestamp: str) -> ArchivedPage
async def compare_snapshots(url: str, timestamps: List[str]) -> ComparisonReport
```

### 9. **ViewsAnalyticsAgent** ⚠️ (PRIORITY 2)
Track item popularity, analyze trends, generate reports.

**Core Methods**:
```python
async def get_views(identifier: str, range: str) -> ViewsData
async def trending_items(category: str, timeframe: str) -> List[TrendingItem]
async def generate_analytics_report(filters: dict) -> AnalyticsReport
```

### 10. **ReviewsAgent** ⚠️ (PRIORITY 2)
Manage user reviews, ratings, sentiment analysis.

**Core Methods**:
```python
async def get_reviews(identifier: str) -> List[Review]
async def add_review(identifier: str, review: ReviewData) -> Review
async def analyze_sentiment(identifier: str) -> SentimentReport
```

### 11. **RelationshipsAgent** ⚠️ (PRIORITY 3)
Manage item relationships, build knowledge graphs.

**Core Methods**:
```python
async def get_relationships(identifier: str) -> RelationshipGraph
async def add_relationship(parent: str, child: str, type: str) -> Relationship
async def find_related_items(identifier: str, depth: int) -> List[Item]
```

### 12. **TasksMonitorAgent** ⚠️ (PRIORITY 3)
Monitor background tasks, track processing status.

**Core Methods**:
```python
async def get_task_status(task_id: str) -> TaskStatus
async def list_tasks(filters: dict) -> List[Task]
async def cancel_task(task_id: str) -> bool
```

### 13. **OCRProcessorAgent** ⚠️ (PRIORITY 3)
Extract text from images/PDFs, improve searchability.

**Core Methods**:
```python
async def ocr_document(identifier: str, language: str) -> OCRResult
async def extract_text(file_path: Path) -> str
async def create_searchable_pdf(identifier: str) -> SearchablePDF
```

═══════════════════════════════════════════════════════════════════
## 🎨 FRONTEND SPECIFICATIONS (Next.js 16.2 + React 19.2)
═══════════════════════════════════════════════════════════════════

### **Tech Stack**
```json
{
  "framework": "Next.js 16.2 (App Router)",
  "ui_library": "React 19.2",
  "styling": "Tailwind CSS 4.2.4 (CSS-only config)",
  "components": "shadcn/ui v4",
  "state": "Zustand 5.0",
  "data_fetching": "TanStack Query v5",
  "forms": "React Hook Form + Zod",
  "animations": "motion (Framer Motion)",
  "charts": "Recharts",
  "tables": "TanStack Table v8",
  "auth": "NextAuth.js v5",
  "icons": "Lucide React",
  "fonts": "Space Grotesk (headings) + Inter (body)"
}
```

### **Core Pages & Features**

#### 1. **Universal Search Page** (`/search`)
```tsx
// Real-time search across ALL content types
<SearchInterface>
  <SearchBar
    placeholder="Search 40M+ items..."
    filters={[
      "Books", "Games", "Software", "APKs", "Videos",
      "Audio", "Images", "Web Archives", "All"
    ]}
    suggestions={realTimeSuggestions}
  />
  <FilterPanel>
    <YearRange />
    <Language />
    <License />
    <FileFormat />
    <MinDownloads />
  </FilterPanel>
  <ResultsGrid layout={grid|list|cards}>
    {results.map(item => (
      <ResultCard
        thumbnail={item.thumbnail}
        title={item.title}
        type={item.mediatype}
        downloads={item.downloads}
        rating={item.rating}
        actions={[
          "Preview",
          "Download",
          "Add to Collection",
          "Build Package"
        ]}
      />
    ))}
  </ResultsGrid>
</SearchInterface>
```

#### 2. **Content Preview Modal** (Universal Previewer)
```tsx
<PreviewModal item={selectedItem}>
  {/* Renders appropriate preview based on content type */}
  {item.type === "book" && <PDFViewer />}
  {item.type === "video" && <VideoPlayer />}
  {item.type === "audio" && <AudioPlayer />}
  {item.type === "game" && <EmulatorPreview />}
  {item.type === "software" && <SoftwareDetails />}
  
  <MetadataPanel>
    <Title>{item.title}</Title>
    <Description>{item.description}</Description>
    <Stats downloads={} views={} rating={} />
    <Tags tags={item.tags} />
  </MetadataPanel>
  
  <ActionBar>
    <Button onClick={download}>Download</Button>
    <Button onClick={addToCollection}>Add to Collection</Button>
    <Button onClick={buildPackage}>Build Package</Button>
    <Button onClick={share}>Share</Button>
  </ActionBar>
</PreviewModal>
```

#### 3. **Download Manager** (`/downloads`)
```tsx
<DownloadManager>
  <ActiveDownloads>
    {activeDownloads.map(dl => (
      <DownloadCard
        filename={dl.filename}
        progress={dl.progress}
        speed={dl.speed}
        eta={dl.eta}
        status={dl.status}
        onPause={pauseDownload}
        onCancel={cancelDownload}
      />
    ))}
  </ActiveDownloads>
  
  <DownloadHistory>
    <DataTable
      columns={["File", "Size", "Date", "Status", "Actions"]}
      data={downloadHistory}
      actions={["Re-download", "Delete", "Open Folder"]}
    />
  </DownloadHistory>
  
  <Settings>
    <MaxConcurrentDownloads />
    <DownloadLocation />
    <BandwidthLimit />
    <AutoExtract />
  </Settings>
</DownloadManager>
```

#### 4. **Collection Builder** (`/collections/builder`)
```tsx
<CollectionBuilder>
  <DragDropZone>
    <SelectedItems
      items={selectedItems}
      onReorder={reorderItems}
      onRemove={removeItem}
    />
  </DragDropZone>
  
  <CollectionSettings>
    <Input label="Collection Name" />
    <Textarea label="Description" />
    <Select label="Category" options={categories} />
    <Input label="Price" type="number" prefix="$" />
    <ImageUpload label="Cover Image" />
  </CollectionSettings>
  
  <PreviewPanel>
    <CollectionPreview collection={currentCollection} />
    <EstimatedRevenue price={price} estimatedSales={100} />
  </PreviewPanel>
  
  <ActionBar>
    <Button onClick={saveDraft}>Save Draft</Button>
    <Button onClick={publish}>Publish Collection</Button>
  </ActionBar>
</CollectionBuilder>
```

#### 5. **Course Creator** (`/courses/create`)
```tsx
<CourseCreator>
  <CourseOutline>
    <ModuleList>
      {modules.map((module, idx) => (
        <Module
          title={module.title}
          lessons={module.lessons}
          onAddLesson={addLesson}
          onReorder={reorderLessons}
        />
      ))}
    </ModuleList>
    <Button onClick={addModule}>+ Add Module</Button>
  </CourseOutline>
  
  <LessonEditor>
    <ContentBlocks>
      <TextBlock />
      <VideoBlock />
      <CodeBlock />
      <QuizBlock />
      <ResourceBlock />
    </ContentBlocks>
  </LessonEditor>
  
  <CourseSettings>
    <Input label="Course Title" />
    <RichTextEditor label="Description" />
    <Select label="Category" />
    <Select label="Difficulty" options={["Beginner", "Intermediate", "Advanced"]} />
    <Input label="Price" type="number" prefix="$" />
    <DurationEstimate auto={true} />
  </CourseSettings>
</CourseCreator>
```

#### 6. **Admin Dashboard** (`/admin`)
```tsx
<AdminDashboard>
  <StatsGrid>
    <StatCard title="Total Revenue" value="$127,543" change="+23%" />
    <StatCard title="Active Users" value="5,432" change="+12%" />
    <StatCard title="Downloads" value="234,567" change="+45%" />
    <StatCard title="Collections" value="1,234" change="+8%" />
  </StatsGrid>
  
  <RevenueChart data={revenueData} />
  
  <RecentActivity>
    <ActivityFeed items={recentActivities} />
  </RecentActivity>
  
  <TopItems>
    <RankingTable
      items={topItems}
      columns={["Item", "Downloads", "Revenue", "Rating"]}
    />
  </TopItems>
</AdminDashboard>
```

#### 7. **User Profile** (`/profile`)
```tsx
<UserProfile>
  <ProfileHeader
    avatar={user.avatar}
    name={user.name}
    email={user.email}
    joinDate={user.joinDate}
  />
  
  <TabsContainer>
    <Tab label="My Downloads">
      <DownloadsList items={userDownloads} />
    </Tab>
    <Tab label="My Collections">
      <CollectionsGrid collections={userCollections} />
    </Tab>
    <Tab label="My Courses">
      <CoursesList courses={userCourses} />
    </Tab>
    <Tab label="Purchase History">
      <PurchaseHistory transactions={userTransactions} />
    </Tab>
    <Tab label="Settings">
      <SettingsForm user={user} />
    </Tab>
  </TabsContainer>
</UserProfile>
```

═══════════════════════════════════════════════════════════════════
## 🗄️ DATABASE SCHEMA (PostgreSQL 18.3 + pgvector)
═══════════════════════════════════════════════════════════════════

```sql
-- Users & Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- argon2id
    name VARCHAR(255),
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user',  -- user, admin, moderator
    subscription_tier VARCHAR(50) DEFAULT 'free',  -- free, basic, pro, enterprise
    stripe_customer_id VARCHAR(255) UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- API Keys (for programmatic access)
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    permissions JSONB DEFAULT '{}',
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Internet Archive Items (cached metadata)
CREATE TABLE ia_items (
    identifier VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    mediatype VARCHAR(50) NOT NULL,  -- texts, movies, audio, software, etree, image
    creator VARCHAR(255),
    publisher VARCHAR(255),
    date DATE,
    language VARCHAR(10),
    subject TEXT[],
    downloads INTEGER DEFAULT 0,
    item_size BIGINT,  -- bytes
    format VARCHAR(50),
    license VARCHAR(100),
    thumbnail_url TEXT,
    metadata JSONB,  -- Full IA metadata
    embedding vector(1536),  -- For semantic search (pgvector)
    indexed_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User Downloads History
CREATE TABLE downloads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ia_identifier VARCHAR(255) REFERENCES ia_items(identifier),
    filename TEXT NOT NULL,
    file_size BIGINT,
    download_url TEXT,
    status VARCHAR(50) DEFAULT 'pending',  -- pending, downloading, completed, failed
    progress INTEGER DEFAULT 0,  -- percentage
    speed BIGINT,  -- bytes/sec
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Collections (bundles of items)
CREATE TABLE collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    cover_image_url TEXT,
    price DECIMAL(10, 2) DEFAULT 0.00,
    stripe_product_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    is_public BOOLEAN DEFAULT FALSE,
    downloads_count INTEGER DEFAULT 0,
    revenue DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Collection Items (many-to-many)
CREATE TABLE collection_items (
    collection_id UUID REFERENCES collections(id) ON DELETE CASCADE,
    ia_identifier VARCHAR(255) REFERENCES ia_items(identifier),
    position INTEGER NOT NULL,
    PRIMARY KEY (collection_id, ia_identifier)
);

-- Courses
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    difficulty VARCHAR(50),  -- beginner, intermediate, advanced
    cover_image_url TEXT,
    price DECIMAL(10, 2) DEFAULT 0.00,
    stripe_product_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    estimated_duration INTEGER,  -- minutes
    is_public BOOLEAN DEFAULT FALSE,
    enrollments_count INTEGER DEFAULT 0,
    revenue DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Course Modules
CREATE TABLE course_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    position INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Course Lessons
CREATE TABLE course_lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID REFERENCES course_modules(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,  -- Rich text / Markdown
    video_url TEXT,
    duration INTEGER,  -- minutes
    position INTEGER NOT NULL,
    resources JSONB DEFAULT '[]',  -- Links to IA items
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Purchases
CREATE TABLE purchases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    item_type VARCHAR(50) NOT NULL,  -- collection, course, single_item
    item_id UUID NOT NULL,  -- References collection or course
    amount DECIMAL(10, 2) NOT NULL,
    stripe_payment_intent_id VARCHAR(255),
    stripe_checkout_session_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',  -- pending, completed, refunded
    purchased_at TIMESTAMPTZ DEFAULT NOW()
);

-- License Keys (for software/games)
CREATE TABLE license_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    purchase_id UUID REFERENCES purchases(id) ON DELETE CASCADE,
    license_key VARCHAR(255) UNIQUE NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    item_id UUID NOT NULL,
    activations_count INTEGER DEFAULT 0,
    max_activations INTEGER DEFAULT 3,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Build Jobs (AutoBuilderAgent)
CREATE TABLE build_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ia_identifier VARCHAR(255),
    build_request TEXT NOT NULL,  -- Natural language request
    source_language VARCHAR(50),
    target_platform VARCHAR(50),
    build_config JSONB,
    status VARCHAR(50) DEFAULT 'queued',  -- queued, building, testing, completed, failed
    progress INTEGER DEFAULT 0,
    log_output TEXT,
    artifact_url TEXT,
    artifact_size BIGINT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agent Tasks (generic background tasks)
CREATE TABLE agent_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent_type VARCHAR(100) NOT NULL,  -- book_rebrander, game_emulator, etc.
    task_type VARCHAR(100) NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',  -- pending, running, completed, failed
    result JSONB,
    error TEXT,
    celery_task_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reviews & Ratings
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ia_identifier VARCHAR(255) REFERENCES ia_items(identifier),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR(255),
    body TEXT,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, ia_identifier)
);

-- Analytics Events
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,  -- search, view, download, purchase, etc.
    event_data JSONB NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe_customer ON users(stripe_customer_id);
CREATE INDEX idx_ia_items_mediatype ON ia_items(mediatype);
CREATE INDEX idx_ia_items_downloads ON ia_items(downloads DESC);
CREATE INDEX idx_ia_items_embedding ON ia_items USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_downloads_user ON downloads(user_id);
CREATE INDEX idx_downloads_status ON downloads(status);
CREATE INDEX idx_collections_user ON collections(user_id);
CREATE INDEX idx_collections_public ON collections(is_public) WHERE is_public = TRUE;
CREATE INDEX idx_courses_user ON courses(user_id);
CREATE INDEX idx_courses_public ON courses(is_public) WHERE is_public = TRUE;
CREATE INDEX idx_purchases_user ON purchases(user_id);
CREATE INDEX idx_build_jobs_user ON build_jobs(user_id);
CREATE INDEX idx_build_jobs_status ON build_jobs(status);
CREATE INDEX idx_agent_tasks_user ON agent_tasks(user_id);
CREATE INDEX idx_agent_tasks_status ON agent_tasks(status);
CREATE INDEX idx_reviews_item ON reviews(ia_identifier);
CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_created ON analytics_events(created_at DESC);
```

═══════════════════════════════════════════════════════════════════
## 🔐 AUTHENTICATION & AUTHORIZATION
═══════════════════════════════════════════════════════════════════

### **JWT Authentication (RS256)**
```python
# backend/core/auth.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Use argon2id (OWASP 2026 recommended)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
security = HTTPBearer()

# RS256 keys (generate with openssl)
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
<YOUR_PRIVATE_KEY_HERE>
-----END PRIVATE KEY-----"""

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
<YOUR_PUBLIC_KEY_HERE>
-----END PUBLIC KEY-----"""

def create_access_token(user_id: str, email: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Role-based access control
def require_role(required_role: str):
    def role_checker(payload: dict = Depends(verify_token)):
        user_role = payload.get("role")
        if user_role != required_role and user_role != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return payload
    return role_checker
```

### **Registration & Login Endpoints**
```python
# backend/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from backend.core.auth import hash_password, verify_password, create_access_token
from backend.core.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        name=req.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate token
    token = create_access_token(str(user.id), user.email, user.role)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }

@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token
    token = create_access_token(str(user.id), user.email, user.role)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }
```

═══════════════════════════════════════════════════════════════════
## 💳 STRIPE INTEGRATION (Complete Implementation)
═══════════════════════════════════════════════════════════════════

```python
# backend/core/stripe_client.py
import stripe
from typing import Optional, Dict, Any
from pydantic import BaseModel

stripe.api_key = "sk_test_YOUR_STRIPE_SECRET_KEY"

class StripeClient:
    
    async def create_customer(self, email: str, name: str, user_id: str) -> stripe.Customer:
        """Create Stripe customer"""
        customer = stripe.Customer.create(
            email=email,
            name=name,
            metadata={"user_id": user_id}
        )
        return customer
    
    async def create_product(
        self,
        name: str,
        description: str,
        metadata: Dict[str, Any]
    ) -> stripe.Product:
        """Create Stripe product"""
        product = stripe.Product.create(
            name=name,
            description=description,
            metadata=metadata
        )
        return product
    
    async def create_price(
        self,
        product_id: str,
        amount: int,  # in cents
        currency: str = "usd"
    ) -> stripe.Price:
        """Create Stripe price"""
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount,
            currency=currency
        )
        return price
    
    async def create_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        metadata: Dict[str, Any]
    ) -> stripe.checkout.Session:
        """Create checkout session"""
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
        return session
    
    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Dict[str, Any]
    ) -> stripe.Subscription:
        """Create subscription"""
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            metadata=metadata
        )
        return subscription
    
    async def verify_webhook(
        self,
        payload: bytes,
        sig_header: str,
        webhook_secret: str
    ) -> stripe.Event:
        """Verify webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return event
        except ValueError:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise Exception("Invalid signature")
    
    async def handle_checkout_completed(
        self,
        session: stripe.checkout.Session,
        db: Session
    ):
        """Handle successful checkout"""
        # Extract metadata
        user_id = session.metadata.get("user_id")
        item_type = session.metadata.get("item_type")
        item_id = session.metadata.get("item_id")
        
        # Create purchase record
        purchase = Purchase(
            user_id=user_id,
            item_type=item_type,
            item_id=item_id,
            amount=session.amount_total / 100,  # Convert from cents
            stripe_payment_intent_id=session.payment_intent,
            stripe_checkout_session_id=session.id,
            status="completed"
        )
        db.add(purchase)
        
        # Generate license key if applicable
        if item_type in ["collection", "course"]:
            license_key = generate_license_key()
            license = LicenseKey(
                user_id=user_id,
                purchase_id=purchase.id,
                license_key=license_key,
                item_type=item_type,
                item_id=item_id
            )
            db.add(license)
        
        db.commit()
        
        # Send confirmation email
        await send_purchase_confirmation_email(user_id, purchase.id)
```

### **Webhook Handler**
```python
# backend/api/routes/webhooks.py
from fastapi import APIRouter, Request, HTTPException
from backend.core.stripe_client import StripeClient
from backend.core.database import get_db

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])
stripe_client = StripeClient()

@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = "whsec_YOUR_WEBHOOK_SECRET"
    
    try:
        event = await stripe_client.verify_webhook(payload, sig_header, webhook_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Handle events
    if event.type == "checkout.session.completed":
        session = event.data.object
        async with get_db() as db:
            await stripe_client.handle_checkout_completed(session, db)
    
    elif event.type == "customer.subscription.created":
        subscription = event.data.object
        # Handle subscription created
    
    elif event.type == "customer.subscription.deleted":
        subscription = event.data.object
        # Handle subscription cancelled
    
    return {"status": "success"}
```

═══════════════════════════════════════════════════════════════════
## 🚀 DEPLOYMENT & INFRASTRUCTURE
═══════════════════════════════════════════════════════════════════

### **Docker Compose (Development)**
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg18
    environment:
      POSTGRES_DB: prometheus_archive
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7.4-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/prometheus_archive
      REDIS_URL: redis://redis:6379
      IA_ACCESS_KEY: ${IA_ACCESS_KEY}
      IA_SECRET_KEY: ${IA_SECRET_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      STRIPE_API_KEY: ${STRIPE_API_KEY}
      STRIPE_WEBHOOK_SECRET: ${STRIPE_WEBHOOK_SECRET}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
  
  celery_worker:
    build: ./backend
    command: celery -A backend.tasks.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/prometheus_archive
      REDIS_URL: redis://redis:6379
      IA_ACCESS_KEY: ${IA_ACCESS_KEY}
      IA_SECRET_KEY: ${IA_SECRET_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
  
  celery_beat:
    build: ./backend
    command: celery -A backend.tasks.celery_app beat --loglevel=info
    environment:
      REDIS_URL: redis://redis:6379
    depends_on:
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

### **Kubernetes (Production)**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-archive-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prometheus-archive-backend
  template:
    metadata:
      labels:
        app: prometheus-archive-backend
    spec:
      containers:
      - name: backend
        image: rjbizsolution23-wq/prometheus-archive-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: prometheus-archive-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: prometheus-archive-secrets
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-archive-backend
spec:
  selector:
    app: prometheus-archive-backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

═══════════════════════════════════════════════════════════════════
## 📊 MONITORING & OBSERVABILITY
═══════════════════════════════════════════════════════════════════

```python
# backend/core/monitoring.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request
import time

# Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"]
)

ACTIVE_USERS = Gauge(
    "active_users_total",
    "Number of active users"
)

DOWNLOADS_TOTAL = Counter(
    "downloads_total",
    "Total downloads",
    ["mediatype"]
)

BUILD_JOBS_TOTAL = Counter(
    "build_jobs_total",
    "Total build jobs",
    ["status"]
)

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

@router.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

═══════════════════════════════════════════════════════════════════
## 🎯 IMPLEMENTATION ROADMAP
═══════════════════════════════════════════════════════════════════

### **Phase 1: Core Infrastructure (Week 1-2)**
- [x] Database schema & models
- [x] Authentication & JWT
- [x] Basic API routes
- [ ] Redis caching layer
- [ ] Celery workers setup
- [ ] Basic frontend shell

### **Phase 2: Essential Agents (Week 3-4)**
- [x] BookRebranderAgent
- [x] GameEmulatorAgent
- [x] SoftwareManagerAgent
- [x] APKManagerAgent
- [ ] **AutoBuilderAgent** (CRITICAL)
- [ ] VideoMoviesAgent
- [ ] AudioMusicAgent

### **Phase 3: UI & UX (Week 5-6)**
- [ ] Universal search interface
- [ ] Content preview modal
- [ ] Download manager
- [ ] Collection builder
- [ ] Course creator
- [ ] User profile

### **Phase 4: Monetization (Week 7-8)**
- [ ] Complete Stripe integration
- [ ] License key system
- [ ] Subscription management
- [ ] Admin dashboard
- [ ] Revenue analytics

### **Phase 5: Advanced Agents (Week 9-10)**
- [ ] WaybackAgent
- [ ] ViewsAnalyticsAgent
- [ ] ReviewsAgent
- [ ] RelationshipsAgent
- [ ] TasksMonitorAgent
- [ ] OCRProcessorAgent

### **Phase 6: Polish & Launch (Week 11-12)**
- [ ] Performance optimization
- [ ] Security audit
- [ ] Load testing
- [ ] Documentation
- [ ] Marketing site
- [ ] Production deployment

═══════════════════════════════════════════════════════════════════
## 🔥 CRITICAL SUCCESS FACTORS
═══════════════════════════════════════════════════════════════════

1. **AutoBuilderAgent MUST be implemented first** - This is the killer feature
2. **UI/UX MUST be exceptional** - Professional, fast, intuitive
3. **Search MUST be instant** - Cached metadata, vector embeddings
4. **Downloads MUST be reliable** - Resume support, parallel downloads
5. **Monetization MUST be frictionless** - One-click checkout
6. **Security MUST be uncompromising** - OWASP 2026 compliant

═══════════════════════════════════════════════════════════════════
## 📝 USAGE INSTRUCTIONS FOR THIS PROMPT
═══════════════════════════════════════════════════════════════════

**To build this system, feed this ENTIRE prompt to:**
- Claude Opus 4.7 (recommended)
- GPT-4o
- Gemini Pro 2.0
- Any LLM with 200K+ context window

**Command:**
```
Build the complete Prometheus Archive Engine v3.0 system as specified.
Start with Phase 1 (database + auth), then implement AutoBuilderAgent,
then build the frontend. Use the exact tech stack specified.
Generate ALL code files, configs, and documentation.
```

**The LLM will generate:**
- Complete backend (FastAPI + agents)
- Complete frontend (Next.js + React)
- Database migrations
- Docker configs
- Kubernetes manifests
- CI/CD pipelines
- Documentation
- Tests

═══════════════════════════════════════════════════════════════════
## 🎖️ EXPECTED OUTCOMES
═══════════════════════════════════════════════════════════════════

**Upon completion, you will have:**
✅ Production-ready SaaS platform  
✅ 13 specialized AI agents  
✅ Professional UI for ALL content types  
✅ Complete monetization system  
✅ Scalable infrastructure  
✅ Comprehensive documentation  
✅ **The ability to build ANYTHING from Internet Archive**

**Revenue Potential:** $68K-$340K/month at full capacity

**Competitive Advantage:** ONLY platform that auto-builds from source

═══════════════════════════════════════════════════════════════════
🔥 END OF PROMPT - READY TO BUILD
═══════════════════════════════════════════════════════════════════
