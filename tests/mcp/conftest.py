from collections.abc import Iterator

import pytest

from app.core.config import get_logging_settings, get_mcp_settings, get_settings


@pytest.fixture(autouse=True)
def isolated_settings(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("MCP_ENABLED", "false")
    for getter in (get_settings, get_mcp_settings, get_logging_settings):
        getter.cache_clear()
    yield
    for getter in (get_settings, get_mcp_settings, get_logging_settings):
        getter.cache_clear()


@pytest.fixture
def bearer_token() -> str:
    # This is an intentionally public fixture, never a deployment credential.
    return "test-only-mcp-bearer-credential-0001"


@pytest.fixture
def enabled_mcp(monkeypatch: pytest.MonkeyPatch, bearer_token: str) -> None:
    monkeypatch.setenv("MCP_ENABLED", "true")
    monkeypatch.setenv("MCP_BEARER_TOKEN", bearer_token)
