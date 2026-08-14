"""
Internet Archive AI Agent System
=================================
Multi-Agent Framework for Intelligent IA Operations

Author: RJ PROMETHEUS APEX
Version: 1.0.0
Date: 2026-07-11

AGENT CAPABILITIES:
- Intelligent search with NLP query understanding
- Automated collection curation
- Bulk operations with smart batching
- Metadata enrichment and validation
- Wayback Machine temporal analysis
- Task orchestration and monitoring
- Anomaly detection and quality assurance
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import json
from datetime import datetime, timedelta
import re

from core.ia_client import (
    InternetArchiveClient, IACredentials, SearchQuery,
    ScrapeQuery, TaskCommand, TaskCategory
)


class AgentRole(Enum):
    """Specialized agent roles"""
    SEARCHER = "searcher"  # Intelligent search operations
    CURATOR = "curator"  # Collection management
    ARCHIVIST = "archivist"  # Upload and preservation
    ANALYST = "analyst"  # Data analysis and insights
    GUARDIAN = "guardian"  # Quality assurance
    TIMEKEEPER = "timekeeper"  # Wayback operations


@dataclass
class AgentTask:
    """Task definition for agents"""
    task_id: str
    role: AgentRole
    operation: str
    parameters: Dict[str, Any]
    priority: int = 5
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class CollectionSpec:
    """Collection specification for curation"""
    name: str
    query: str
    min_quality_score: float = 0.7
    max_items: Optional[int] = None
    metadata_template: Optional[Dict[str, Any]] = None
    auto_enrich: bool = True


class IASearchAgent:
    """Intelligent search agent with NLP understanding"""
    
    def __init__(self, client: InternetArchiveClient):
        self.client = client
        self.role = AgentRole.SEARCHER
    
    def parse_natural_language_query(self, nl_query: str) -> str:
        """
        Convert natural language to IA search syntax
        
        Example:
            "videos about NASA from 2020" -> 
            "collection:nasa AND mediatype:movies AND year:2020"
        """
        query_parts = []
        
        # Media type detection
        media_map = {
            'video': 'movies',
            'movie': 'movies',
            'audio': 'audio',
            'music': 'audio',
            'book': 'texts',
            'text': 'texts',
            'image': 'image',
            'photo': 'image',
            'software': 'software'
        }
        
        for keyword, mediatype in media_map.items():
            if keyword in nl_query.lower():
                query_parts.append(f"mediatype:{mediatype}")
                break
        
        # Year detection
        year_match = re.search(r'\b(19|20)\d{2}\b', nl_query)
        if year_match:
            query_parts.append(f"year:{year_match.group()}")
        
        # Collection detection
        collections = ['nasa', 'gutenberg', 'prelinger', 'librivox', 'etree']
        for coll in collections:
            if coll in nl_query.lower():
                query_parts.append(f"collection:{coll}")
        
        # Subject extraction (simple keyword approach)
        keywords = re.findall(r'\b[A-Z][a-z]{3,}\b', nl_query)
        if keywords:
            subject = ' '.join(keywords[:3])  # Top 3 keywords
            query_parts.append(f'title:("{subject}" OR {subject.split()[0]})')
        
        return ' AND '.join(query_parts) if query_parts else nl_query
    
    def smart_search(self, query: str, auto_parse: bool = True,
                    max_results: int = 1000) -> List[Dict[str, Any]]:
        """
        Execute intelligent search with automatic query optimization
        
        Args:
            query: Search query (natural language or IA syntax)
            auto_parse: Automatically parse natural language
            max_results: Maximum results to return
        
        Returns:
            List of search results
        """
        if auto_parse and not any(op in query for op in [':', 'AND', 'OR']):
            parsed_query = self.parse_natural_language_query(query)
            print(f"📝 Parsed query: {parsed_query}")
        else:
            parsed_query = query
        
        results = []
        for item in self.client.scrape(parsed_query):
            results.append(item)
            if len(results) >= max_results:
                break
        
        return results
    
    def faceted_search(self, base_query: str, 
                      facets: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
        """
        Execute faceted search across multiple dimensions
        
        Args:
            base_query: Base search query
            facets: Dictionary of facet fields and their values
        
        Returns:
            Dictionary of results grouped by facet
        """
        results = {}
        
        for facet_name, facet_values in facets.items():
            results[facet_name] = {}
            for value in facet_values:
                facet_query = f"{base_query} AND {facet_name}:{value}"
                facet_results = list(self.client.scrape(
                    ScrapeQuery(query=facet_query, count=100)
                ))
                results[facet_name][value] = facet_results
        
        return results


class IACuratorAgent:
    """Collection curation and management agent"""
    
    def __init__(self, client: InternetArchiveClient):
        self.client = client
        self.role = AgentRole.CURATOR
    
    def create_collection(self, spec: CollectionSpec) -> Dict[str, Any]:
        """
        Create and populate a curated collection
        
        Args:
            spec: Collection specification
        
        Returns:
            Collection creation report
        """
        print(f"📚 Creating collection: {spec.name}")
        
        # Search for candidate items
        candidates = list(self.client.scrape(
            ScrapeQuery(query=spec.query, count=1000)
        ))
        
        print(f"Found {len(candidates)} candidate items")
        
        # Apply quality scoring
        scored_items = []
        for item in candidates:
            score = self._calculate_quality_score(item)
            if score >= spec.min_quality_score:
                scored_items.append((score, item))
        
        # Sort by quality and limit
        scored_items.sort(reverse=True, key=lambda x: x[0])
        if spec.max_items:
            scored_items = scored_items[:spec.max_items]
        
        final_items = [item for score, item in scored_items]
        
        print(f"✅ Selected {len(final_items)} high-quality items")
        
        return {
            'name': spec.name,
            'query': spec.query,
            'total_candidates': len(candidates),
            'selected_items': len(final_items),
            'items': final_items,
            'avg_quality_score': sum(s for s, _ in scored_items) / len(scored_items) if scored_items else 0
        }
    
    def _calculate_quality_score(self, item: Dict[str, Any]) -> float:
        """Calculate item quality score based on metadata completeness"""
        score = 0.0
        
        # Has title
        if item.get('title'):
            score += 0.2
        
        # Has description
        if item.get('description'):
            score += 0.2
        
        # Has creator/uploader
        if item.get('creator') or item.get('uploader'):
            score += 0.15
        
        # Has subject tags
        if item.get('subject'):
            score += 0.15
        
        # Has date
        if item.get('date') or item.get('year'):
            score += 0.1
        
        # Has language
        if item.get('language'):
            score += 0.1
        
        # Has collection
        if item.get('collection'):
            score += 0.1
        
        return min(score, 1.0)
    
    def enrich_metadata(self, identifier: str, 
                       auto_enhance: bool = True) -> Dict[str, Any]:
        """
        Enrich item metadata with intelligent suggestions
        
        Args:
            identifier: Item identifier
            auto_enhance: Automatically apply enhancements
        
        Returns:
            Enrichment report
        """
        metadata = self.client.get_metadata(identifier)
        current_meta = metadata.get('metadata', {})
        
        suggestions = {}
        
        # Suggest subjects based on title/description
        if not current_meta.get('subject'):
            title = current_meta.get('title', '')
            desc = current_meta.get('description', '')
            text = f"{title} {desc}".lower()
            
            # Simple keyword extraction
            keywords = self._extract_keywords(text)
            if keywords:
                suggestions['subject'] = keywords
        
        # Suggest language if missing
        if not current_meta.get('language'):
            suggestions['language'] = ['eng']  # Default assumption
        
        # Suggest mediatype if missing
        if not current_meta.get('mediatype'):
            files = metadata.get('files', [])
            if files:
                suggestions['mediatype'] = self._infer_mediatype(files)
        
        if auto_enhance and suggestions and self.client.credentials:
            self.client.update_metadata(identifier, suggestions)
            print(f"✅ Enhanced metadata for {identifier}")
        
        return {
            'identifier': identifier,
            'suggestions': suggestions,
            'applied': auto_enhance
        }
    
    def _extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extract keywords from text"""
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        filtered = [w for w in words if w not in common_words]
        
        # Count frequencies
        freq = {}
        for word in filtered:
            freq[word] = freq.get(word, 0) + 1
        
        # Return top keywords
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:max_keywords]]
    
    def _infer_mediatype(self, files: List[Dict]) -> str:
        """Infer media type from file extensions"""
        extensions = [f.get('name', '').split('.')[-1].lower() for f in files]
        
        if any(ext in extensions for ext in ['mp4', 'avi', 'mov', 'mkv']):
            return 'movies'
        elif any(ext in extensions for ext in ['mp3', 'flac', 'ogg', 'wav']):
            return 'audio'
        elif any(ext in extensions for ext in ['pdf', 'epub', 'txt']):
            return 'texts'
        elif any(ext in extensions for ext in ['jpg', 'png', 'gif', 'tiff']):
            return 'image'
        else:
            return 'data'


