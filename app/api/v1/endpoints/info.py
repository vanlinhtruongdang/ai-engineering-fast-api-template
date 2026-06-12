from fastapi import APIRouter

from app.api.dependencies import get_api_settings

router = APIRouter()


@router.get("/")
async def read_system_info() -> dict[str, str]:
    settings = get_api_settings()
    return {
        "status": "ok",
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
