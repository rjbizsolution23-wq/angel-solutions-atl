"""
Internet Archive Ultimate Master System
========================================

Complete Python SDK and AI agent system for Internet Archive.

Author: RJ PROMETHEUS APEX
Company: RJ Business Solutions
Version: 1.0.0
Date: 2026-07-11

Quick Start:
    >>> from core.ia_client import InternetArchiveClient
    >>> client = InternetArchiveClient()
    >>> results = client.search("collection:nasa")
"""

__version__ = "1.0.0"
__author__ = "RJ PROMETHEUS APEX"
__email__ = "support@rickjeffersonsolutions.com"
__license__ = "MIT"

from core.ia_client import (
    InternetArchiveClient,
    IACredentials,
    SearchQuery,
    ScrapeQuery,
    TaskCommand,
    TaskCategory,
    OutputFormat,
)

from agents.ia_agent import (
    IAOrchestratorAgent,
    IASearchAgent,
    IACuratorAgent,
    IATimekeeperAgent,
    CollectionSpec,
    AgentTask,
    AgentRole,
)

__all__ = [
    # Client
    "InternetArchiveClient",
    "IACredentials",
    "SearchQuery",
    "ScrapeQuery",
    "TaskCommand",
    "TaskCategory",
    "OutputFormat",
    # Agents
    "IAOrchestratorAgent",
    "IASearchAgent",
    "IACuratorAgent",
    "IATimekeeperAgent",
    "CollectionSpec",
    "AgentTask",
    "AgentRole",
]
