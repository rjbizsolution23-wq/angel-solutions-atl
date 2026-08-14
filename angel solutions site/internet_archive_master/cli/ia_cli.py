#!/usr/bin/env python3
"""
Internet Archive Ultimate CLI Tool
===================================
Command-line interface for all IA operations

Author: RJ PROMETHEUS APEX
Version: 1.0.0
Date: 2026-07-11

COMMANDS:
  search       - Search Internet Archive
  scrape       - Deep scrape with pagination
  metadata     - Get/update item metadata
  upload       - Upload files to IA
  download     - Download items
  wayback      - Wayback Machine operations
  tasks        - Task management
  agent        - AI agent operations
  collection   - Collection curation
"""

import click
import json
import os
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich import print as rprint

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ia_client import (
    InternetArchiveClient, IACredentials, SearchQuery,
    ScrapeQuery, TaskCommand, TaskCategory, OutputFormat
)
from agents.ia_agent import (
    IAOrchestratorAgent, IASearchAgent, IACuratorAgent,
    IATimekeeperAgent, CollectionSpec, AgentTask, AgentRole
)

console = Console()


def get_credentials() -> Optional[IACredentials]:
    """Get credentials from environment or config"""
    access_key = os.getenv('IA_ACCESS_KEY')
    secret_key = os.getenv('IA_SECRET_KEY')
    
    if access_key and secret_key:
        return IACredentials(access_key, secret_key)
    
    # Try config file
    config_path = Path.home() / '.ia_credentials.json'
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            return IACredentials(
                config.get('access_key'),
                config.get('secret_key')
            )
    
    return None


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Internet Archive Ultimate CLI Tool
    
    Complete command-line interface for ALL Internet Archive operations.
    """
    pass


# ============================================================================
# SEARCH COMMANDS
# ============================================================================

@cli.command()
@click.argument('query')
@click.option('--fields', '-f', multiple=True, help='Fields to return')
@click.option('--rows', '-r', default=100, help='Results per page')
@click.option('--page', '-p', default=1, help='Page number')
@click.option('--format', '-o', type=click.Choice(['json', 'csv', 'table']), 
              default='table', help='Output format')
@click.option('--output-file', type=click.Path(), help='Save to file')
def search(query, fields, rows, page, format, output_file):
    """
    Search Internet Archive (max 10,000 results)
    
    Examples:
        ia search "collection:nasa"
        ia search "mediatype:movies AND year:2020" -f title -f identifier
        ia search "subject:AI" --format json --output-file results.json
    """
    client = InternetArchiveClient(credentials=get_credentials())
    
    search_query = SearchQuery(
        query=query,
        fields=list(fields) if fields else None,
        rows=rows,
        page=page
    )
    
    console.print(f"[cyan]Searching:[/cyan] {query}")
    
    results = client.search(search_query)
    docs = results['response']['docs']
    total = results['response']['numFound']
    
    console.print(f"[green]Found {total} items[/green]")
    
    if format == 'table':
        table = Table(title=f"Search Results (Page {page})")
        
        if fields:
            for field in fields:
                table.add_column(field.capitalize())
        else:
            table.add_column("Identifier")
            table.add_column("Title")
        
        for doc in docs:
            if fields:
                row = [str(doc.get(f, '')) for f in fields]
            else:
                row = [doc.get('identifier', ''), doc.get('title', '')]
            table.add_row(*row)
        
        console.print(table)
    
    elif format == 'json':
        output = json.dumps(docs, indent=2)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(output)
            console.print(f"[green]Saved to {output_file}[/green]")
        else:
            console.print(output)
    
    elif format == 'csv':
        import csv
        import io
        
        output = io.StringIO()
        if docs:
            writer = csv.DictWriter(output, fieldnames=docs[0].keys())
            writer.writeheader()
            writer.writerows(docs)
        
        csv_output = output.getvalue()
        if output_file:
            with open(output_file, 'w') as f:
                f.write(csv_output)
            console.print(f"[green]Saved to {output_file}[/green]")
        else:
            console.print(csv_output)


@cli.command()
@click.argument('query')
@click.option('--fields', '-f', multiple=True, help='Fields to return')
@click.option('--max-results', '-m', type=int, help='Maximum results')
@click.option('--output-file', '-o', type=click.Path(), help='Save to JSONL file')
def scrape(query, fields, max_results, output_file):
    """
    Deep scrape with unlimited pagination (use for >10K results)
    
    Examples:
        ia scrape "collection:etree" -f identifier -f title -m 50000
        ia scrape "mediatype:audio" -o all_audio.jsonl
    """
    client = InternetArchiveClient(credentials=get_credentials())
    
    scrape_query = ScrapeQuery(
        query=query,
        fields=list(fields) if fields else None,
        count=100
    )
    
    console.print(f"[cyan]Scraping:[/cyan] {query}")
    
    count = 0
    outfile = open(output_file, 'w') if output_file else None
    
    try:
        with Progress() as progress:
            task = progress.add_task("[green]Scraping...", total=max_results or 0)
            
            for item in client.scrape(scrape_query):
                count += 1
                
                if outfile:
                    outfile.write(json.dumps(item) + '\n')
                else:
                    console.print(item)
                
                progress.update(task, advance=1)
                
                if max_results and count >= max_results:
                    break
        
        console.print(f"[green]✅ Scraped {count} items[/green]")
        
        if outfile:
            console.print(f"[green]Saved to {output_file}[/green]")
    
    finally:
        if outfile:
            outfile.close()


# ============================================================================
# METADATA COMMANDS
# ============================================================================

@cli.command()
@click.argument('identifier')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'table']),
              default='json', help='Output format')
def metadata(identifier, format):
    """
    Get item metadata
    
    Examples:
        ia metadata gov.archives.arc.1155023
        ia metadata my-item --format table
    """
    client = InternetArchiveClient(credentials=get_credentials())
    
    console.print(f"[cyan]Fetching metadata for:[/cyan] {identifier}")
    
    metadata = client.get_metadata(identifier)
    
    if format == 'json':
        console.print_json(data=metadata)
    elif format == 'yaml':
        import yaml
        console.print(yaml.dump(metadata, default_flow_style=False))
    elif format == 'table':
        table = Table(title=f"Metadata: {identifier}")
        table.add_column("Field")
        table.add_column("Value")
        
        for key, value in metadata.get('metadata', {}).items():
            table.add_row(key, str(value))
        
        console.print(table)


@cli.command()
@click.argument('identifier')
@click.argument('metadata_json')
def update_metadata(identifier, metadata_json):
    """
    Update item metadata (requires auth)
    
    Examples:
        ia update-metadata my-item '{"title":"New Title"}'
        ia update-metadata my-item @metadata.json
    """
    client = InternetArchiveClient(credentials=get_credentials())
    
    if not client.credentials:
        console.print("[red]❌ Authentication required. Set IA_ACCESS_KEY and IA_SECRET_KEY[/red]")
        return
    
    # Load metadata
    if metadata_json.startswith('@'):
        with open(metadata_json[1:]) as f:
            metadata_dict = json.load(f)
    else:
        metadata_dict = json.loads(metadata_json)
    
    console.print(f"[cyan]Updating metadata for:[/cyan] {identifier}")
    
    result = client.update_metadata(identifier, metadata_dict)
    
    if result.get('success'):
        console.print("[green]✅ Metadata updated successfully[/green]")
    else:
        console.print(f"[red]❌ Update failed: {result}[/red]")


# ============================================================================
# UPLOAD/DOWNLOAD COMMANDS
# ============================================================================

@cli.command()
@click.argument('identifier')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--metadata', '-m', help='Metadata as JSON or @file.json')
@click.option('--no-derive', is_flag=True, help='Skip derivative generation')
def upload(identifier, files, metadata, no_derive):
    """
    Upload files to Internet Archive (requires auth)
    
    Examples:
        ia upload my-item video.mp4 -m '{"title":"My Video","mediatype":"movies"}'
        ia upload my-book book.pdf cover.jpg -m @metadata.json
    """
    client = InternetArchiveClient(credentials=get_credentials())
    
    if not client.credentials:
        console.print("[red]❌ Authentication required[/red]")
        return
    
    # Parse metadata
    metadata_dict = None
    if metadata:
        if metadata.startswith('@'):
            with open(metadata[1:]) as f:
                metadata_dict = json.load(f)
        else:
            metadata_dict = json.loads(metadata)
    
    console.print(f"[cyan]Uploading to:[/cyan] {identifier}")
    
    with Progress() as progress:
        task = progress.add_task("[green]Uploading...", total=len(files))
        
        for filepath in files:
            filename = os.path.basename(filepath)
            console.print(f"📤 {filename}")
            
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            client.upload_file(
                identifier=identifier,
                filename=filename,
                file_data=file_data,
                metadata=metadata_dict if metadata_dict else None,
                queue_derive=not no_derive
            )
            
            progress.update(task, advance=1)
    
    console.print(f"[green]✅ Upload complete: https://archive.org/details/{identifier}[/green]")


@cli.command()
@click.argument('identifier')
@click.option('--output-dir', '-o', type=click.Path(), default='.',
              help='Output directory')
@click.option('--files', '-f', multiple=True, help='Specific files to download')
def download(identifier, output_dir, files):
    """
    Download item files
    
    Examples:
        ia download my-item
        ia download my-item -f video.mp4 -f subtitles.srt
        ia download my-item -o /downloads/
    """
    client = InternetArchiveClient(credentials=get_credentials())
    
    console.print(f"[cyan]Downloading:[/cyan] {identifier}")
    
    # Get metadata to list files
    metadata = client.get_metadata(identifier)
    available_files = metadata.get('files', [])
    
    # Filter files if specified
    if files:
        available_files = [f for f in available_files if f.get('name') in files]
    
    os.makedirs(output_dir, exist_ok=True)
    
    with Progress() as progress:
        task = progress.add_task("[green]Downloading...", total=len(available_files))
        
        for file_info in available_files:
            filename = file_info.get('name')
            if filename:
                console.print(f"📥 {filename}")
                
                content = client.download_file(identifier, filename)
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                progress.update(task, advance=1)
    
    console.print(f"[green]✅ Downloaded {len(available_files)} files to {output_dir}[/green]")


# ============================================================================
# WAYBACK COMMANDS
# ============================================================================

@cli.command()
@click.argument('url')
@click.option('--timestamp', '-t', help='Timestamp (YYYYMMDDhhmmss)')
def wayback_check(url, timestamp):
    """
    Check if URL is in Wayback Machine
    
    Examples:
        ia wayback-check example.com
        ia wayback-check nasa.gov --timestamp 20200101
    """
    client = InternetArchiveClient()
    
    console.print(f"[cyan]Checking Wayback for:[/cyan] {url}")
    
    result = client.check_wayback_availability(url, timestamp=timestamp)
    
    if result.get('archived_snapshots'):
        snapshot = result['archived_snapshots']['closest']
        console.print("[green]✅ URL is archived![/green]")
        console.print(f"URL: {snapshot['url']}")
        console.print(f"Timestamp: {snapshot['timestamp']}")
        console.print(f"Status: {snapshot['status']}")
    else:
        console.print("[yellow]⚠️  URL not found in Wayback Machine[/yellow]")


@cli.command()
@click.argument('url')
@click.option('--from-year', type=int, help='Start year')
@click.option('--to-year', type=int, help='End year')
def wayback_history(url, from_year, to_year):
    """
    Analyze complete Wayback history of URL
    
    Examples:
        ia wayback-history nasa.gov
        ia wayback-history example.com --from-year 2010 --to-year 2020
    """
    client = InternetArchiveClient()
    agent = IATimekeeperAgent(client)
    
    console.print(f"[cyan]Analyzing history:[/cyan] {url}")
    
    with console.status("[bold green]Analyzing..."):
        analysis = agent.analyze_url_history(url, from_year, to_year)
    
    console.print_json(data=analysis)


# ============================================================================
# AGENT COMMANDS
# ============================================================================

@cli.command()
@click.argument('query')
@click.option('--max-results', '-m', default=100, type=int)
def smart_search(query, max_results):
    """
    AI-powered search with natural language understanding
    
    Examples:
        ia smart-search "videos about space from NASA"
        ia smart-search "books about artificial intelligence from 2020"
    """
    client = InternetArchiveClient(credentials=get_credentials())
    agent = IASearchAgent(client)
    
    console.print(f"[cyan]AI Search:[/cyan] {query}")
    
    with console.status("[bold green]Searching..."):
        results = agent.smart_search(query, max_results=max_results)
    
    table = Table(title=f"Results ({len(results)} items)")
    table.add_column("Identifier")
    table.add_column("Title")
    
    for item in results[:20]:  # Show first 20
        table.add_row(
            item.get('identifier', ''),
            item.get('title', '')[:60]
        )
    
    console.print(table)
    
    if len(results) > 20:
        console.print(f"[dim]... and {len(results) - 20} more results[/dim]")


@cli.command()
@click.argument('name')
@click.argument('query')
@click.option('--max-items', '-m', type=int, help='Maximum items')
@click.option('--min-quality', type=float, default=0.7, help='Minimum quality score')
def create_collection(name, query, max_items, min_quality):
    """
    AI-powered collection curation
    
    Examples:
        ia create-collection "NASA-Videos" "collection:nasa AND mediatype:movies"
        ia create-collection "AI-Books" "subject:AI AND mediatype:texts" --max-items 100
    """
    client = InternetArchiveClient(credentials=get_credentials())
    agent = IACuratorAgent(client)
    
    spec = CollectionSpec(
        name=name,
        query=query,
        max_items=max_items,
        min_quality_score=min_quality
    )
    
    console.print(f"[cyan]Creating collection:[/cyan] {name}")
    
    with console.status("[bold green]Curating..."):
        result = agent.create_collection(spec)
    
    console.print(f"[green]✅ Collection created![/green]")
    console.print(f"Total candidates: {result['total_candidates']}")
    console.print(f"Selected items: {result['selected_items']}")
    console.print(f"Avg quality: {result['avg_quality_score']:.2f}")


@cli.command()
def configure():
    """Configure Internet Archive credentials"""
    console.print("[cyan]Internet Archive Configuration[/cyan]\n")
    
    console.print("Get your credentials at: https://archive.org/account/s3.php\n")
    
    access_key = click.prompt("Access Key")
    secret_key = click.prompt("Secret Key", hide_input=True)
    
    config_path = Path.home() / '.ia_credentials.json'
    config = {
        'access_key': access_key,
        'secret_key': secret_key
    }
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    config_path.chmod(0o600)  # Secure permissions
    
    console.print(f"\n[green]✅ Configuration saved to {config_path}[/green]")


if __name__ == '__main__':
    cli()
