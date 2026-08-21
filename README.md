# FastAPI Template

A reusable FastAPI foundation for backend services. It provides a small production-oriented core and documents extension paths instead of committing unused application layers.

## Quick start

```bash
uv sync
uv run python -m app.main
```

The API is available at `http://localhost:1114`; interactive documentation is at `/docs` and `/scalar` in development.

```bash
scripts/test-suite.sh default
```

Run the containerized development service with:

```bash
docker compose --env-file .env.dev -f docker-compose.dev.yml up --build
```

## Repository layout

```text
app/
  api/        HTTP application factory, routers, and dependencies
  core/       Settings, logging, middleware, and infrastructure helpers
  schemas/    Pydantic request and response contracts
  services/   Reusable business behavior
tests/        Unit and component tests mirroring application areas
scripts/      Repeatable quality, test, and GitNexus commands
.agents/      Contributor and coding-agent conventions
```

Create `repositories/`, `models/`, and `db/` only when a persistence adapter is needed. Create `agents/` or `pipelines/` only when the project has a concrete agent or multi-step processing contract.

## Quality commands

```bash
uv run ruff format --check
uv run ruff check
uv run ty check
scripts/test-suite.sh default
scripts/test-report.sh default
```

`default` runs local unit and component tests. `integration`, `acceptance`, and `live` lanes are opt-in and are intended for projects that add their matching infrastructure or credentials.

## Configuration

Copy `.env.example` to the environment file used by the selected Compose configuration. The template reads `ENV_FILE` first and defaults to `.env.dev`.

Development defaults keep API documentation available. Production settings must provide explicit `CORS_ALLOW_ORIGINS` and should disable public documentation unless it is intentionally exposed.

See [the architecture guide](docs/fastapi-template-architecture.md) for boundaries, extension paths, health endpoints, and operational conventions.
