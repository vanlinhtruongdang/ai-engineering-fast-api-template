# MCP architecture and research

This explanation is for developers choosing how to add MCP capabilities to a
service built from this template. Sources and the installed SDK were checked on
2026-10-12. The dependency range is `mcp>=2.3.0,<3.0`; `uv.lock` resolves it to
`mcp==2.3.0` and `mcp-types==2.3.0`.

## SDK and exposure decision

The [official Python SDK](https://github.com/modelcontextprotocol/python-sdk)
provides `MCPServer`, typed registration and the `Client` used in this repository.
It owns JSON-RPC, protocol schemas, transport framing and request limits. The
template adds service adapters and its internal-client HTTP authentication.

| Approach | Fit for this template |
| --- | --- |
| Explicit registration with the official SDK | Selected. Each capability has a named service, schema and permission boundary; no second MCP framework is required. |
| Standalone FastMCP | An alternative framework with its own integration APIs. It is not an installed dependency here. |
| FastMCP conversion from FastAPI/OpenAPI | Useful when an existing HTTP API is the intended MCP surface. Requires reviewing route mappings and inherited authentication rather than assuming every REST route should become a capability. |

[FastMCP's FastAPI integration](https://gofastmcp.com/integrations/fastapi)
documents `FastMCP.from_fastapi`, OpenAPI route mapping and mounting an MCP app.
This template registers only the two requested capabilities because the REST
API and the MCP interface have different callers and exposure policies.

## Ownership and lifetime

REST routes in `app/api/` and MCP handlers in `app/mcp/` call the same services.
`HealthResponse` owns the health output. `get_system_info()` and
`SystemInfoResponse` own the four metadata fields: `status`, `name`, `version`
and `environment`. The REST response at `/api/v1/` retains those fields; the
MCP resource serializes the same schema to JSON text.

Each `create_app()` creates its own MCP server when HTTP is enabled. The
mounted SDK app has an internal route `/`, making the public endpoint `/mcp/`.
FastAPI's parent lifespan enters `server.session_manager.run()` and closes it
on shutdown. Initialization failures propagate instead of leaving a running
REST app with a broken enabled MCP endpoint. The SDK's
[ASGI mounting guide](https://py.sdk.modelcontextprotocol.io/run/asgi/)
explains why a mounted sub-application's lifespan does not start its manager.

`python -m app.mcp` configures existing logging and creates a server without
importing `app.main` or starting FastAPI. HTTP enablement and bearer settings
are not read by this entry point. Protocol goes to stdout; application logging
uses stderr and the configured rotating file.

## Protocol and transport decision

SDK v2 supports modern `2026-07-28` discovery and the older initialize
handshake. Its [protocol-version guide](https://py.sdk.modelcontextprotocol.io/protocol-versions/)
describes `Client`'s default `auto` mode: probe `server/discover`, then fall back
to initialization against older servers. `mode="legacy"` uses initialization;
the tested version is `2025-11-25`.

HTTP uses Streamable HTTP. Legacy requests use `stateless_http=True` and
`json_response=True`, avoiding stored sessions and a persistent event stream.
Modern requests also carry their own protocol context. The two baseline
capabilities need no subscriptions, server-initiated callbacks or conversation
state; subscriptions are disabled explicitly. Do not infer durable execution,
resumable notifications or exactly-once effects from this transport.

## Authentication boundary

HTTP is opt-in and requires a shared bearer token plus SDK Host/Origin
allowlists. The [SDK deployment guide](https://py.sdk.modelcontextprotocol.io/run/deploy/)
explains DNS-rebinding protection and TLS proxy handling. This template keeps
that protection enabled and provides no switch to bypass it.

The shared token is a decision for team-controlled internal clients. It grants
the same access to every holder and supplies no user identity, per-user scopes,
OAuth discovery or token issuer. External clients require an identity provider
and a resource-server design using the
[SDK authorization APIs](https://py.sdk.modelcontextprotocol.io/run/authorization/).
That integration must verify issuer, audience/resource, expiry and scopes, with
permission checks at each protected capability. Tool annotations describe
behavior; they do not enforce permission.

## Verification boundary

`tests/mcp/` exercises both protocol eras through the mounted HTTP app and a
real SDK stdio subprocess, checks discovery and structured output, and covers
configuration, bearer rejection, Host/Origin, CORS preflight and lifespan.
REST checks verify the metadata and probe responses. The raw stdio subprocess
test checks protocol-only stdout and exit on stdin closure.

The client example uses the locked SDK and validates outputs with shared
schemas. Local checks do not prove an organization's reverse proxy, TLS
certificate, browser host, external identity provider or production network.
