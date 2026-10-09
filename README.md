# FastAPI template for AI engineering projects

A small, typed HTTP foundation for teams building model-backed APIs, agents, and data workflows. The template provides application setup, configuration, logging, health endpoints, local tests, quality checks, and container packaging. It leaves model providers, storage, queues, and orchestration to the first use case that needs them.

## Start locally

Use Python 3.12 and `uv` to create the locked development environment. The repository already includes a development environment file; review `.env.dev` before starting and keep real credentials out of tracked files.

```bash
uv sync --locked
uv run python -m app.main
```

The default server listens on `http://localhost:1114`. Open `/docs` or `/scalar` for the development API reference. Check `/health` for liveness, `/ready` for baseline readiness, or `/api/v1/` for application metadata. Stop the local server with Ctrl+C.

```bash
scripts/verify.sh
```

`scripts/verify.sh` runs Ruff formatting and lint checks, Ty type checking, and the default local test lane. CI runs the same gate after `uv sync --locked --all-groups` and also builds the container image.

## What is included

| Area | Current implementation |
| --- | --- |
| HTTP | FastAPI application factory, versioned router, OpenAPI and Scalar in development |
| Operations | Root liveness and readiness endpoints, request ID middleware, CORS configuration |
| Configuration | Pydantic Settings loaded from `ENV_FILE` or `.env.dev`, with environment variable overrides |
| Logging | Console and rotating file handlers; JSON format can be enabled through settings |
| Delivery | Locked Python dependencies, Dockerfile, development/staging/production Compose files, CI quality and image build jobs |
| Quality | Ruff, Ty, pytest lanes, branch coverage report command, GitNexus guidance for code changes |

The current readiness check reports `ok` because this baseline has no mandatory external dependency. Adding a database or provider requires a corresponding readiness policy; the template does not supply that integration.

## Tooling for contributors

| Tool | Role in this repository | Required for |
| --- | --- | --- |
| Python 3.12 and `uv` | Runtime and locked Python environment | Local app and Python checks |
| Ruff | Formatter and linter, installed by `uv sync --locked` | Python changes and CI |
| Ty | Static type checker, installed by `uv sync --locked` | Python changes and CI |
| pytest, HTTPX, pytest-cov | Local tests and coverage, installed with the dev group | Test and coverage commands |
| GitNexus CLI | Dependency/impact index; repository alias `fastapi_template` | Agents and contributors changing existing code or making commits under [repository rules](AGENTS.md) |
| Node.js | Runs the local `.gitnexus/run.cjs` status helper | Checking GitNexus index status |
| Docker with Compose | Container build and environment-specific local deployment | Container workflows |
| Draw.io (diagrams.net) | Edits `.drawio` sources and exports diagram screenshots | Creating or updating project diagrams; Desktop CLI is needed for command-line PNG export |
| Bun | JavaScript/TypeScript runtime and package manager | Optional if a derived project adds JS/TS tooling; this repository has no Bun application or package manifest |

Ruff and Ty are declared in the `dev` group of [`pyproject.toml`](pyproject.toml); do not install separate global copies to satisfy this project's checks. GitNexus, Draw.io, and Bun are external tools and are not Python dependencies. On a fresh checkout, create the local GitNexus index with `scripts/gitnexus-refresh.sh`; later check `node .gitnexus/run.cjs status` and refresh through the same script when stale. See the [GitNexus guide](.agents/gitnexus-guidelines.md).

## Repository layout

```text
app/
  main.py       importable app and local server entry point
  api/          app factory, middleware, dependencies, versioned endpoints
  core/         settings, logging, request context
  schemas/      Pydantic API contracts
  services/     behavior independent of HTTP transport
  agents/       empty until an agent has a defined contract
  pipelines/    empty until a multi-step workflow is needed
  db/, models/, repositories/, common/, utils/   empty extension packages
tests/          in-process API and service checks, pytest lane contract
scripts/        verification, test, coverage, and GitNexus commands
.agents/        coding, testing, writing, and diagram rules
```

The request path is `app/main.py` → `app/api/app.py` → versioned endpoint → service → response schema. Start a new API capability by defining its input/output contract, adding the endpoint and reusable service behavior, and checking the public response. For AI features, define provider permissions, validation, failure behavior, and audit evidence before adding code to `app/agents/` or `app/pipelines/`. The [architecture guide](docs/fastapi-template-architecture.md) explains the existing boundaries.

## Configuration and deployment

[`app/core/config.py`](app/core/config.py) defines defaults and supported environment variables. `ENV_FILE` selects an environment file and defaults to `.env.dev`. [`.env.example`](.env.example) lists the setting names and development-oriented sample values. The three Compose files select `.env.dev`, `.env.staging`, and `.env.production` respectively; review the selected file before use.

Production mode rejects `CORS_ALLOW_ORIGINS=*`. Set explicit trusted origins, review `DOCS_ENABLED`, and disable `SERVER_RELOAD` for deployments. The production Compose command runs Uvicorn without reload. Store secrets through the deployment environment; tracked example or environment files must not contain real credentials.

For local container development:

```bash
docker compose --env-file .env.dev -f docker-compose.dev.yml up --build
```

## Quality and test lanes

```bash
uv run ruff format --check
uv run ruff check
uv run ty check
scripts/test-suite.sh default
scripts/test-report.sh default
```

The default lane runs unit and in-process component tests without optional infrastructure. `integration`, `acceptance`, and `live` are separate lanes for projects that add their fixtures and dependencies; live provider tests require explicit authorization. `scripts/test-report.sh default` writes local coverage artifacts under `reports/tests/` without a coverage threshold. See the [testing guide](.agents/testing-guidelines.md) for lane rules.

Coding agents start with [AGENTS.md](AGENTS.md); Claude Code uses [CLAUDE.md](CLAUDE.md) as a pointer to the same rules. The [contributor guide](.agents/README.md) maps conventions to each kind of task. For diagrams, use the [component library](assets/diagrams/README.md) and follow the [diagram guide](.agents/diagram-guidelines.md) for the editable source, screenshot, reading guide, and references.
