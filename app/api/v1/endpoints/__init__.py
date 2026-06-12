from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.info import router as info_router

__all__ = ["health_router", "info_router"]
