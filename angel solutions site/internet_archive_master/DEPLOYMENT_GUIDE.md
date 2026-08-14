# 🚀 Internet Archive Ultimate Master System - Deployment Guide

**Complete step-by-step deployment and usage instructions**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Usage Examples](#usage-examples)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Python**: 3.10 or higher
- **OS**: Linux, macOS, or Windows
- **Memory**: 512MB minimum
- **Disk**: 100MB for installation

### Get API Credentials

1. Create an Internet Archive account at https://archive.org
2. Get your S3 API keys at https://archive.org/account/s3.php
3. Save your `access_key` and `secret_key`

---

## Installation

### Method 1: Automated Deployment (Recommended)

```bash
# Clone repository
git clone https://github.com/rjbizsolution23-wq/internet-archive-master.git
cd internet-archive-master

# Run deployment script
./deploy.sh
```

The script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Install CLI tool
- ✅ Create directories
- ✅ Run tests

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/rjbizsolution23-wq/internet-archive-master.git
cd internet-archive-master

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

---

## Configuration

### Option 1: Interactive Configuration

```bash
ia configure
```

Prompts for:
- Access Key
- Secret Key

Saves to `~/.ia_credentials.json` with secure permissions (600).

### Option 2: Environment Variables

```bash
# Linux/macOS
export IA_ACCESS_KEY="your_access_key_here"
export IA_SECRET_KEY="your_secret_key_here"

# Windows
set IA_ACCESS_KEY=your_access_key_here
set IA_SECRET_KEY=your_secret_key_here
```

### Option 3: Manual Configuration File

Create `~/.ia_credentials.json`:

```json
{
  "access_key": "your_access_key",
  "secret_key": "your_secret_key"
}
```

Set secure permissions:

```bash
chmod 600 ~/.ia_credentials.json
```

---

## Verification

### Test 1: Client Initialization

```python
from core.ia_client import InternetArchiveClient

client = InternetArchiveClient()
print("✅ Client initialized successfully")
```

### Test 2: Search (No Auth Required)

```bash
ia search "collection:nasa" --format table
```

Expected output:
```
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Identifier         ┃ Title                    ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ nasa_video_001     │ Apollo 11 Moon Landing   │
│ ...                │ ...                      │
└────────────────────┴──────────────────────────┘
```

### Test 3: Wayback Machine

```bash
ia wayback-check nasa.gov
```

Expected output:
```
✅ URL is archived!
URL: http://web.archive.org/web/...
Timestamp: 20260711...
Status: 200
```

### Test 4: Metadata Retrieval

```bash
ia metadata gov.archives.arc.1155023
```

Should return complete JSON metadata.

---

## Usage Examples

### Basic Search

```bash
# Simple search
ia search "collection:nasa"

# With filters
ia search "mediatype:movies AND year:2020" -f title -f identifier

# Export to JSON
ia search "subject:AI" --format json --output-file results.json
```

### Deep Scraping (Unlimited Results)

```bash
# Scrape large collections
ia scrape "collection:etree" -m 50000 -o results.jsonl

# Specific fields
ia scrape "mediatype:audio" -f identifier -f title -f date
```

### AI-Powered Search

```bash
# Natural language queries
ia smart-search "videos about space exploration from NASA"
ia smart-search "books about artificial intelligence from 2020"
```

### Metadata Operations

```bash
# Get metadata
ia metadata item-identifier

# Update metadata (requires auth)
ia update-metadata my-item '{"title":"New Title"}'
ia update-metadata my-item @metadata.json
```

### Upload Files

```bash
# Upload single file
ia upload my-item video.mp4 -m '{"title":"My Video","mediatype":"movies"}'

# Upload multiple files
ia upload my-book book.pdf cover.jpg -m @metadata.json

# Skip derivative generation
ia upload my-item file.txt --no-derive
```

### Download Files

```bash
# Download all files from an item
ia download item-identifier

# Download specific files
ia download item-id -f video.mp4 -f subtitles.srt

# Custom output directory
ia download item-id -o /path/to/downloads/
```

### Wayback Machine

```bash
# Check if URL is archived
ia wayback-check example.com

# Check specific timestamp
ia wayback-check nasa.gov --timestamp 20200101

# Analyze complete history
ia wayback-history nasa.gov --from-year 2010 --to-year 2020
```

### Collection Curation

```bash
# Create curated collection
ia create-collection "NASA-Videos" "collection:nasa AND mediatype:movies" --max-items 100

# High quality only
ia create-collection "Premium-Audio" "mediatype:audio" --min-quality 0.9
```

---

## Production Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

ENV IA_ACCESS_KEY=""
ENV IA_SECRET_KEY=""

CMD ["ia", "--help"]
```

Build and run:

```bash
docker build -t ia-master .
docker run -e IA_ACCESS_KEY=$IA_ACCESS_KEY -e IA_SECRET_KEY=$IA_SECRET_KEY ia-master ia search "collection:nasa"
```

### Systemd Service

Create `/etc/systemd/system/ia-worker.service`:

```ini
[Unit]
Description=Internet Archive Worker
After=network.target

[Service]
Type=simple
User=iauser
WorkingDirectory=/opt/ia-master
Environment="IA_ACCESS_KEY=your_key"
Environment="IA_SECRET_KEY=your_secret"
ExecStart=/opt/ia-master/venv/bin/python worker.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ia-worker
sudo systemctl start ia-worker
sudo systemctl status ia-worker
```

### Kubernetes Deployment

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ia-master
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ia-master
  template:
    metadata:
      labels:
        app: ia-master
    spec:
      containers:
      - name: ia-master
        image: ia-master:latest
        env:
        - name: IA_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: ia-credentials
              key: access-key
        - name: IA_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ia-credentials
              key: secret-key
```

Deploy:

```bash
kubectl apply -f deployment.yaml
```

### CI/CD Integration

GitHub Actions example (`.github/workflows/deploy.yml`):

```yaml
name: Deploy IA Master

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .
      
      - name: Run tests
        run: pytest tests/
      
      - name: Deploy to production
        env:
          IA_ACCESS_KEY: ${{ secrets.IA_ACCESS_KEY }}
          IA_SECRET_KEY: ${{ secrets.IA_SECRET_KEY }}
        run: ./deploy.sh
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall package
pip install -e .
```

### Issue: "401 Unauthorized"

**Causes:**
- Invalid credentials
- Expired credentials
- Missing credentials

**Solutions:**
```bash
# Verify credentials
ia configure

# Check environment variables
echo $IA_ACCESS_KEY
echo $IA_SECRET_KEY

# Test with simple operation
ia search "collection:test"  # No auth required
```

### Issue: "429 Too Many Requests"

**Solution:**
- Implement rate limiting in your code
- Use exponential backoff
- Check queue status before operations

```python
import time

client = InternetArchiveClient(credentials=creds)

# Check limits before upload
limits = client.check_s3_limits("my-bucket")
if not limits['can_upload']:
    print("Queue overloaded, waiting...")
    time.sleep(60)
```

### Issue: "503 Service Unavailable (SlowDown)"

**Solution:**
- S3 queue is overloaded
- Wait and retry with exponential backoff
- Check queue status

```bash
# Check queue status
curl "https://s3.us.archive.org/?check_limit=1&accesskey=$IA_ACCESS_KEY&bucket=my-bucket"
```

### Issue: Import errors

**Solution:**
```bash
# Ensure all __init__.py files exist
touch core/__init__.py
touch agents/__init__.py
touch cli/__init__.py

# Reinstall
pip install -e .
```

### Issue: CLI command not found

**Solution:**
```bash
# Ensure package is installed
pip install -e .

# Or use full path
python -m cli.ia_cli search "collection:nasa"
```

---

## Performance Optimization

### 1. Connection Pooling

```python
from core.ia_client import InternetArchiveClient

# Reuse client for multiple operations
client = InternetArchiveClient(credentials=creds)

# Make multiple requests with same session
for identifier in item_list:
    metadata = client.get_metadata(identifier)
```

### 2. Batch Operations

```python
# Instead of individual requests
for item in items:
    client.get_metadata(item)

# Use scraping API
for item in client.scrape("collection:mycollection"):
    # Process in batches
    pass
```

### 3. Parallel Downloads

```python
from concurrent.futures import ThreadPoolExecutor

def download_item(identifier):
    client = InternetArchiveClient()
    return client.download_file(identifier, "file.mp4")

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(download_item, identifiers)
```

---

## Security Best Practices

### 1. Never Commit Credentials

```bash
# Add to .gitignore
echo ".ia_credentials.json" >> .gitignore
echo ".env" >> .gitignore
```

### 2. Use Environment Variables in Production

```bash
# Load from secure vault
export IA_ACCESS_KEY=$(vault read -field=access_key secret/ia)
export IA_SECRET_KEY=$(vault read -field=secret_key secret/ia)
```

### 3. Rotate Keys Regularly

- Generate new keys every 90 days
- Revoke old keys after transition
- Use different keys for dev/staging/prod

### 4. Monitor API Usage

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = InternetArchiveClient(credentials=creds)
logger.info(f"Client initialized for user: {creds.access_key[:5]}...")
```

---

## Support & Resources

### Documentation
- **README**: Complete project overview
- **API Reference**: `/docs/API_REFERENCE.md`
- **Examples**: `/examples/`

### Official Internet Archive Resources
- **Developer Portal**: https://archive.org/developers/
- **Help Center**: https://help.archive.org/
- **Blog**: https://blog.archive.org/

### Community
- **GitHub Issues**: Report bugs and request features
- **Stack Overflow**: Tag questions with `internet-archive`

### Commercial Support
- **Email**: support@rickjeffersonsolutions.com
- **Company**: RJ Business Solutions

---

**Last Updated:** 2026-07-11  
**Version:** 1.0.0  
**Author:** RJ PROMETHEUS APEX  
**Company:** RJ Business Solutions
