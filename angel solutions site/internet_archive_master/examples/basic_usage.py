"""
Internet Archive Basic Usage Examples
======================================

Simple examples demonstrating core functionality.

Author: RJ PROMETHEUS APEX
Date: 2026-07-11
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ia_client import (
    InternetArchiveClient, IACredentials, SearchQuery,
    ScrapeQuery, TaskCommand
)


def example_1_search():
    """Example 1: Basic search"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Search")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Simple search
    results = client.search("collection:nasa AND mediatype:movies")
    
    print(f"Found {results['response']['numFound']} items")
    
    # Show first 5 results
    for doc in results['response']['docs'][:5]:
        print(f"- {doc.get('identifier')}: {doc.get('title', 'No title')}")


def example_2_scrape():
    """Example 2: Deep scraping with pagination"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Deep Scraping")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Scrape first 50 items
    count = 0
    for item in client.scrape("collection:etree"):
        print(f"{count+1}. {item.get('identifier')}")
        count += 1
        if count >= 50:
            break
    
    print(f"\nScraped {count} items")


def example_3_metadata():
    """Example 3: Get item metadata"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Get Metadata")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # First, search for an item
    results = client.search("collection:nasa")
    if not results['response']['docs']:
        print("No items found")
        return
    
    identifier = results['response']['docs'][0]['identifier']
    print(f"Getting metadata for: {identifier}")
    
    metadata = client.get_metadata(identifier)
    
    # Display metadata
    meta = metadata.get('metadata', {})
    print(f"\nTitle: {meta.get('title', 'N/A')}")
    print(f"Description: {meta.get('description', 'N/A')}")
    print(f"Date: {meta.get('date', 'N/A')}")
    print(f"Creator: {meta.get('creator', 'N/A')}")
    print(f"Media Type: {meta.get('mediatype', 'N/A')}")
    
    # Display files
    files = metadata.get('files', [])
    print(f"\nFiles ({len(files)}):")
    for f in files[:5]:  # First 5 files
        print(f"- {f.get('name')} ({f.get('size', 0)} bytes)")


def example_4_wayback():
    """Example 4: Wayback Machine"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Wayback Machine")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Check if URL is archived
    url = "nasa.gov"
    print(f"Checking Wayback for: {url}")
    
    result = client.check_wayback_availability(url)
    
    if result.get('archived_snapshots'):
        snapshot = result['archived_snapshots']['closest']
        print(f"\n✅ URL is archived!")
        print(f"Wayback URL: {snapshot['url']}")
        print(f"Timestamp: {snapshot['timestamp']}")
        print(f"Status: {snapshot['status']}")
    else:
        print("\n❌ URL not found in Wayback Machine")
    
    # Query CDX for capture history
    print(f"\nQuerying CDX for recent captures...")
    captures = client.query_cdx(url, limit=5)
    
    if captures and len(captures) > 1:
        print(f"Found {len(captures)-1} captures (showing 5):")
        for row in captures[1:]:  # Skip header
            print(f"- {row[1]}: {row[4]}")  # timestamp, status


def example_5_download():
    """Example 5: Download files"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Download Files")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Search for a small item
    results = client.search("collection:opensource_movies")
    if not results['response']['docs']:
        print("No items found")
        return
    
    identifier = results['response']['docs'][0]['identifier']
    print(f"Downloading from: {identifier}")
    
    # Get metadata to see available files
    metadata = client.get_metadata(identifier)
    files = metadata.get('files', [])
    
    # Find a small file (< 1MB)
    small_file = None
    for f in files:
        size = int(f.get('size', 0))
        if size < 1_000_000 and size > 0:  # Between 0 and 1MB
            small_file = f.get('name')
            break
    
    if small_file:
        print(f"Downloading: {small_file}")
        content = client.download_file(identifier, small_file)
        print(f"Downloaded {len(content)} bytes")
    else:
        print("No suitable file found for demo")


