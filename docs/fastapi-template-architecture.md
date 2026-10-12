# FastAPI Template Architecture

## Design goals

The template favors a compact, production-oriented HTTP service:

- Keep API contracts, infrastructure, and business behavior separate.
- Keep conventional extension packages discoverable without pre-implementing their behavior.
- Make development ergonomics explicit without making production permissive.
- Provide documented extension seams rather than speculative placeholders.

## Core layout

```text
app/
  main.py                 Application entry point
  api/
    app.py                Application factory and middleware
    dependencies.py       Shared HTTP dependencies
    v1/                   Versioned router and endpoint modules
  core/                   Settings, logging, request context, infrastructure helpers
  mcp/                    Explicit MCP adapters, HTTP auth and stdio entry point
  schemas/                Pydantic request and response contracts
  services/               Business behavior independent of HTTP transport
tests/
  api/                    API contract and middleware tests
  services/               Service behavior tests
  mcp/                    MCP protocol, security and local subprocess checks
```

## Request flow

The application factory loads settings, configures middleware, and mounts the versioned router. An endpoint handles HTTP input and delegates reusable behavior to a service. The current health service returns a `HealthResponse`; projects adding error paths must define their status codes and response contracts at the API boundary.

## MCP boundary

`app/mcp/` exposes the health service as `get_health_status` and the shared
metadata service as the JSON resource `app://info`. REST and MCP use the same
schemas; `/api/v1/` retains its metadata fields. HTTP mounts at `/mcp/` only
when enabled with valid bearer and Host/Origin configuration. The parent
FastAPI lifespan owns the SDK session manager. Each factory creates a separate
server; stdio uses the same capability factory without importing the HTTP app.

The official SDK v2 owns protocol handling. The baseline uses stateless JSON
responses for legacy HTTP clients and supports modern discovery. Shared-token
access is limited to team-controlled internal clients. Read the
[MCP architecture](mcp/architecture.md) and [operations reference](mcp/reference.md)
before extending capabilities or deploying to a remote hostname.

## Health and readiness

`/health` is a liveness endpoint and must not depend on optional infrastructure. `/ready` reports whether enabled mandatory dependencies are usable. Projects add dependency checks only when they add the dependency itself.

## Extension packages

- `repositories/`, `models/`, and `db/` are placeholders for a persistence boundary.
- `agents/` is reserved for a defined agent input/output contract.
- `pipelines/` is reserved for a concrete multi-step processing flow.
- `common/` and `utils/` are available for narrowly scoped shared code.
- Keep these packages empty until the matching capability is needed.

## Testing model

Tests use one primary taxonomy marker: `unit`, `component`, `integration`, `acceptance`, or `live`. The default lane runs without infrastructure or credentials. Projects opt into the additional lanes when their requirements and fixtures exist.
