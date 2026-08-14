# Internet Archive API Complete Reference

**Comprehensive documentation for ALL Internet Archive APIs**

---

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Search APIs](#search-apis)
- [Storage APIs (IAS3)](#storage-apis-ias3)
- [Metadata APIs](#metadata-apis)
- [Wayback Machine APIs](#wayback-machine-apis)
- [Task APIs](#task-apis)
- [Additional APIs](#additional-apis)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

---

## Overview

The Internet Archive provides 15+ RESTful APIs for accessing and managing its collections. All APIs return JSON by default (unless specified otherwise) and follow REST principles.

**Base URLs:**
- Main API: `https://archive.org`
- S3 Storage: `https://s3.us.archive.org`
- Wayback CDX: `https://web.archive.org/cdx/search/cdx`
- Backend API: `https://be-api.us.archive.org`

---

## Authentication

### S3 Keys (Recommended for Programmatic Access)

Get your keys at: https://archive.org/account/s3.php

**Header Format:**
```
Authorization: LOW <access_key>:<secret_key>
```

**Python Example:**
```python
headers = {
    'Authorization': f'LOW {access_key}:{secret_key}'
}
```

### HTTP Cookies (Browser-Based)

For interactive sessions, use Internet Archive cookies:
- `logged-in-user`
- `logged-in-sig`

**Security:** ALWAYS use HTTPS when transmitting credentials.

---

## Search APIs

### 1. Advanced Search API

**Endpoint:** `GET https://archive.org/advancedsearch.php`

**Parameters:**
- `q` (required): Query string (Lucene syntax)
- `output`: Response format (`json`, `xml`, `csv`, `atom`)
- `rows`: Results per page (default: 50, max: 10000)
- `page`: Page number (1-indexed)
- `fl[]`: Fields to return (repeatable)
- `sort[]`: Sort fields (repeatable)

**Query Syntax:**
```
# Simple keyword
title:NASA

# Boolean operators
title:NASA AND mediatype:movies

# Field search
collection:nasa AND year:2020

# Wildcards
title:space*

# Phrase search
title:"space exploration"

# Range search
year:[2010 TO 2020]

# Negation
collection:nasa NOT mediatype:audio
```

**Example Request:**
```bash
curl "https://archive.org/advancedsearch.php?q=collection:nasa+AND+mediatype:movies&fl[]=identifier&fl[]=title&output=json&rows=10"
```

**Response:**
```json
{
  "responseHeader": {
    "status": 0,
    "QTime": 123
  },
  "response": {
    "numFound": 12845,
    "start": 0,
    "docs": [
      {
        "identifier": "nasa_video_001",
        "title": "Apollo 11 Moon Landing"
      }
    ]
  }
}
```

**Limitations:**
- Maximum 10,000 sorted paged results
- Use Scraping API for deeper pagination

---

### 2. Scraping API (Deep Pagination)

**Endpoint:** `GET https://archive.org/services/search/v1/scrape`

**Parameters:**
- `q` (required): Query string
- `fields`: Comma-separated fields
- `sorts`: Comma-separated sort fields
- `count`: Results per request (min: 100)
- `cursor`: Pagination cursor
- `total_only`: Return only total count (`true`/`false`)

**Example Request:**
```bash
curl "https://archive.org/services/search/v1/scrape?q=collection:nasa&fields=title,identifier&count=100"
```

**Response:**
```json
{
  "items": [
    {"identifier": "item1", "title": "Title 1"},
    {"identifier": "item2", "title": "Title 2"}
  ],
  "count": 100,
  "total": 12845,
  "cursor": "W3siaWRlbnRpZmllciI6Iml0ZW0xMDAifV0="
}
```

**Pagination Pattern:**
```python
cursor = None
while True:
    params = {'q': query, 'count': 100}
    if cursor:
        params['cursor'] = cursor
    
    response = requests.get(url, params=params).json()
    
    for item in response['items']:
        process(item)
    
    cursor = response.get('cursor')
    if not cursor:
        break
```

---

## Storage APIs (IAS3)

### 3. S3-Like API

**Endpoint:** `https://s3.us.archive.org`

#### Upload File (PUT)

**URL Pattern:** `PUT https://s3.us.archive.org/{bucket}/{filename}`

**Headers:**
- `Authorization: LOW access:secret` (required)
- `x-archive-auto-make-bucket: 1` - Auto-create item
- `x-archive-queue-derive: 1` - Queue derivatives
- `x-archive-meta-{field}: {value}` - Set metadata
- `x-archive-size-hint: {bytes}` - Size hint for optimization
- `x-archive-keep-old-version: 1` - Version control

**Example:**
```bash
curl -X PUT \
  -H "Authorization: LOW mykey:mysecret" \
  -H "x-archive-auto-make-bucket: 1" \
  -H "x-archive-meta-title: My Video" \
  -H "x-archive-meta-mediatype: movies" \
  -H "x-archive-queue-derive: 1" \
  --data-binary @video.mp4 \
  https://s3.us.archive.org/my-item/video.mp4
```

**Response:**
```
HTTP/1.1 200 OK
```

#### Download File (GET)

**URL Pattern:** `GET https://archive.org/download/{identifier}/{filename}`

**Example:**
```bash
curl https://archive.org/download/my-item/video.mp4 -o video.mp4
```

**Alternative (S3):**
```bash
curl https://s3.us.archive.org/my-item/video.mp4 -o video.mp4
```

#### Delete File (DELETE)

**URL Pattern:** `DELETE https://s3.us.archive.org/{bucket}/{filename}`

**Example:**
```bash
curl -X DELETE \
  -H "Authorization: LOW mykey:mysecret" \
  https://s3.us.archive.org/my-item/old-file.mp4
```

**Note:** Cannot delete buckets (items), only files.

#### Check Upload Limits

**Endpoint:** `GET https://s3.us.archive.org/?check_limit=1&accesskey={key}&bucket={bucket}`

**Response:**
```json
{
  "over_limit": 0,
  "bucket": "my-item",
  "detail": "Queue ready"
}
```

**Values:**
- `over_limit: 0` - Ready for uploads
- `over_limit: 1` - Queue overloaded, expect 503 errors

---

## Metadata APIs

### 4. Metadata Read API

**Endpoint:** `GET https://archive.org/metadata/{identifier}`

**Parameters:**
- `callback`: JSONP callback function

**Example:**
```bash
curl https://archive.org/metadata/nasa_video_001
```

**Response:**
```json
{
  "created": 1234567890,
  "d1": "ia600100.us.archive.org",
  "d2": "ia700100.us.archive.org",
  "dir": "/1/items/nasa_video_001",
  "files": [
    {
      "name": "video.mp4",
      "source": "original",
      "format": "MPEG4",
      "size": "123456789",
      "md5": "abc123...",
      "crc32": "12345678",
      "sha1": "def456..."
    }
  ],
  "metadata": {
    "identifier": "nasa_video_001",
    "title": "Apollo 11 Landing",
    "mediatype": "movies",
    "description": "Moon landing footage",
    "collection": ["nasa", "movies"],
    "creator": "NASA",
    "date": "1969-07-20",
    "subject": ["space", "moon", "apollo"],
    "language": "eng"
  },
  "server": "ia600100.us.archive.org",
  "uniq": 123456789,
  "workable_servers": ["ia600100.us.archive.org", "ia700100.us.archive.org"]
}
```

---

### 5. Metadata Write API

**Endpoint:** `POST https://archive.org/metadata/{identifier}`

**Authentication:** Required (S3 keys or cookies)

#### Simple Update

**Parameters:**
- `-target`: Target section (default: `metadata`)
- `-patch`: JSON patch operations (RFC 6902)

**Example (Add/Update Fields):**
```bash
curl -X POST \
  -H "Authorization: LOW mykey:mysecret" \
  -d '-patch=[{"op":"add","path":"/metadata/title","value":"New Title"}]' \
  https://archive.org/metadata/my-item
```

**Response:**
```json
{
  "success": true,
  "log": "https://catalogd.archive.org/log/1234567890"
}
```

#### JSON Patch Operations

**Add:**
```json
{"op": "add", "path": "/metadata/field", "value": "value"}
```

**Replace:**
```json
{"op": "replace", "path": "/metadata/field", "value": "new_value"}
```

**Remove:**
```json
{"op": "remove", "path": "/metadata/field"}
```

**Batch Update:**
```json
[
  {"op": "add", "path": "/metadata/title", "value": "New Title"},
  {"op": "add", "path": "/metadata/description", "value": "New desc"},
  {"op": "remove", "path": "/metadata/old_field"}
]
```

---

## Wayback Machine APIs

### 6. Availability API

**Endpoint:** `GET https://archive.org/wayback/available`

**Parameters:**
- `url` (required): URL to check
- `timestamp`: Specific timestamp (YYYYMMDDhhmmss)
- `callback`: JSONP callback

**Example:**
```bash
curl "https://archive.org/wayback/available?url=example.com"
```

**Response (Available):**
```json
{
  "archived_snapshots": {
    "closest": {
      "available": true,
      "url": "http://web.archive.org/web/20130919044612/http://example.com/",
      "timestamp": "20130919044612",
      "status": "200"
    }
  }
}
```

**Response (Not Available):**
```json
{
  "archived_snapshots": {}
}
```

---

### 7. CDX Server API

**Endpoint:** `GET https://web.archive.org/cdx/search/cdx`

**Parameters:**
- `url` (required): URL to query
- `matchType`: `exact`, `prefix`, `host`, `domain`
- `limit`: Maximum results
- `from`: Start date (YYYYMMDD)
- `to`: End date (YYYYMMDD)
- `output`: `json`, `csv`, `text`
- `filter`: Filter by status, mimetype, etc.
- `collapse`: Collapse field (deduplicate)
- `fl`: Fields to return

**Example:**
```bash
curl "https://web.archive.org/cdx/search/cdx?url=nasa.gov&output=json&limit=10"
```

**Response:**
```json
[
  ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"],
  ["gov,nasa)/", "20200101120000", "http://nasa.gov/", "text/html", "200", "ABC123", "12345"]
]
```

**Advanced Filtering:**
```bash
# Only 200 responses
?url=nasa.gov&filter=statuscode:200

# HTML only
?url=nasa.gov&filter=mimetype:text/html

# Collapse by digest (unique content)
?url=nasa.gov&collapse=digest
```

---

## Task APIs

### 8. Tasks API

**Endpoint:** `GET https://archive.org/services/tasks.php`

**Categories:**
- `summary`: Total counts
- `catalog`: Active tasks
- `history`: Completed tasks

**Filtering Criteria:**
- `identifier`: Item ID
- `task_id`: Task ID
- `cmd`: Command type
- `submitter`: User
- `priority`: Priority level
- `submittime>`, `submittime<`: Time ranges

**Example (Get Active Tasks):**
```bash
curl "https://archive.org/services/tasks.php?catalog=1&identifier=my-item"
```

**Response:**
```json
{
  "summary": {
    "queued": 5,
    "running": 2,
    "error": 0,
    "paused": 0
  },
  "tasks": [
    {
      "identifier": "my-item",
      "server": "ia800100",
      "command": "derive.php",
      "args": {},
      "task_id": 123456,
      "submittime": "2026-07-11 10:30:00",
      "color": "blue"
    }
  ]
}
```

#### Submit Task

**Endpoint:** `POST https://archive.org/services/tasks.php`

**Parameters:**
- `cmd`: Task command (e.g., `derive.php`)
- `identifier`: Item ID
- `args`: JSON arguments
- `priority`: Priority (0-10)

**Task Types:**
- `derive.php` - Generate derivatives
- `fixer.php` - Fix metadata
- `delete.php` - Delete files
- `rename.php` - Rename files
- `make_dark.php` - Restrict access
- `make_undark.php` - Unrestrict access

**Example:**
```bash
curl -X POST \
  -H "Authorization: LOW mykey:mysecret" \
  -d "cmd=derive.php" \
  -d "identifier=my-item" \
  -d "priority=5" \
  https://archive.org/services/tasks.php
```

#### Check Rate Limits

**Endpoint:** `GET https://archive.org/services/tasks.php?rate_limits=1&cmd={command}`

**Response:**
```json
{
  "user": "myusername",
  "cmd": "derive.php",
  "limit": 100,
  "inflight": 5,
  "blocked": 0
}
```

---

## Additional APIs

### 9. Changes API

**Endpoint:** `GET https://be-api.us.archive.org/changes/{date}`

**Date Format:** YYYY-MM-DD

**Example:**
```bash
curl https://be-api.us.archive.org/changes/2026-07-11
```

---

### 10. Views API

**Endpoint:** `GET https://be-api.us.archive.org/views/v1/item/{identifier}`

**Example:**
```bash
curl https://be-api.us.archive.org/views/v1/item/nasa_video_001
```

**Response:**
```json
{
  "identifier": "nasa_video_001",
  "views": 123456,
  "downloads": 12345
}
```

---

## Error Handling

### Common HTTP Status Codes

- `200 OK` - Success
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Item/file not found
- `429 Too Many Requests` - Rate limited
- `503 Service Unavailable` - Queue overloaded (SlowDown)

### Error Response Format

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {}
}
```

### Retry Logic

**Recommended Pattern:**
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.get(url)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            continue
        
        if response.status_code == 503:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue
        
        response.raise_for_status()
        break
        
    except requests.RequestException as e:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)
```

---

## Rate Limiting

### General Limits

- **Search API**: No hard limit, but be respectful
- **S3 Uploads**: Check with `?check_limit=1`
- **Tasks API**: User-specific quotas
- **Wayback APIs**: Reasonable use encouraged

### Best Practices

1. **Use cursor pagination** for large result sets
2. **Implement exponential backoff** for retries
3. **Check queue status** before bulk uploads
4. **Respect 429 responses** and Retry-After headers
5. **Use compression** (`Accept-Encoding: gzip`)
6. **Cache responses** when appropriate
7. **Batch operations** where possible

### Headers

**Request Headers:**
```
User-Agent: YourApp/1.0 (contact@example.com)
Accept-Encoding: gzip, deflate
```

**Response Headers:**
```
Retry-After: 60
X-Rate-Limit-Remaining: 95
X-Rate-Limit-Reset: 1234567890
```

---

## Metadata Field Reference

### Standard Fields

**Required:**
- `identifier` - Unique item ID (lowercase, alphanumeric, dashes, underscores)
- `mediatype` - Media type (texts, movies, audio, image, software, data, web)

**Recommended:**
- `title` - Item title
- `description` - Item description
- `creator` - Creator/author
- `date` - Creation date (YYYY-MM-DD)
- `subject` - Subject tags (array)
- `language` - Language code (ISO 639-3)
- `collection` - Parent collection(s)

**Optional:**
- `year` - Year (YYYY)
- `publisher` - Publisher
- `contributor` - Contributors
- `rights` - Rights statement
- `licenseurl` - License URL
- `scanner` - Scanner information
- `sponsor` - Sponsor

### System Fields (Read-Only)

- `addeddate` - Date added to IA
- `publicdate` - Date made public
- `updatedate` - Last update date
- `uploader` - User who uploaded
- `backup_location` - Backup node

---

**Last Updated:** 2026-07-11  
**Version:** 1.0.0  
**Author:** RJ PROMETHEUS APEX
