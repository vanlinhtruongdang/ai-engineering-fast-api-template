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
  schemas/                Pydantic request and response contracts
  services/               Business behavior independent of HTTP transport
tests/
  api/                    API contract and middleware tests
  services/               Service behavior tests
```

## Request flow

The application factory loads settings, configures middleware, and mounts the versioned router. An endpoint handles HTTP input and delegates reusable behavior to a service. The current health service returns a `HealthResponse`; projects adding error paths must define their status codes and response contracts at the API boundary.

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
