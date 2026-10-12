from app.core.config import APISettings
from app.schemas.info import SystemInfoResponse


def get_system_info(settings: APISettings) -> SystemInfoResponse:
    return SystemInfoResponse(
        status="ok",
        name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
