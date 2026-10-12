import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.api.app import create_app
from app.core.config import MCPSettings, get_mcp_settings


def test_http_defaults_are_disabled_and_local_only() -> None:
    settings = MCPSettings()
    assert not settings.enabled
    assert settings.bearer_token is None
    assert settings.allowed_origins == ""
    assert set(settings.allowed_hosts.split(",")) == {
        "localhost",
        "localhost:*",
        "127.0.0.1",
        "127.0.0.1:*",
        "[::1]",
        "[::1]:*",
    }


@pytest.mark.parametrize("token", [None, "", "short", " " * 40, "a" * 32 + "\n", "é" * 32])
def test_enabled_http_rejects_missing_or_invalid_token(monkeypatch: pytest.MonkeyPatch, token: str | None) -> None:
    monkeypatch.setenv("MCP_ENABLED", "true")
    if token is not None:
        monkeypatch.setenv("MCP_BEARER_TOKEN", token)
    with pytest.raises(ValidationError, match="MCP_BEARER_TOKEN") as error:
        create_app()
    if token:
        assert token not in str(error.value)


@pytest.mark.parametrize(
    ("variable", "value"),
    [
        ("MCP_ALLOWED_HOSTS", ""),
        ("MCP_ALLOWED_HOSTS", "*"),
        ("MCP_ALLOWED_HOSTS", "*.example.com"),
        ("MCP_ALLOWED_HOSTS", "https://localhost"),
        ("MCP_ALLOWED_HOSTS", "localhost:70000"),
        ("MCP_ALLOWED_HOSTS", "user@localhost"),
        ("MCP_ALLOWED_ORIGINS", "*"),
        ("MCP_ALLOWED_ORIGINS", "https://app.example.com/path"),
        ("MCP_ALLOWED_ORIGINS", "https://app.example.com:*"),
        ("MCP_ALLOWED_ORIGINS", "https://user:pass@app.example.com"),
    ],
)
def test_invalid_allowlists_fail_configuration(monkeypatch: pytest.MonkeyPatch, variable: str, value: str) -> None:
    monkeypatch.setenv(variable, value)
    with pytest.raises(ValidationError, match=variable):
        create_app()


def test_valid_settings_hide_secret_and_cache_environment(monkeypatch: pytest.MonkeyPatch, bearer_token: str) -> None:
    monkeypatch.setenv("MCP_ENABLED", "true")
    monkeypatch.setenv("MCP_BEARER_TOKEN", bearer_token)
    monkeypatch.setenv("MCP_ALLOWED_HOSTS", "api.example.com,api.example.com:443,[::1]:1114")
    monkeypatch.setenv("MCP_ALLOWED_ORIGINS", "https://app.example.com,http://localhost:3000")
    first = get_mcp_settings()
    assert bearer_token not in repr(first)
    monkeypatch.setenv("MCP_ENABLED", "false")
    assert get_mcp_settings() is first
    get_mcp_settings.cache_clear()
    assert not get_mcp_settings().enabled


def test_explicit_env_file_and_environment_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_file = tmp_path / "mcp.env"
    env_file.write_text("MCP_ENABLED=false\nMCP_ALLOWED_HOSTS=api.example.com\n", encoding="utf-8")
    file_config = MCPSettings.model_config.copy()
    file_config["env_file"] = env_file
    monkeypatch.setattr(MCPSettings, "model_config", file_config)
    assert MCPSettings().allowed_hosts == "api.example.com"
    monkeypatch.setenv("MCP_ALLOWED_HOSTS", "localhost")
    assert MCPSettings().allowed_hosts == "localhost"
    monkeypatch.delenv("MCP_ALLOWED_HOSTS")
    empty_config = MCPSettings.model_config.copy()
    empty_config["env_file"] = os.devnull
    monkeypatch.setattr(MCPSettings, "model_config", empty_config)
    assert MCPSettings().allowed_hosts.startswith("localhost,")
