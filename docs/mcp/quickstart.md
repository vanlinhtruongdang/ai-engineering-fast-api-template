# Connect to the MCP server

Run these commands from the repository root with Python 3.12 and `uv` installed.
This tutorial ends with a discovered tool, a structured health result and the
application metadata resource. REST works immediately after a fresh clone;
MCP HTTP requires explicit configuration.

## Install the locked environment

```bash
uv sync --locked
```

## Try stdio first

The example starts `python -m app.mcp` with the same locked interpreter, calls
the capabilities and closes the subprocess with the SDK context manager:

```bash
uv run python examples/mcp_client.py stdio
```

Expect `Protocol: 2026-07-28`, the tool `get_health_status`, the resource
`app://info` and `Health: {"status": "ok"}`. Stdio needs no HTTP token.

For an MCP host that manages the process, use command `uv`, arguments
`["run", "python", "-m", "app.mcp"]` and this repository as its working
directory. Set `ENV_FILE` in the host's process environment if you use a
different configuration file. Launching the server directly waits for an MCP
client on stdin; ordinary terminal text is not a protocol request.

## Enable HTTP with a private local token file

Create a new local configuration file. This command refuses to overwrite an
existing file, creates it with owner-only permissions and prints no token:

```bash
uv run python - <<'PY'
import os
import secrets

fd = os.open(".env.mcp.local", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as config:
    config.write(
        "MCP_ENABLED=true\n"
        f"MCP_BEARER_TOKEN={secrets.token_urlsafe(32)}\n"
        "SERVER_RELOAD=false\n"
        "LOG_DIR=/tmp/fastapi-template-logs\n"
    )
print("Created .env.mcp.local")
PY
```

`.env.*.local` files are ignored. The versioned `.env.dev`, `.env.staging`,
`.env.production` and `.env.example` files contain defaults and placeholders,
including an invalid token placeholder that must be replaced before enabling
HTTP. Keep real tokens in private overrides or deployment secret injection;
agree deployment values with DevOps. Environment variables override file
values, so remove stale `MCP_*` overrides before diagnosing this tutorial.

Start the application in one terminal:

```bash
ENV_FILE=.env.mcp.local uv run python -m app.main
```

Run the client in another terminal:

```bash
ENV_FILE=.env.mcp.local uv run python examples/mcp_client.py http
```

The endpoint is `http://localhost:1114/mcp/`, including the trailing slash.
The client reads the token from the selected configuration file and sends
`Authorization: Bearer ...` on each HTTP request. It checks `is_error` before
using `structured_content`, validates the JSON resource, and closes both
HTTP and MCP contexts. Transport exceptions, MCP request rejection and tool
failures have distinct messages and return a nonzero exit status. SDK v2 can
represent an HTTP rejection as an `MCPError`; check server logs for its status.
Stop the server with Ctrl+C.

For an already configured server, pass its URL and supply its token through
your environment or selected `ENV_FILE`:

```bash
uv run python examples/mcp_client.py http --url http://localhost:1114/mcp/
```

Use HTTPS for a remote endpoint. Remote hostnames must appear in the server's
`MCP_ALLOWED_HOSTS`; see [operations](reference.md).

## Inspect capabilities interactively

With Node.js 22.19.0 or newer, the [official MCP Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector)
can launch the stdio server:

```bash
npx @modelcontextprotocol/inspector uv run python -m app.mcp
```

This downloads a separate optional tool. Follow the local URL printed by
Inspector, connect with stdio, list tools/resources, call `get_health_status`
and read `app://info`. Inspector clients that use initialization are supported
by the legacy path.

For the Inspector browser's Streamable HTTP mode, declare its actual origin
in both `MCP_ALLOWED_ORIGINS` and `CORS_ALLOW_ORIGINS`, then restart the app.
Use `/mcp/` and its bearer authorization field. The default empty MCP Origin
allowlist deliberately rejects browser requests. Do not place tokens in URLs
or screenshots.

## Check the local contract

```bash
scripts/test-suite.sh component tests/mcp
scripts/verify.sh
```

The suite includes controlled in-process HTTP and real local stdio processes.
It does not contact a provider or require a production credential. See
[reference](reference.md) for `401`, `403`, `421` and lifecycle failures.
