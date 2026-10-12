import os
import re
from functools import lru_cache
from ipaddress import IPv6Address
from typing import Self
from urllib.parse import urlsplit

from pydantic import Field, SecretStr, model_validator
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


class MCPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    enabled: bool = Field(default=False, validation_alias="MCP_ENABLED")
    bearer_token: SecretStr | None = Field(default=None, validation_alias="MCP_BEARER_TOKEN")
    allowed_hosts: str = Field(
        default="localhost,localhost:*,127.0.0.1,127.0.0.1:*,[::1],[::1]:*",
        validation_alias="MCP_ALLOWED_HOSTS",
    )
    allowed_origins: str = Field(default="", validation_alias="MCP_ALLOWED_ORIGINS")

    @model_validator(mode="after")
    def validate_http_configuration(self) -> Self:
        if self.enabled:
            token = self.bearer_token.get_secret_value() if self.bearer_token is not None else ""
            if len(token) < 32 or re.fullmatch(r"[A-Za-z0-9._~+/-]+=*", token) is None:
                raise ValueError("MCP_BEARER_TOKEN must be at least 32 characters and use bearer-token characters")

        hosts = [value.strip() for value in self.allowed_hosts.split(",") if value.strip()]
        if not hosts:
            raise ValueError("MCP_ALLOWED_HOSTS must contain at least one hostname")
        for host in hosts:
            candidate = host[:-1] + "1" if host.endswith(":*") else host
            try:
                parsed = urlsplit("//" + candidate)
                hostname = parsed.hostname or ""
                port = parsed.port
                valid_name = re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?", hostname) is not None
                if ":" in hostname:
                    IPv6Address(hostname)
                    valid_name = True
                if (
                    not valid_name
                    or parsed.username is not None
                    or parsed.password is not None
                    or parsed.path
                    or parsed.query
                    or parsed.fragment
                    or any(character in candidate for character in "*\\?#@ \t\r\n")
                    or candidate.endswith(":")
                    or port == 0
                ):
                    raise ValueError
            except ValueError:
                raise ValueError("MCP_ALLOWED_HOSTS must use hostnames with an optional port or :*") from None

        for origin in (value.strip() for value in self.allowed_origins.split(",") if value.strip()):
            try:
                parsed = urlsplit(origin)
                port = parsed.port
                if (
                    parsed.scheme not in {"http", "https"}
                    or not parsed.hostname
                    or parsed.username is not None
                    or parsed.password is not None
                    or parsed.path
                    or parsed.query
                    or parsed.fragment
                    or any(character in origin for character in "*\\?#@ \t\r\n")
                    or origin.endswith(":")
                    or port == 0
                ):
                    raise ValueError
            except ValueError:
                raise ValueError(
                    "MCP_ALLOWED_ORIGINS must use exact http(s) origins without paths or wildcards"
                ) from None
        return self


@lru_cache
def get_settings() -> APISettings:
    return APISettings()


@lru_cache
def get_logging_settings() -> LoggingSettings:
    return LoggingSettings()


@lru_cache
def get_mcp_settings() -> MCPSettings:
    return MCPSettings()


__all__ = [
    "APISettings",
    "LoggingSettings",
    "MCPSettings",
    "get_logging_settings",
    "get_mcp_settings",
    "get_settings",
]
