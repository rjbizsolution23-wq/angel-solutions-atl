"""
Prometheus Archive Engine - Desktop Software API Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import internetarchive as ia
from uuid import uuid4

from ...core.db import get_db
from ...core.auth import get_current_user
from ...models.database import User, ArchivedContent, SearchHistory
from ...agents.software_manager import SoftwareManagerAgent
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

agent = SoftwareManagerAgent(ia_client=ia)

class BundleRequest(BaseModel):
    identifiers: List[str]
    bundle_name: str
    description: Optional[str] = "Custom Software Bundle"

@router.get("/search")
async def search_software_endpoint(
    query: str,
    platform: str = "windows",
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Query classic and legacy desktop software installers"""
    year_range = (min_year, max_year) if min_year and max_year else None
    try:
        results = await agent.search_software(
            query=query,
            platform=platform,
            year_range=year_range
        )

        # Log query history
        history_id = str(uuid4())
        history = SearchHistory(
            id=history_id,
            query=f"Platform: {platform}, Keyword: {query}",
            search_type="software",
            results_count=len(results),
            results_summary=f"Found {len(results)} software for: {query}",
            created_by_id=current_user.id
        )
        db.add(history)
        await db.commit()

        # Synchronize query to Base44
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("SearchHistory", {
            "id": history_id,
            "query": f"Platform: {platform}, Keyword: {query}",
            "search_type": "ai_research",
            "results_count": len(results),
            "results_summary": f"Found {len(results)} software for: {query}",
            "created_by_id": current_user.id
        })

        return {"software": results}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query desktop software archives: {str(exc)}"
        ) from exc

@router.post("/bundle")
async def create_bundle_endpoint(
    payload: BundleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Bundles multiple desktop software applications into a single installer suite"""
    try:
        # Load packages for all identifiers
        packages = []
        for ident in payload.identifiers:
            package = await agent.get_software_package(ident)
            packages.append(package)

        bundle = await agent.create_bundle(
            name=payload.bundle_name,
            description=payload.description,
            packages=packages
        )

        # Save bundle content log
        content_id = str(uuid4())
        content = ArchivedContent(
            id=content_id,
            url=f"https://archive.org/details/{payload.identifiers[0] if payload.identifiers else 'multi'}",
            title=bundle.name,
            description=bundle.description,
            content_type="software",
            status="archived",
            file_size=int(bundle.total_size_mb * 1024 * 1024),
            archive_source="ai_agent",
            notes=f"Bundle containing {len(packages)} applications.",
            created_by_id=current_user.id
        )
        db.add(content)
        await db.commit()

        # Synchronize archived content item to Base44 cloud NoSQL (map 'software' -> 'api_data')
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("ArchivedContent", {
            "id": content_id,
            "url": f"https://archive.org/details/{payload.identifiers[0] if payload.identifiers else 'multi'}",
            "title": bundle.name,
            "description": bundle.description[:200] if bundle.description else "",
            "content_type": "api_data",
            "status": "archived",
            "archive_source": "ai_agent",
            "notes": f"Bundle containing {len(packages)} applications.",
            "created_by_id": current_user.id
        })

        return {
            "bundle_name": bundle.name,
            "description": bundle.description,
            "platform": bundle.platform,
            "total_size_mb": bundle.total_size_mb,
            "apps_included": [
                {
                    "identifier": app.identifier,
                    "title": app.title,
                    "publisher": app.publisher,
                    "version": app.version,
                    "license": app.license,
                    "download_urls": app.file_urls
                }
                for app in bundle.software
            ],
            "installation_guide": bundle.installation_guide
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate installer bundle: {str(exc)}"
        ) from exc
