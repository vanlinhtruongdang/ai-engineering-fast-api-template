# MCP reference and operations

This reference describes the shipped baseline for developers and operators.
HTTP and stdio expose the same explicitly registered capabilities.

## Capabilities and entry points

| Interface | Contract |
| --- | --- |
| Streamable HTTP | `/mcp/` on the existing FastAPI listener; default local port `1114`. Independent of `API_PREFIX`. `/mcp` redirects to the canonical trailing-slash path when enabled. Both paths return `404` when disabled. |
| Stdio | `uv run python -m app.mcp`; no FastAPI app, HTTP bearer token or listener. The launching OS user/host owns local process access. |
| Tool `get_health_status` | No arguments. `HealthResponse`, structured JSON `{"status":"ok"}`. Read-only, non-destructive, idempotent and closed-world annotations. Baseline liveness checks no external dependency. |
| Resource `app://info` | JSON text, MIME `application/json`: `status`, `name`, `version`, `environment`, using the shared REST metadata service/schema. |
| Prompts | None registered. |

`DOCS_ENABLED` controls REST documentation and does not control MCP. Discovery
is available through authenticated MCP calls, independently of OpenAPI.

## Configuration

`MCPSettings` in `app/core/config.py` uses `ENV_FILE` (default `.env.dev`), with
environment variables taking precedence. The file is selected at module
import. `get_mcp_settings()` caches settings; restart deployed processes after
changing values. Tests clear the cache and read an empty environment file.

| Variable | Default | Validation and effect |
| --- | --- | --- |
| `MCP_ENABLED` | `false` | Controls the HTTP mount only. |
| `MCP_BEARER_TOKEN` | Unset | Required for enabled HTTP. At least 32 ASCII bearer-token characters; whitespace is invalid. `SecretStr` masks representations and configuration errors omit input values. |
| `MCP_ALLOWED_HOSTS` | `localhost,localhost:*,127.0.0.1,127.0.0.1:*,[::1],[::1]:*` | Comma-separated Host values. Bare host, exact port or `:*`; no scheme, path, credentials or hostname wildcard. At least one entry. IPv6 uses brackets. |
| `MCP_ALLOWED_ORIGINS` | Empty | Comma-separated exact `http://` or `https://` origins with optional port. No path, credentials or wildcard. Absent Origin is allowed; present Origin must match. |

HTTP configuration is checked by `create_app()` before startup. Invalid
allowlists fail configuration even when HTTP is disabled. Stdio does not load
`MCPSettings`. Token characters follow `[A-Za-z0-9._~+/-]+=*`; generate random
tokens rather than treating length as sufficient entropy. Versioned environment
templates contain `<replace-with-a-random-token-at-deployment>`, which fails
token validation if HTTP is enabled without replacing it.

## Authentication and browser access

The mount's ASGI middleware requires exactly one
`Authorization: Bearer <token>` header and compares it with
`secrets.compare_digest`. Missing, incorrect or malformed credentials return
`401` with `WWW-Authenticate: Bearer`. It protects all HTTP methods and
subpaths. FastAPI's existing CORS middleware handles browser preflight before
the bearer middleware; actual requests still require authorization.

After bearer authentication, the SDK enforces DNS-rebinding protection:
unlisted Host returns `421`; unlisted Origin returns `403`. Host entries match
literal header values. List a bare hostname and its port variant when both
are expected. CORS permission alone does not authorize an MCP Origin.

Browser clients need the same explicit origins in `MCP_ALLOWED_ORIGINS` and
`CORS_ALLOW_ORIGINS`. Configure `CORS_ALLOW_METHODS` to permit `POST`, `GET`,
`DELETE` and `OPTIONS` as needed, and `CORS_ALLOW_HEADERS` to permit
`Authorization`, `Content-Type`, `Accept` and `MCP-Protocol-Version`.
Expose `X-Request-ID` through `CORS_EXPOSE_HEADERS` if browser code reads it.
This stateless setup issues no session ID; a future session-based transport
would also need MCP session headers in the CORS policy.

