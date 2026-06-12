from fastapi import APIRouter

from app.api.v1.endpoints import health_router, info_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(info_router, tags=["system"])

__all__ = ["api_router"]
