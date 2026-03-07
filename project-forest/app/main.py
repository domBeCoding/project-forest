"""
Project Forest - Main FastAPI Application

Entry point for the automated trading bot.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown."""
    # Startup
    settings = get_settings()
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    
    # TODO: Initialize exchange client, database connections, etc.
    
    yield
    
    # Shutdown
    print(f"👋 Shutting down {settings.app_name}")
    
    # TODO: Clean up resources


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Automated cryptocurrency trading bot",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Include routers
    app.include_router(health.router)
    
    @app.get("/", response_class=JSONResponse)
    async def root():
        """Root endpoint with basic info."""
        return {
            "service": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/private/status"
        }
    
    return app


# Create the app instance for uvicorn
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
