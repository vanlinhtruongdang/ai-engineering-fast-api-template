import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx2
import pytest
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp_types import TextContent, TextResourceContents

from app.api.app import create_app


@pytest.mark.parametrize(("mode", "version"), [("auto", "2026-07-28"), ("legacy", "2025-11-25")])
@pytest.mark.usefixtures("enabled_mcp")
async def test_http_discovery_tool_and_resource(mode: str, version: str, bearer_token: str) -> None:
    app = create_app()
    async with (
        app.router.lifespan_context(app),
        httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app),
            base_url="http://localhost",
            headers={"Authorization": f"Bearer {bearer_token}", "X-Request-ID": "mcp-test"},
        ) as http,
        Client(streamable_http_client("http://localhost/mcp/", http_client=http), mode=mode) as client,
    ):
        assert client.protocol_version == version
        assert client.server_info is not None
        assert client.server_info.name == "FastAPI Template"
        tools = await client.list_tools()
        assert [tool.name for tool in tools.tools] == ["get_health_status"]
        tool = tools.tools[0]
        assert tool.input_schema["properties"] == {}
        assert tool.output_schema is not None
        assert tool.output_schema["properties"]["status"]["type"] == "string"
        assert tool.annotations is not None
        assert tool.annotations.read_only_hint
        assert tool.annotations.idempotent_hint
        result = await client.call_tool("get_health_status")
        assert not result.is_error
        assert result.structured_content == {"status": "ok"}

        resources = await client.list_resources()
        assert [str(resource.uri) for resource in resources.resources] == ["app://info"]
        assert resources.resources[0].mime_type == "application/json"
        resource = await client.read_resource("app://info")
        content = resource.contents[0]
        assert isinstance(content, TextResourceContents)
        assert content.mime_type == "application/json"
        metadata = (await http.get("/api/v1/")).json()
        assert json.loads(content.text) == metadata
        assert (await client.list_prompts()).prompts == []

        unknown = await client.call_tool("unknown_tool")
        assert unknown.is_error
        assert isinstance(unknown.content[0], TextContent)
        assert "Unknown tool" in unknown.content[0].text


async def test_disabled_mcp_returns_404_and_preserves_rest() -> None:
    app = create_app()
    async with httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://localhost") as http:
        for path in ("/mcp", "/mcp/"):
            assert (await http.post(path, json={})).status_code == 404
        assert (await http.get("/health")).json() == {"status": "ok"}
        assert (await http.get("/ready")).json() == {"status": "ok"}


@pytest.mark.parametrize("method", ["POST", "GET", "DELETE", "OPTIONS"])
@pytest.mark.parametrize("authorization", [None, "Basic invalid", "Bearer", "Bearer wrong", "Bearer bad token"])
@pytest.mark.usefixtures("enabled_mcp")
async def test_bearer_rejection_covers_all_methods(
    method: str, authorization: str | None, bearer_token: str, caplog: pytest.LogCaptureFixture
) -> None:
    headers = {"X-Request-ID": "auth-test"}
    if authorization is not None:
        headers["Authorization"] = authorization
    app = create_app()
    async with httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://localhost") as http:
        with caplog.at_level(logging.WARNING, logger="app.mcp.http"):
            response = await http.request(method, "/mcp/", headers=headers)
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.headers["X-Request-ID"] == "auth-test"
    assert "MCP bearer authentication rejected" in caplog.text
    assert bearer_token not in caplog.text + response.text
    if authorization is not None:
        assert authorization not in caplog.text + response.text


@pytest.mark.usefixtures("enabled_mcp")
async def test_malformed_duplicate_authorization_is_rejected(bearer_token: str) -> None:
    app = create_app()
    async with httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://localhost") as http:
        response = await http.post(
            "/mcp/",
            headers=[("Authorization", f"Bearer {bearer_token}"), ("Authorization", "Bearer other")],
        )
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("headers", "status"), [({"Host": "evil.example"}, 421), ({"Origin": "https://evil.example"}, 403)]
)
@pytest.mark.usefixtures("enabled_mcp")
async def test_sdk_rejects_host_and_origin(headers: dict[str, str], status: int, bearer_token: str) -> None:
    app = create_app()
    async with (
        app.router.lifespan_context(app),
        httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://localhost") as http,
    ):
        response = await http.post(
            "/mcp/",
            json={},
            headers={"Authorization": f"Bearer {bearer_token}", "X-Request-ID": "security-test", **headers},
        )
    assert response.status_code == status
    assert response.headers["X-Request-ID"] == "security-test"


@pytest.mark.usefixtures("enabled_mcp")
async def test_allowed_browser_origin_and_cors_preflight(monkeypatch: pytest.MonkeyPatch, bearer_token: str) -> None:
    origin = "http://localhost:3000"
    monkeypatch.setenv("MCP_ALLOWED_ORIGINS", origin)
    monkeypatch.setenv("CORS_ALLOW_ORIGINS", origin)
    app = create_app()
    async with (
        app.router.lifespan_context(app),
        httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://localhost") as http,
    ):
        preflight = await http.options(
            "/mcp/",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Authorization,Content-Type,MCP-Protocol-Version",
            },
        )
        assert preflight.status_code == 200
        assert preflight.headers["access-control-allow-origin"] == origin
        response = await http.post(
            "/mcp/",
            json={"jsonrpc": "2.0", "id": 1, "method": "server/discover"},
            headers={"Authorization": f"Bearer {bearer_token}", "Origin": origin, "X-Request-ID": "browser-test"},
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin
        assert response.headers["X-Request-ID"] == "browser-test"


@pytest.mark.usefixtures("enabled_mcp")
async def test_factories_own_independent_lifecycles(monkeypatch: pytest.MonkeyPatch) -> None:
    first = create_app()
    second = create_app()
    assert first.state.mcp_server is not second.state.mcp_server
    events: list[str] = []
    original_run = first.state.mcp_server.session_manager.run

    @asynccontextmanager
    async def tracked_run() -> AsyncIterator[None]:
        async with original_run():
            events.append("started")
            try:
                yield
            finally:
                events.append("stopped")

    monkeypatch.setattr(first.state.mcp_server.session_manager, "run", tracked_run)
    async with first.router.lifespan_context(first), second.router.lifespan_context(second):
        assert events == ["started"]
    assert events == ["started", "stopped"]


@pytest.mark.usefixtures("enabled_mcp")
async def test_mcp_startup_failure_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    app = create_app()

    @asynccontextmanager
    async def failing_run() -> AsyncIterator[None]:
        raise RuntimeError("MCP startup failed")
        yield

    monkeypatch.setattr(app.state.mcp_server.session_manager, "run", failing_run)
    with pytest.raises(RuntimeError, match="MCP startup failed"):
        async with app.router.lifespan_context(app):
            pytest.fail("Startup must fail before serving requests")
