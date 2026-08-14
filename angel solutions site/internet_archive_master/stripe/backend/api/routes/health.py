"""
Health check endpoints.
"""
from fastapi import APIRouter
from core.config import get_settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "environment": settings.environment,
        "stripe_mode": settings.stripe_mode
    }
