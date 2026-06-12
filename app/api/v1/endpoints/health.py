from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services import get_health_status

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return get_health_status()