class IATimekeeperAgent:
    """Wayback Machine temporal analysis agent"""
    
    def __init__(self, client: InternetArchiveClient):
        self.client = client
        self.role = AgentRole.TIMEKEEPER
    
    def analyze_url_history(self, url: str, 
                           from_year: Optional[int] = None,
                           to_year: Optional[int] = None) -> Dict[str, Any]:
        """
        Analyze complete temporal history of a URL
        
        Args:
            url: URL to analyze
            from_year: Start year (optional)
            to_year: End year (optional)
        
        Returns:
            Temporal analysis report
        """
        print(f"⏰ Analyzing history of {url}")
        
        from_date = f"{from_year}0101" if from_year else None
        to_date = f"{to_year}1231" if to_year else None
        
        # Get all captures
        captures = self.client.query_cdx(
            url=url,
            from_date=from_date,
            to_date=to_date,
            output_format='json'
        )
        
        if not captures or len(captures) < 2:
            return {
                'url': url,
                'total_captures': len(captures) if captures else 0,
                'analysis': 'Insufficient data'
            }
        
        # Parse CDX response (skip header row)
        headers = captures[0]
        data_rows = captures[1:]
        
        # Analyze patterns
        timestamps = [row[1] for row in data_rows]
        status_codes = [row[4] for row in data_rows]
        
        # Extract years
        years = {}
        for ts in timestamps:
            year = ts[:4]
            years[year] = years.get(year, 0) + 1
        
        # Find gaps (years with no captures)
        if from_year and to_year:
            all_years = set(str(y) for y in range(from_year, to_year + 1))
            captured_years = set(years.keys())
            gaps = sorted(all_years - captured_years)
        else:
            gaps = []
        
        # Success rate
        success_count = sum(1 for code in status_codes if code.startswith('2'))
        success_rate = success_count / len(status_codes) if status_codes else 0
        
        return {
            'url': url,
            'total_captures': len(data_rows),
            'date_range': {
                'first': timestamps[0],
                'last': timestamps[-1]
            },
            'yearly_distribution': years,
            'temporal_gaps': gaps,
            'success_rate': success_rate,
            'status_distribution': self._count_distribution(status_codes)
        }
    
    def _count_distribution(self, items: List[str]) -> Dict[str, int]:
        """Count distribution of items"""
        dist = {}
        for item in items:
            dist[item] = dist.get(item, 0) + 1
        return dist
    
    def find_first_capture(self, url: str) -> Optional[Dict[str, Any]]:
        """Find the very first capture of a URL"""
        availability = self.client.check_wayback_availability(url, timestamp="19960101")
        
        if availability.get('archived_snapshots'):
            snapshot = availability['archived_snapshots']['closest']
            return {
                'url': snapshot['url'],
                'timestamp': snapshot['timestamp'],
                'status': snapshot['status']
            }
        return None


