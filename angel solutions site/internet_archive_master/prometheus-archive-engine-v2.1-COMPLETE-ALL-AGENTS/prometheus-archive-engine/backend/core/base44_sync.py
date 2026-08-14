"""
Prometheus Archive Engine - Base44 BaaS Synchronizer
Provides real-time synchronization between local PostgreSQL/SQLite database models
and Base44 Cloud Entity collections.
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import httpx

logger = logging.getLogger(__name__)

# Retrieve Base44 credentials from Environment variables, with provided defaults
BASE44_API_KEY = os.getenv("BASE44_API_KEY", "e3bf3c7cc79044f58d69edfa2a2a7e63")
BASE44_APP_ID = os.getenv("BASE44_APP_ID", "6a51e1fe45074c4d50be5dea")

# Intelligently construct default API URL targeting the active AppBuilder domain and App ID
DEFAULT_API_URL = f"https://app.base44.com/api/apps/{BASE44_APP_ID}"
BASE44_API_URL = os.getenv("BASE44_API_URL", DEFAULT_API_URL)

# If the env variable was explicitly set to the legacy host, correct it to the resolved AppBuilder host
if "api.base44.com" in BASE44_API_URL:
    BASE44_API_URL = DEFAULT_API_URL

def format_record_for_base44(entity_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats and cleans record schemas to strictly align with Base44's entity field requirements.
    """
    payload = {**record}

    # Standardize datetime objects to ISO format strings
    for key, value in list(payload.items()):
        if isinstance(value, datetime):
            payload[key] = value.isoformat()

    # Model-specific cleanups
    if entity_name == "ArchivedContent":
        # Map metadata_json (dict) to string metadata
        if "metadata_json" in payload:
            m_json = payload.pop("metadata_json")
            if m_json and not payload.get("metadata"):
                payload["metadata"] = json.dumps(m_json)
        
        # Ensure all types match
        if "file_size" in payload and payload["file_size"] is not None:
            payload["file_size"] = int(payload["file_size"])
        if "is_favorite" in payload:
            payload["is_favorite"] = bool(payload["is_favorite"])
        if "created_by_id" in payload:
            payload["created_by_id"] = str(payload["created_by_id"])

    elif entity_name == "SearchHistory":
        if "created_by_id" in payload:
            payload["created_by_id"] = str(payload["created_by_id"])
        if "results_count" in payload:
            payload["results_count"] = int(payload["results_count"])

    elif entity_name == "AIAgent":
        if "temperature" in payload and payload["temperature"] is not None:
            payload["temperature"] = float(payload["temperature"])

    return payload

async def sync_to_base44(entity_name: str, record: Dict[str, Any]) -> bool:
    """
    Performs real-time synchronization of a single record into a Base44 Cloud Entity collection.
    
    Args:
        entity_name: Target collection name on Base44 (e.g. 'SearchHistory', 'ArchivedContent')
        record: Data dictionary mapping schema properties
        
    Returns:
        bool: True if sync succeeded, False otherwise
    """
    if not BASE44_API_KEY or not BASE44_APP_ID:
        logger.info(f"Base44 credentials not configured. Simulating sync for entity '{entity_name}': {record}")
        return True

    url = f"{BASE44_API_URL}/entities/{entity_name}"
    headers = {
        "api_key": BASE44_API_KEY,
        "appId": BASE44_APP_ID,
        "app_id": BASE44_APP_ID,
        "X-App-Id": BASE44_APP_ID,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            payload = format_record_for_base44(entity_name, record)
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code in [200, 201]:
                logger.info(f"✅ Successfully synchronized record to Base44 {entity_name}: {payload.get('id') or payload.get('query')}")
                return True
            else:
                logger.error(f"❌ Base44 Sync error for {entity_name} ({response.status_code}): {response.text}")
                return False
    except Exception as exc:
        logger.error(f"❌ Failed to communicate with Base44 API during sync: {str(exc)}")
        return False

async def bulk_sync_to_base44(entity_name: str, records: List[Dict[str, Any]]) -> bool:
    """
    Performs bulk-creation synchronization of multiple records into a Base44 collection.
    """
    if not BASE44_API_KEY or not BASE44_APP_ID:
        logger.info(f"Base44 credentials not configured. Simulating bulk sync for {len(records)} '{entity_name}' records.")
        return True

    url = f"{BASE44_API_URL}/entities/{entity_name}/bulk"
    headers = {
        "api_key": BASE44_API_KEY,
        "appId": BASE44_APP_ID,
        "app_id": BASE44_APP_ID,
        "X-App-Id": BASE44_APP_ID,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            formatted_records = [format_record_for_base44(entity_name, r) for r in records]
            response = await client.post(url, json=formatted_records, headers=headers)
            if response.status_code in [200, 201]:
                logger.info(f"✅ Successfully bulk-synchronized {len(records)} records to Base44 {entity_name}")
                return True
            else:
                logger.error(f"❌ Base44 Bulk Sync error for {entity_name} ({response.status_code}): {response.text}")
                return False
    except Exception as exc:
        logger.error(f"❌ Failed to execute bulk sync with Base44 API: {str(exc)}")
        return False