def example_6_upload():
    """Example 6: Upload file (requires credentials)"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Upload File (Demo)")
    print("="*60)
    
    # Note: This example shows the code but won't execute without credentials
    
    print("This example requires credentials. Set environment variables:")
    print("  export IA_ACCESS_KEY='your_access_key'")
    print("  export IA_SECRET_KEY='your_secret_key'")
    print("\nExample code:")
    
    code = '''
import os
from core.ia_client import InternetArchiveClient, IACredentials

credentials = IACredentials(
    access_key=os.getenv('IA_ACCESS_KEY'),
    secret_key=os.getenv('IA_SECRET_KEY')
)

client = InternetArchiveClient(credentials=credentials)

# Create a test file
test_content = b"Hello, Internet Archive!"

# Upload to new item
client.upload_file(
    identifier="my-test-item",
    filename="test.txt",
    file_data=test_content,
    metadata={
        "title": "My Test Item",
        "description": "Test upload via API",
        "mediatype": "texts",
        "collection": "test_collection"
    },
    auto_make_bucket=True,
    queue_derive=True
)

print("✅ Upload complete!")
print("View at: https://archive.org/details/my-test-item")
'''
    
    print(code)


def example_7_advanced_search():
    """Example 7: Advanced search with filters"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Advanced Search")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Complex query
    query = SearchQuery(
        query="collection:nasa AND mediatype:movies AND year:2020",
        fields=["identifier", "title", "date", "downloads"],
        rows=10
    )
    
    results = client.search(query)
    
    print(f"Query: {query.query}")
    print(f"Total results: {results['response']['numFound']}")
    print(f"\nTop 10 results:")
    
    for i, doc in enumerate(results['response']['docs'], 1):
        print(f"{i}. {doc.get('title', 'No title')}")
        print(f"   ID: {doc.get('identifier')}")
        print(f"   Date: {doc.get('date', 'N/A')}")
        print(f"   Downloads: {doc.get('downloads', 'N/A')}")
        print()


def example_8_bulk_metadata():
    """Example 8: Bulk metadata retrieval"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Bulk Metadata Retrieval")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Search for items
    results = client.search("collection:opensource_audio")
    identifiers = [doc['identifier'] for doc in results['response']['docs'][:5]]
    
    print(f"Retrieving metadata for {len(identifiers)} items...\n")
    
    for identifier in identifiers:
        metadata = client.get_metadata(identifier)
        meta = metadata.get('metadata', {})
        
        print(f"📦 {identifier}")
        print(f"   Title: {meta.get('title', 'N/A')}")
        print(f"   Files: {len(metadata.get('files', []))}")
        print()


def example_9_faceted_search():
    """Example 9: Faceted search"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Faceted Search")
    print("="*60)
    
    client = InternetArchiveClient()
    
    # Search by year facets
    years = ['2020', '2021', '2022']
    
    print("Searching NASA collection by year:\n")
    
    for year in years:
        query = f"collection:nasa AND year:{year}"
        total = client.get_total_results(query)
        print(f"{year}: {total} items")


def example_10_check_limits():
    """Example 10: Check upload limits"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Check Upload Limits")
    print("="*60)
    
    print("This example requires credentials.")
    print("\nExample code:")
    
    code = '''
from core.ia_client import InternetArchiveClient, IACredentials
import os

credentials = IACredentials(
    access_key=os.getenv('IA_ACCESS_KEY'),
    secret_key=os.getenv('IA_SECRET_KEY')
)

client = InternetArchiveClient(credentials=credentials)

# Check if we can upload to a bucket
limits = client.check_s3_limits("my-bucket-name")

if limits['can_upload']:
    print("✅ Ready for uploads")
else:
    print("⚠️ Queue is overloaded, wait before uploading")
    
print(f"Status: {limits}")
'''
    
    print(code)


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("INTERNET ARCHIVE BASIC USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        example_1_search,
        example_2_scrape,
        example_3_metadata,
        example_4_wayback,
        example_5_download,
        example_6_upload,
        example_7_advanced_search,
        example_8_bulk_metadata,
        example_9_faceted_search,
        example_10_check_limits
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"\n❌ Example {i} failed: {e}")
        
        if i < len(examples):
            input("\nPress Enter to continue...")
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
