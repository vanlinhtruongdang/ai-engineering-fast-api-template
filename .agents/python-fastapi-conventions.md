# Python and FastAPI Conventions

These rules apply to Python code in projects created from this template.

## Python style

- Target Python 3.12 or later.
- Prefer clear, concise code with type hints on public functions and data structures.
- Prefer the standard library before introducing a dependency.
- Choose data structures that fit the operation: `dict` for lookup and `set` for membership.
- Avoid premature optimization, unnecessary copies, and expensive work at import time.
- Cache only stable, measured computations with an appropriate cache boundary.

## Ruff and Ty

Every Python change must pass the configured checks. Ruff enforces correctness, imports, annotations, FastAPI behavior, security, performance, return, and pytest rules. Exceptions are limited to pytest assertions and the container bind host, and are documented in `pyproject.toml`.

```bash
uv run ruff format --check
uv run ruff check
uv run ty check
```

Ty treats invalid arguments, assignments, returns, unresolved imports, and unresolved references as errors. Do not suppress type errors merely because the application runs.

## FastAPI structure

- `app/main.py` is the runnable entry point.
- `app/api/app.py` owns the application factory and middleware registration.
- `app/api/v1/router.py` composes versioned routers.
- `app/api/v1/endpoints/` contains route modules.
- `app/core/` owns settings, logging, security, and infrastructure helpers.
- `app/services/` owns business logic; handlers should remain thin.
- `app/schemas/` owns request and response contracts.
- Use `Depends()` for shared request dependencies where it improves clarity.
- Use a lifespan for startup and shutdown rather than import-time side effects.

## Adding a feature

1. Define or update the contract schema first when the public API changes.
2. Put reusable behavior in a service rather than directly in a route handler.
3. Add persistence layers only when a concrete data-access requirement exists.
4. Add matching tests under the corresponding test area.
5. Measure potential hot paths before optimizing them.
6. For agent or prompt features, define schema validation and failure behavior before prompt wording.
