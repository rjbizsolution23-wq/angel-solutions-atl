"""
Prometheus Archive Engine - Retro Games API Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import internetarchive as ia
from uuid import uuid4

from ...core.db import get_db
from ...core.auth import get_current_user
from ...models.database import User, ArchivedContent, SearchHistory
from ...agents.game_emulator import GameEmulatorAgent
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

agent = GameEmulatorAgent(ia_client=ia)

class PackageRequest(BaseModel):
    identifier: str
    platform: str # nes, snes, genesis, arcade, dos

@router.get("/search")
async def search_games_endpoint(
    platform: str,
    genre: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search classic ROM assets inside Internet Archive console room collection"""
    year_range = (min_year, max_year) if min_year and max_year else None
    try:
        results = await agent.search_games(
            platform=platform,
            genre=genre,
            year_range=year_range
        )

        # Log query history
        history_id = str(uuid4())
        history = SearchHistory(
            id=history_id,
            query=f"Platform: {platform}, Genre: {genre or 'all'}",
            search_type="games",
            results_count=len(results),
            results_summary=f"Found {len(results)} games for: {platform}",
            created_by_id=current_user.id
        )
        db.add(history)
        await db.commit()

        # Synchronize query to Base44
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("SearchHistory", {
            "id": history_id,
            "query": f"Platform: {platform}, Genre: {genre or 'all'}",
            "search_type": "ai_research",
            "results_count": len(results),
            "results_summary": f"Found {len(results)} games for: {platform}",
            "created_by_id": current_user.id
        })

        return {"games": results}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search console room archives: {str(exc)}"
        ) from exc

@router.post("/package")
async def package_game_endpoint(
    payload: PackageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Builds ready-to-play ROM package coupled with a matching WASM web emulator core"""
    try:
        package = await agent.get_game_package(payload.identifier, payload.platform)
        
        # Build local content asset log
        content_id = payload.identifier
        content = ArchivedContent(
            id=content_id,
            url=f"https://archive.org/details/{payload.identifier}",
            title=package.title,
            description=package.description,
            content_type="game",
            status="archived",
            archive_source="ai_agent",
            notes=f"Platform: {payload.platform}. Core Emulator: {package.rom_files[0] if package.rom_files else 'none'}",
            created_by_id=current_user.id
        )
        db.add(content)
        await db.commit()

        # Synchronize archived content item to Base44 cloud NoSQL (map 'game' -> 'api_data')
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("ArchivedContent", {
            "id": content_id,
            "url": f"https://archive.org/details/{payload.identifier}",
            "title": package.title,
            "description": package.description[:200] if package.description else "",
            "content_type": "api_data",
            "status": "archived",
            "archive_source": "ai_agent",
            "notes": f"Platform: {payload.platform}. Core Emulator: {package.rom_files[0] if package.rom_files else 'none'}",
            "created_by_id": current_user.id
        })

        # Map to browser RetroArch core identifiers
        from ...agents.game_emulator import EMULATOR_MAP
        em_info = EMULATOR_MAP.get(payload.platform.lower(), {"name": "RetroArch", "core": "fceumm"})

        return {
            "identifier": payload.identifier,
            "title": package.title,
            "platform": payload.platform,
            "publisher": package.publisher,
            "genre": package.genre,
            "description": package.description,
            "emulator": em_info,
            "rom_links": [
                f"https://archive.org/download/{payload.identifier}/{rom}"
                for rom in package.rom_files
            ],
            "screenshots": package.screenshot_urls
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate emulator pack: {str(exc)}"
        ) from exc
