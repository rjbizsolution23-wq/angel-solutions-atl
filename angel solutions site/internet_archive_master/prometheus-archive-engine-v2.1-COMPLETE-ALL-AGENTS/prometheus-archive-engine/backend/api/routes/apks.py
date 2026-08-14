"""
Prometheus Archive Engine - Mobile APKs API Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import internetarchive as ia
from uuid import uuid4

from ...core.db import get_db
from ...core.auth import get_current_user
from ...models.database import User, ArchivedContent, SearchHistory
from ...agents.apk_manager import APKManagerAgent
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

agent = APKManagerAgent(ia_client=ia)

class APKBundleRequest(BaseModel):
    identifiers: List[str]
    bundle_name: str
    category: str
    description: Optional[str] = "Custom APK App Collection"

@router.get("/search")
async def search_apks_endpoint(
    query: str,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Query classic and legacy Android app packages"""
    try:
        results = await agent.search_apks(
            query=query,
            category=category
        )

        # Log query history
        history_id = str(uuid4())
        history = SearchHistory(
            id=history_id,
            query=f"Category: {category or 'all'}, Keyword: {query}",
            search_type="apks",
            results_count=len(results),
            results_summary=f"Found {len(results)} APKs for: {query}",
            created_by_id=current_user.id
        )
        db.add(history)
        await db.commit()

        # Synchronize query to Base44
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("SearchHistory", {
            "id": history_id,
            "query": f"Category: {category or 'all'}, Keyword: {query}",
            "search_type": "ai_research",
            "results_count": len(results),
            "results_summary": f"Found {len(results)} APKs for: {query}",
            "created_by_id": current_user.id
        })

        return {"apks": results}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query mobile APK archives: {str(exc)}"
        ) from exc

@router.post("/bundle")
async def create_apk_bundle_endpoint(
    payload: APKBundleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Bundles multiple APK applications into a single custom app repository"""
    try:
        # Load packages for all identifiers
        packages = []
        for ident in payload.identifiers:
            package = await agent.get_apk_package(ident)
            packages.append(package)

        bundle = await agent.create_bundle(
            name=payload.bundle_name,
            description=payload.description,
            category=payload.category,
            apks=packages
        )

        # Save bundle content log
        content_id = str(uuid4())
        content = ArchivedContent(
            id=content_id,
            url=f"https://archive.org/details/{payload.identifiers[0] if payload.identifiers else 'multi'}",
            title=bundle.name,
            description=bundle.description,
            content_type="apk",
            status="archived",
            file_size=int(bundle.total_size_mb * 1024 * 1024),
            archive_source="ai_agent",
            notes=f"Custom APK Collection containing {len(packages)} applications.",
            created_by_id=current_user.id
        )
        db.add(content)
        await db.commit()

        # Synchronize archived content item to Base44 cloud NoSQL (map 'apk' -> 'api_data')
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("ArchivedContent", {
            "id": content_id,
            "url": f"https://archive.org/details/{payload.identifiers[0] if payload.identifiers else 'multi'}",
            "title": bundle.name,
            "description": bundle.description[:200] if bundle.description else "",
            "content_type": "api_data",
            "status": "archived",
            "archive_source": "ai_agent",
            "notes": f"Custom APK Collection containing {len(packages)} applications.",
            "created_by_id": current_user.id
        })

        return {
            "bundle_name": bundle.name,
            "description": bundle.description,
            "category": bundle.category,
            "total_size_mb": bundle.total_size_mb,
            "apks_included": [
                {
                    "identifier": apk.identifier,
                    "app_name": apk.app_name,
                    "package_name": apk.package_name,
                    "version": apk.version,
                    "min_sdk": apk.min_sdk,
                    "download_url": apk.file_url,
                    "size_bytes": apk.file_size
                }
                for apk in bundle.apks
            ]
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate APK bundle: {str(exc)}"
        ) from exc
