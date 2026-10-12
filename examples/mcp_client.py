"""Run from the repository root with `uv run python examples/mcp_client.py stdio|http`."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import httpx2
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.exceptions import MCPError
from mcp_types import TextResourceContents

from app.core.config import get_mcp_settings
from app.schemas.health import HealthResponse
from app.schemas.info import SystemInfoResponse


async def show_capabilities(client: Client) -> int:
    print(f"Protocol: {client.protocol_version}")
    print("Tools:", [tool.name for tool in (await client.list_tools()).tools])
    print("Resources:", [str(resource.uri) for resource in (await client.list_resources()).resources])
    result = await client.call_tool("get_health_status")
    if result.is_error:
        print("MCP tool failed (is_error=true).", file=sys.stderr)
        return 1
    health = HealthResponse.model_validate(result.structured_content)
    print("Health:", json.dumps(health.model_dump()))
    resource = await client.read_resource("app://info")
    content = resource.contents[0]
    if not isinstance(content, TextResourceContents) or content.mime_type != "application/json":
        raise ValueError("Expected JSON text resource")
    print("Info:", SystemInfoResponse.model_validate_json(content.text).model_dump_json())
    return 0


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transport", choices=("http", "stdio"))
    parser.add_argument("--url", default="http://localhost:1114/mcp/")
    args = parser.parse_args()
    try:
        if args.transport == "stdio":
            parameters = StdioServerParameters(
                command=sys.executable,
                args=["-m", "app.mcp"],
                cwd=Path(__file__).resolve().parents[1],
                env=dict(os.environ),
            )
            async with Client(parameters, read_timeout_seconds=10) as client:
                return await show_capabilities(client)

        token = get_mcp_settings().bearer_token
        if token is None or not token.get_secret_value():
            print("Set MCP_BEARER_TOKEN in the environment or selected ENV_FILE.", file=sys.stderr)
            return 1
        async with (
            httpx2.AsyncClient(headers={"Authorization": f"Bearer {token.get_secret_value()}"}, timeout=10) as http,
            Client(streamable_http_client(args.url, http_client=http), read_timeout_seconds=10) as client,
        ):
            return await show_capabilities(client)
    except* (httpx2.HTTPError, OSError, TimeoutError):
        print("MCP transport failed; check endpoint, credentials, Host/Origin and process startup.", file=sys.stderr)
    except* MCPError:
        print("MCP request rejected; check capability names, HTTP auth/Host/Origin and server logs.", file=sys.stderr)
    except* ValueError:
        print("MCP configuration or response failed validation.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
