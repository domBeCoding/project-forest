"""
Health check endpoints for Project Forest.

- /private/status: Liveness probe (is the app running?)
- /private/healthcheck: Readiness probe (are all dependencies healthy?)
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Literal, Optional
from datetime import datetime

from app.config import Settings, get_settings

router = APIRouter(prefix="/private", tags=["health"])


class StatusResponse(BaseModel):
    """Simple status response for liveness checks."""
    status: Literal["up"]
    service: str
    version: str
    timestamp: str


class HealthComponent(BaseModel):
    """Individual component health status."""
    status: Literal["up", "down", "unknown"]
    details: Optional[str] = None


class HealthcheckResponse(BaseModel):
    """Detailed health check including all dependencies."""
    overall: Literal["up", "down", "degraded"]
    service: str
    version: str
    timestamp: str
    components: Dict[str, HealthComponent]


@router.get("/status", response_model=StatusResponse)
async def status(settings: Settings = Depends(get_settings)) -> StatusResponse:
    """
    Liveness probe - returns basic app status.
    
    Use this to check if the application process is running.
    This endpoint should be lightweight and always return 200 if the app is alive.
    """
    return StatusResponse(
        status="up",
        service=settings.app_name,
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@router.get("/healthcheck", response_model=HealthcheckResponse)
async def healthcheck(settings: Settings = Depends(get_settings)) -> HealthcheckResponse:
    """
    Readiness probe - returns overall health including dependencies.
    
    Use this to check if the app AND all its dependencies are healthy.
    Returns 200 only if everything is operational.
    """
    components: Dict[str, HealthComponent] = {}
    
    # Check application itself
    components["app"] = HealthComponent(
        status="up",
        details="Application is running"
    )
    
    # Placeholder: Check exchange API connectivity (to be implemented)
    # For now, we mark it as "unknown" since we're just building the skeleton
    components["exchange_api"] = HealthComponent(
        status="unknown",
        details="Exchange client not yet initialized"
    )
    
    # Placeholder: Check database/cache if added later
    components["database"] = HealthComponent(
        status="unknown",
        details="No database configured"
    )
    
    # Determine overall status
    statuses = [c.status for c in components.values()]
    if all(s == "up" for s in statuses):
        overall = "up"
    elif any(s == "down" for s in statuses):
        overall = "down"
    else:
        overall = "degraded"
    
    return HealthcheckResponse(
        overall=overall,
        service=settings.app_name,
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat() + "Z",
        components=components
    )
