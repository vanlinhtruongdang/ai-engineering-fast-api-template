from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.api.dependencies import get_api_settings
from app.api.v1 import api_router
from app.core.logging import configure_logging
from app.core.request_context import attach_request_id
from app.services import get_health_status, get_readiness_status


def _parse_cors_values(raw_value: str, *, default_wildcard: bool = False) -> list[str]:
    if raw_value == "*":
        return ["*"]

    values = [value.strip() for value in raw_value.split(",") if value.strip()]
    if values:
        return values

    return ["*"] if default_wildcard else []


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    yield


def create_app() -> FastAPI:
    settings = get_api_settings()
    if settings.environment == "production" and settings.cors_allow_origins == "*":
        raise ValueError("CORS_ALLOW_ORIGINS must be explicit in production")

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="FastAPI template scaffold for backend APIs.",
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url=None,
        openapi_url=settings.openapi_url if settings.docs_enabled else None,
        lifespan=lifespan,
        openapi_tags=[
            {"name": "health", "description": "Public health-check endpoints."},
            {"name": "system", "description": "Application metadata and system endpoints."},
        ],
    )
    app.state.request_id_header = settings.request_id_header
    app.middleware("http")(attach_request_id)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_parse_cors_values(settings.cors_allow_origins, default_wildcard=True),
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=_parse_cors_values(settings.cors_allow_methods, default_wildcard=True),
        allow_headers=_parse_cors_values(settings.cors_allow_headers, default_wildcard=True),
        expose_headers=_parse_cors_values(settings.cors_expose_headers),
        max_age=settings.cors_max_age,
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/health", include_in_schema=False)
    async def health_check() -> object:
        return get_health_status()

    @app.get("/ready", include_in_schema=False)
    async def readiness_check() -> object:
        return get_readiness_status()

    if settings.docs_enabled:

        @app.get(settings.scalar_path, include_in_schema=False)
        async def scalar_html() -> object:
            return get_scalar_api_reference(
                openapi_url=settings.openapi_url,
                title=f"{app.title} - Scalar",
            )

    return app


__all__ = ["create_app"]
