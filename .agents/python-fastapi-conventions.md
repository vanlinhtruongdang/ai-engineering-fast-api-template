# Python and FastAPI conventions

These are the baseline conventions for this template and for projects that retain its structure. Check `pyproject.toml` and the current implementation before copying a rule into a derived service.

## Python and quality tools

- Use Python `>=3.12,<3.14`, as declared in `pyproject.toml`; Ruff targets Python 3.12. Add type hints to public functions and data structures. Prefer direct, readable code and the standard library before a new dependency.
- Install the locked development environment with `uv sync --locked`. Ruff and Ty are development dependencies, not runtime dependencies. Run `uv run ruff format --check`, `uv run ruff check`, and `uv run ty check` for Python changes; `scripts/verify.sh` also runs the default test lane.
- Follow the configured Ruff rule set and Ty error rules in `pyproject.toml`. The only current Ruff file exceptions cover pytest assertions and the container bind host. Do not silence a diagnostic without explaining a concrete false positive or boundary.
- Avoid expensive work at import time. Cache only stable computations at a boundary whose invalidation is understood. Optimize after measurement.

## Module ownership and request flow

| Layer | Responsibility |
| --- | --- |
| `app/main.py` | Importable `app` and local `python -m app.main` entry point |
| `app/api/app.py` | App factory, lifespan, middleware, global probe routes, router mount, documentation exposure |
| `app/api/v1/router.py` and `endpoints/` | Versioned route composition, HTTP inputs and outputs |
| `app/api/dependencies.py` | Shared HTTP dependencies where FastAPI injection helps |
| `app/schemas/` | Pydantic request and response contracts |
| `app/services/` | Reusable behavior independent of HTTP transport |
| `app/core/` | Settings, logging, request context, and cross-cutting infrastructure |

For a new endpoint, define the request/response contract, add a route under the versioned router, put reusable behavior in a service, and add focused contract/behavior checks. Keep handlers thin but do not create a service that only renames one obvious expression. Add `db/`, `models/`, and `repositories/` behavior only with a real persistence requirement; add `agents/` or `pipelines/` behavior only with a defined AI or workflow contract.

## API invariants

- Keep existing versioned paths under the configurable `API_PREFIX` (default `/api/v1`). Root `/health` and `/ready` are unversioned probes and excluded from OpenAPI. The current versioned health and system routes are in `app/api/v1/`.
- `/health` is liveness. `/ready` must reflect enabled mandatory dependencies once a project adds them; the dependency-free baseline returns `ok`. Do not let an optional dependency fail liveness.
- Declare response contracts with Pydantic schemas where the API shape matters. Validate external input at the boundary; do not rely on prompt wording or downstream provider behavior for stable rules. Make failure status and response shape explicit when a new route can fail.
- Keep blocking calls out of async request paths. Initialize and close long-lived resources in lifespan; avoid hidden clients and side effects at module import.
- Preserve request ID propagation through `attach_request_id`. Treat inbound headers and logs as untrusted input; do not log secrets, raw prompts, model responses, or sensitive payloads.

## Settings and deployment

`APISettings` and `LoggingSettings` use `ENV_FILE` (default `.env.dev`) as their file source, with environment values taking precedence through Pydantic Settings. The file path is selected when `app/core/config.py` is imported, so set `ENV_FILE` before importing the app. `get_settings()` and `get_logging_settings()` are cached; tests that change values must clear or override those caches deliberately and restore state afterward. Add a setting only for a real runtime choice and update `.env.example`, deployment files, and docs that depend on it.

Production `create_app()` rejects wildcard `CORS_ALLOW_ORIGINS`; production deployment must name trusted origins. `DOCS_ENABLED` controls OpenAPI and both interactive documentation UIs. Keep development convenience settings from leaking into public deployments. Never commit real secrets or expose them in examples.