class IAOrchestratorAgent:
    """Master orchestrator for multi-agent coordination"""
    
    def __init__(self, client: InternetArchiveClient):
        self.client = client
        self.searcher = IASearchAgent(client)
        self.curator = IACuratorAgent(client)
        self.timekeeper = IATimekeeperAgent(client)
        self.task_queue: List[AgentTask] = []
    
    def execute_workflow(self, workflow: List[AgentTask]) -> Dict[str, Any]:
        """
        Execute multi-step workflow with agent coordination
        
        Args:
            workflow: List of agent tasks
        
        Returns:
            Workflow execution report
        """
        print(f"🚀 Executing workflow with {len(workflow)} tasks")
        
        results = []
        
        for task in sorted(workflow, key=lambda t: t.priority, reverse=True):
            print(f"\n▶️  Task {task.task_id}: {task.operation}")
            
            try:
                if task.role == AgentRole.SEARCHER:
                    result = self._execute_search_task(task)
                elif task.role == AgentRole.CURATOR:
                    result = self._execute_curator_task(task)
                elif task.role == AgentRole.TIMEKEEPER:
                    result = self._execute_timekeeper_task(task)
                else:
                    result = {'error': 'Unknown role'}
                
                task.status = 'completed'
                task.result = result
                task.completed_at = datetime.now()
                
                print(f"✅ Completed in {(task.completed_at - task.created_at).total_seconds():.2f}s")
                
            except Exception as e:
                task.status = 'failed'
                task.error = str(e)
                print(f"❌ Failed: {e}")
            
            results.append(task)
        
        return {
            'total_tasks': len(workflow),
            'completed': sum(1 for t in results if t.status == 'completed'),
            'failed': sum(1 for t in results if t.status == 'failed'),
            'tasks': results
        }
    
    def _execute_search_task(self, task: AgentTask) -> Any:
        """Execute search agent task"""
        op = task.operation
        params = task.parameters
        
        if op == 'smart_search':
            return self.searcher.smart_search(**params)
        elif op == 'faceted_search':
            return self.searcher.faceted_search(**params)
        else:
            raise ValueError(f"Unknown search operation: {op}")
    
    def _execute_curator_task(self, task: AgentTask) -> Any:
        """Execute curator agent task"""
        op = task.operation
        params = task.parameters
        
        if op == 'create_collection':
            spec = CollectionSpec(**params)
            return self.curator.create_collection(spec)
        elif op == 'enrich_metadata':
            return self.curator.enrich_metadata(**params)
        else:
            raise ValueError(f"Unknown curator operation: {op}")
    
    def _execute_timekeeper_task(self, task: AgentTask) -> Any:
        """Execute timekeeper agent task"""
        op = task.operation
        params = task.parameters
        
        if op == 'analyze_history':
            return self.timekeeper.analyze_url_history(**params)
        elif op == 'find_first_capture':
            return self.timekeeper.find_first_capture(**params)
        else:
            raise ValueError(f"Unknown timekeeper operation: {op}")


if __name__ == "__main__":
    # Demo workflow
    print("Internet Archive AI Agent System")
    print("=" * 60)
    
    client = InternetArchiveClient()
    orchestrator = IAOrchestratorAgent(client)
    
    # Create demo workflow
    workflow = [
        AgentTask(
            task_id="search-1",
            role=AgentRole.SEARCHER,
            operation="smart_search",
            parameters={'query': 'videos about space exploration', 'max_results': 10},
            priority=10
        ),
        AgentTask(
            task_id="time-1",
            role=AgentRole.TIMEKEEPER,
            operation="analyze_history",
            parameters={'url': 'nasa.gov', 'from_year': 2020, 'to_year': 2026},
            priority=8
        )
    ]
    
    # Execute
    report = orchestrator.execute_workflow(workflow)
    
    print("\n" + "=" * 60)
    print(f"✅ Workflow completed: {report['completed']}/{report['total_tasks']} tasks")
