import asyncio
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryFile

import pytest
from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp_types import TextResourceContents


@pytest.mark.parametrize(("mode", "version"), [("auto", "2026-07-28"), ("legacy", "2025-11-25")])
async def test_sdk_stdio_process(mode: str, version: str, tmp_path: Path) -> None:
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp"],
        env={"ENV_FILE": os.devnull, "LOG_DIR": str(tmp_path), "LOG_LEVEL": "DEBUG", "MCP_ENABLED": "true"},
    )
    # HTTP settings deliberately lack a token; stdio never creates the HTTP application.
    with TemporaryFile(mode="w+", encoding="utf-8") as stderr:
        async with Client(stdio_client(parameters, errlog=stderr), mode=mode, read_timeout_seconds=5) as client:
            assert client.protocol_version == version
            assert [tool.name for tool in (await client.list_tools()).tools] == ["get_health_status"]
            result = await client.call_tool("get_health_status")
            assert not result.is_error
            assert result.structured_content == {"status": "ok"}
            resource = (await client.read_resource("app://info")).contents[0]
            assert isinstance(resource, TextResourceContents)
            assert json.loads(resource.text)["name"] == "FastAPI Template"
            assert (await client.call_tool("unknown_tool")).is_error
        stderr.seek(0)
        assert "Unknown tool" in stderr.read()
    assert "Unknown tool" in (tmp_path / "app.log").read_text(encoding="utf-8")


async def test_stdio_stdout_is_only_protocol_and_process_exits(tmp_path: Path) -> None:
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "app.mcp",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "ENV_FILE": os.devnull, "LOG_DIR": str(tmp_path), "LOG_LEVEL": "DEBUG"},
    )
    try:
        assert process.stdin is not None
        assert process.stdout is not None
        meta = {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {"name": "stdout-test", "version": "1"},
        }
        for request_id, method, params in (
            (1, "server/discover", {"_meta": meta}),
            (
                2,
                "tools/call",
                {
                    "name": "get_health_status",
                    "arguments": {},
                    "_meta": meta,
                },
            ),
        ):
            message = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
            process.stdin.write((json.dumps(message) + "\n").encode())
            await process.stdin.drain()
            response = json.loads(await asyncio.wait_for(process.stdout.readline(), timeout=5))
            assert response["jsonrpc"] == "2.0"
            assert response["id"] == request_id
            assert "result" in response
        process.stdin.close()
        remaining_stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5)
        assert process.returncode == 0
        assert remaining_stdout == b""
        assert b"DEBUG" in stderr
    finally:
        if process.returncode is None:
            process.kill()
            await process.wait()


async def test_stdio_example_runs_with_locked_interpreter(tmp_path: Path) -> None:
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "examples/mcp_client.py",
        "stdio",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "ENV_FILE": os.devnull, "LOG_DIR": str(tmp_path)},
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
        assert process.returncode == 0, stderr.decode()
        assert b"Protocol: 2026-07-28" in stdout
        assert b'Health: {"status": "ok"}' in stdout
        assert b"app://info" in stdout
    finally:
        if process.returncode is None:
            process.kill()
            await process.wait()
