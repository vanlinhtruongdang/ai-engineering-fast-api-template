from functools import partial

import httpx2
import pytest
from mcp import Client

from app.api.app import create_app
from app.core.config import get_mcp_settings, get_settings
from app.mcp import create_server
from examples.mcp_client import main, show_capabilities


@pytest.mark.parametrize("authorized", [True, False])
@pytest.mark.usefixtures("enabled_mcp")
async def test_http_example(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], bearer_token: str, authorized: bool
) -> None:
    app = create_app()
    monkeypatch.setattr("sys.argv", ["mcp_client.py", "http", "--url", "http://localhost/mcp/"])
    monkeypatch.setattr(httpx2, "AsyncClient", partial(httpx2.AsyncClient, transport=httpx2.ASGITransport(app=app)))
    if not authorized:
        monkeypatch.setenv("MCP_BEARER_TOKEN", bearer_token + "wrong")
        get_mcp_settings.cache_clear()
    async with app.router.lifespan_context(app):
        exit_code = await main()
    output = capsys.readouterr()
    if authorized:
        assert exit_code == 0
        assert 'Health: {"status": "ok"}' in output.out
        assert '"name":"FastAPI Template"' in output.out
    else:
        assert exit_code == 1
        assert "MCP request rejected" in output.err
    assert bearer_token not in output.out + output.err


async def test_example_checks_tool_error_before_using_output(capsys: pytest.CaptureFixture[str]) -> None:
    server = create_server(get_settings())
    server.remove_tool("get_health_status")
    async with Client(server) as client:
        exit_code = await show_capabilities(client)
    assert exit_code == 1
    output = capsys.readouterr()
    assert "MCP tool failed (is_error=true)" in output.err
    assert "Health:" not in output.out
