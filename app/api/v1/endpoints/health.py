from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services import get_health_status, get_readiness_status

router = APIRouter()


@router.get("/health")
async def health_check() -> HealthResponse:
    return get_health_status()


@router.get("/health/ready")
async def readiness_check() -> HealthResponse:
    return get_readiness_status()
