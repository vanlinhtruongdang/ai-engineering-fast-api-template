import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_ENV_FILE = os.getenv("ENV_FILE", ".env.dev")


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(
        default="development",
        description="Runtime environment name such as development, staging, or production.",
        validation_alias="ENVIRONMENT",
    )
    api_prefix: str = Field(
        default="/api/v1",
        description="Versioned API prefix mounted by FastAPI.",
        validation_alias="API_PREFIX",
    )

    app_name: str = Field(
        default="FastAPI Template",
        description="Application display name used in OpenAPI metadata.",
        validation_alias="APP_NAME",
    )
    app_version: str = Field(
        default="0.1.0",
        description="Semantic version string of the API application.",
        validation_alias="APP_VERSION",
    )
    openapi_url: str = Field(
        default="/openapi.json",
        description="Endpoint where OpenAPI schema is exposed.",
        validation_alias="OPENAPI_URL",
    )
    cors_allow_origins: str = Field(
        default="*",
        description="Comma-separated list of allowed CORS origins, or * for all origins.",
        validation_alias="CORS_ALLOW_ORIGINS",
    )
    cors_allow_credentials: bool = Field(
        default=False,
        description="Whether cross-origin requests may include credentials.",
        validation_alias="CORS_ALLOW_CREDENTIALS",
    )
    cors_allow_methods: str = Field(
        default="*",
        description="Comma-separated list of allowed CORS methods, or * for all methods.",
        validation_alias="CORS_ALLOW_METHODS",
    )
    cors_allow_headers: str = Field(
        default="*",
        description="Comma-separated list of allowed CORS headers, or * for all headers.",
        validation_alias="CORS_ALLOW_HEADERS",
    )
    cors_expose_headers: str = Field(
        default="",
        description="Comma-separated list of CORS response headers exposed to the browser.",
        validation_alias="CORS_EXPOSE_HEADERS",
    )
    cors_max_age: int = Field(
        default=600,
        description="Number of seconds browsers may cache CORS preflight results.",
        ge=0,
        validation_alias="CORS_MAX_AGE",
    )
    scalar_path: str = Field(
        default="/scalar",
        description="Endpoint that serves Scalar API reference UI.",
        validation_alias="SCALAR_PATH",
    )
    docs_enabled: bool = Field(
        default=True,
        description="Whether OpenAPI and interactive documentation endpoints are exposed.",
        validation_alias="DOCS_ENABLED",
    )
    request_id_header: str = Field(
        default="X-Request-ID",
        description="Response header carrying the request correlation identifier.",
        validation_alias="REQUEST_ID_HEADER",
    )

    server_host: str = Field(
        default="0.0.0.0",
        description="Host interface used by Uvicorn server.",
        validation_alias="SERVER_HOST",
    )
    server_port: int = Field(
        default=1114,
        description="TCP port used by Uvicorn server.",
        ge=1,
        le=65535,
        validation_alias="SERVER_PORT",
    )
    server_reload: bool = Field(
        default=True,
        description="Enable auto-reload mode during local development.",
        validation_alias="SERVER_RELOAD",
    )


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    level: str = Field(
        default="INFO",
        description="Logging verbosity level.",
        validation_alias="LOG_LEVEL",
    )
    dir: str = Field(
        default="logs",
        description="Directory path storing log files.",
        validation_alias="LOG_DIR",
    )
    file: str = Field(
        default="app.log",
        description="Primary rotating log filename.",
        validation_alias="LOG_FILE",
    )
    max_bytes: int = Field(
        default=5 * 1024 * 1024,
        description="Maximum size in bytes before rotating log file.",
        gt=0,
        validation_alias="LOG_MAX_BYTES",
    )
    backup_count: int = Field(
        default=5,
        description="Number of rotated backup files to retain.",
        ge=1,
        validation_alias="LOG_BACKUP_COUNT",
    )
    json_logs: bool = Field(
        default=False,
        description="Emit JSON log lines for machine-readable production logs.",
        validation_alias="LOG_JSON",
    )


@lru_cache
def get_settings() -> APISettings:
    return APISettings()


@lru_cache
def get_logging_settings() -> LoggingSettings:
    return LoggingSettings()


__all__ = [
    "APISettings",
    "LoggingSettings",
    "get_logging_settings",
    "get_settings",
]
