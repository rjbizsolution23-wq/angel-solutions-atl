"""
Prometheus Archive Engine - Book Rebrander API Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import internetarchive as ia

from ...core.db import get_db
from ...core.auth import get_current_user
from ...models.database import User, ArchivedContent, SearchHistory
from ...agents.book_rebrander import BookRebranderAgent
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

router = APIRouter()

# Instantiate single static agent wrapper
agent = BookRebranderAgent(ia_client=ia)

class RebrandRequest(BaseModel):
    identifier: str
    new_title: Optional[str] = None
    new_author: Optional[str] = None
    brand_name: Optional[str] = "RJ Business Solutions"

@router.get("/search")
async def search_books_endpoint(
    query: str,
    subject: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Query Internet Archive books library"""
    year_range = (min_year, max_year) if min_year and max_year else None
    try:
        results = await agent.search_books(
            query=query,
            subject=subject,
            year_range=year_range
        )

        # Log query history
        history_id = str(uuid4())
        history = SearchHistory(
            id=history_id,
            query=query,
            search_type="books",
            results_count=len(results),
            results_summary=f"Found {len(results)} books for: {query}",
            created_by_id=current_user.id
        )
        db.add(history)
        await db.commit()

        # Synchronize query to Base44
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("SearchHistory", {
            "id": history_id,
            "query": query,
            "search_type": "ai_research",
            "results_count": len(results),
            "results_summary": f"Found {len(results)} books for: {query}",
            "created_by_id": current_user.id
        })

        return {"books": results}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query internet archive books: {str(exc)}"
        ) from exc

@router.post("/rebrand")
async def rebrand_book_endpoint(
    payload: RebrandRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Executes AI modernization and corporate rebranding workflow"""
    try:
        # Download core content
        book = await agent.download_book(payload.identifier)
        
        # Modernize and rebrand book
        # Note: If no API keys are loaded, agent falls back to simulation mock
        enhanced = await agent.enhance_book(book)
        branded = await agent.rebrand_book(
            enhanced=enhanced,
            new_title=payload.new_title or f"Enhanced {book.title}",
            new_author=payload.new_author or "AI Publisher Engine",
            brand_name=payload.brand_name
        )

        # Build local content asset log
        content_id = payload.identifier
        content = ArchivedContent(
            id=content_id,
            url=f"https://archive.org/details/{payload.identifier}",
            title=branded.new_title,
            description=branded.enhanced.enhancement_summary,
            content_type="book",
            status="archived",
            file_size=len(branded.styled_content),
            archive_source="ai_agent",
            notes=f"Rebranded under {payload.brand_name}",
            created_by_id=current_user.id
        )
        db.add(content)
        await db.commit()

        # Synchronize archived content item to Base44 cloud NoSQL (map 'book' -> 'document')
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("ArchivedContent", {
            "id": content_id,
            "url": f"https://archive.org/details/{payload.identifier}",
            "title": branded.new_title,
            "description": branded.enhanced.enhancement_summary[:200],
            "content_type": "document",
            "status": "archived",
            "file_size": len(branded.styled_content),
            "archive_source": "ai_agent",
            "notes": f"Rebranded under {payload.brand_name}",
            "created_by_id": current_user.id
        })

        return {
            "identifier": payload.identifier,
            "title": branded.new_title,
            "author": branded.new_author,
            "brand": branded.brand_name,
            "summary": branded.enhanced.enhancement_summary,
            "word_count": branded.enhanced.word_count,
            "chapters": branded.enhanced.chapters,
            "preview_content": branded.styled_content[:1500] # Yield truncated content preview
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute book rebranding: {str(exc)}"
        ) from exc

class NarrateRequest(BaseModel):
    identifier: str
    voice_id: Optional[str] = None
    text_preview: Optional[str] = None

@router.post("/narrate")
async def narrate_book_endpoint(
    payload: NarrateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generates premium voice narration audiobooks using ElevenLabs AI Speech Scribe"""
    try:
        from ...core.elevenlabs import ElevenLabsClient
        client = ElevenLabsClient()
        
        text_to_read = payload.text_preview
        if not text_to_read:
            book = await agent.download_book(payload.identifier)
            text_to_read = book.content[:5000] # Synthesize introduction block
            
        audio_content = await client.generate_speech(
            text=text_to_read,
            voice_id=payload.voice_id
        )
        
        if not audio_content:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to synthesize audiobook from ElevenLabs"
            )

        # Log content generation to Base44
        from ...core.base44_sync import sync_to_base44
        audio_id = f"{payload.identifier}-narrated"
        await sync_to_base44("ArchivedContent", {
            "id": audio_id,
            "url": f"https://archive.org/details/{payload.identifier}/narrated",
            "title": f"Narrated Audiobook: {payload.identifier}",
            "description": f"ElevenLabs Audiobook generation of {payload.identifier}",
            "content_type": "other",
            "status": "archived",
            "file_size": len(audio_content),
            "archive_source": "ai_agent",
            "notes": "Narrated using ElevenLabs Audio Engine",
            "created_by_id": current_user.id
        })

        return {
            "identifier": payload.identifier,
            "voice_id": payload.voice_id or "default",
            "audio_size_bytes": len(audio_content),
            "status": "success",
            "message": "Audiobook narration successfully rendered."
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate audiobook: {str(exc)}"
        ) from exc