All token holders have the same access. There is no OAuth metadata endpoint,
user identity or per-client policy. Before supporting external clients, use
the SDK resource-server authorization integration with your IdP and validate
issuer, audience/resource, token expiry and scopes at the protected operations.
The [SDK authorization guide](https://py.sdk.modelcontextprotocol.io/run/authorization/)
defines that separate boundary.

## Deploy on the existing listener

Compose already reads `.env.dev`, `.env.staging` or `.env.production` through
`env_file`. These files and `.env.example` may be versioned as complete
templates containing defaults and explicit placeholders. Agree actual origins,
Host values and credentials with DevOps, then supply real tokens through
deployment secret injection or a private untracked override. For Compose,
provide private values through a deployment-specific `env_file` override.
No MCP service or extra port is needed. `.dockerignore` excludes environment
files from the image. Never put real credentials in the versioned templates;
local `.env.*.local` overrides are ignored by Git.

Use HTTPS for remote clients. At a TLS-terminating reverse proxy:

1. Preserve the intended public Host and allowlist exactly that value. If the
   proxy rewrites Host, allowlist its controlled upstream value and enforce
   public Host routing at the proxy.
2. Forward `/mcp/` including its trailing slash to the FastAPI listener. Pass
   `Authorization`, `Content-Type`, `Accept` and `MCP-Protocol-Version`; avoid
   logging Authorization or request bodies.
3. Trust forwarded headers only from the proxy's actual network addresses.
   For a proxy at `127.0.0.1`, an illustrative Uvicorn command is:

   ```bash
   uv run uvicorn app.main:app --host 127.0.0.1 --port 1114 --proxy-headers --forwarded-allow-ips 127.0.0.1
   ```

   Change the trusted address to match the deployment. Do not trust arbitrary
   forwarded headers or disable SDK Host/Origin protection.

These settings follow the [SDK deployment guidance](https://py.sdk.modelcontextprotocol.io/run/deploy/).
Rotate the shared token in the server and all clients, then restart processes;
the baseline does not implement overlapping tokens or per-client revocation.

## Lifecycle, limits and errors

The FastAPI parent lifespan starts the MCP session manager and closes it on
shutdown. Enabled MCP startup failure fails application startup. Each app
factory owns a separate server. The SDK enforces its default HTTP body limit
of 4 MiB; this template does not override it.

Legacy HTTP uses JSON responses and no stored session. Modern requests carry
their own protocol context. There are no enabled subscriptions, event store,
durable runs or server-initiated callbacks. Adding a mutating tool still needs
explicit authorization, validation and idempotency independent of transport.

`is_error=true` indicates a tool failure, including an unknown tool in this
SDK. A successful tool has `structured_content`. JSON-RPC failures raise
`MCPError`; SDK v2 also synthesizes `MCPError` for some non-JSON-RPC HTTP
rejections, so server logs identify their HTTP status. Connection and process
failures are transport exceptions and can be nested in exception groups. The
client example reports request rejection, transport exceptions and tool failure
separately and exits nonzero instead of consuming a failed result.

Normal MCP HTTP responses, including bearer and SDK security rejections,
reuse the existing request ID response header. Authentication rejection logs
a fixed warning with no credential. SDK and application logs use the existing
console/file configuration; stdio stdout is reserved for protocol. Keep log
verbosity and access logging consistent with the data handled by new tools.

| Symptom | Check |
| --- | --- |
| `404` at `/mcp/` | `MCP_ENABLED` and the process's selected `ENV_FILE`; restart after edits. |
| Startup validation error | Token presence/format and allowlist syntax. Never paste the real token into a report. |
| `401` | Exactly one bearer header, current token in both client and server, proxy header forwarding. |
| `421` | Actual Host header, including port, against `MCP_ALLOWED_HOSTS`. |
| `403` | Actual Origin against `MCP_ALLOWED_ORIGINS`; also check browser CORS policy. |
| `413` | SDK HTTP request body limit; split the input contract if large inputs are expected. |
| `405` on GET with a legacy client | The stateless legacy setup has no persistent GET event stream. Use normal request/response tools. |
| Task group not initialized | Parent app lifespan did not enter `session_manager.run()`. ASGI test transports do not start lifespan automatically. |
| Stdio hangs or logs appear as protocol | Correct command/interpreter/working directory, writable log directory, no imports of `app.main`, and no prints to stdout in handlers. |
