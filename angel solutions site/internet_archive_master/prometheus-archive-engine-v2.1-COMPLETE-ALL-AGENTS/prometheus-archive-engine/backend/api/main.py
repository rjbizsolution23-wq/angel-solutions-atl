"""
Prometheus Archive Engine - FastAPI Application
Main API entry point
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

# Import routers
from .routes import auth, books, games, software, apks, orchestrate, checkout, webhooks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Prometheus Archive Engine starting up...")
    yield
    logger.info("👋 Shutting down gracefully...")


# Create FastAPI application
app = FastAPI(
    title="Prometheus Archive Engine API",
    description="AI-Powered Internet Archive Monetization Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "prometheus-archive-engine"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Prometheus Archive Engine",
        "version": "2.0.0",
        "description": "AI-Powered Internet Archive Monetization Platform",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "books": "/api/books",
            "games": "/api/games",
            "orchestrate": "/api/orchestrate",
            "checkout": "/api/checkout"
        }
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(games.router, prefix="/api/games", tags=["Games"])
app.include_router(software.router, prefix="/api/software", tags=["Software"])
app.include_router(apks.router, prefix="/api/apks", tags=["APKs"])
app.include_router(orchestrate.router, prefix="/api/orchestrate", tags=["Orchestration"])
app.include_router(checkout.router, prefix="/api/checkout", tags=["Checkout"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
