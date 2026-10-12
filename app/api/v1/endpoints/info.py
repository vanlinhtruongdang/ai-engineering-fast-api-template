from fastapi import APIRouter

from app.api.dependencies import get_api_settings
from app.schemas.info import SystemInfoResponse
from app.services.info_service import get_system_info

router = APIRouter()


@router.get("/")
async def read_system_info() -> SystemInfoResponse:
    return get_system_info(get_api_settings())
