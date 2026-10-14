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
| MCP | Official SDK v2, opt-in Streamable HTTP at `/mcp/` with bearer/Host/Origin protection, independent stdio, shared health and metadata services |
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
| Node.js | Runs GitNexus CLI and the local `.gitnexus/run.cjs` status helper; GitNexus 1.6.12 requires `^22.18.0` or `>=24.11.0` | GitNexus commands, even when installed through Bun |
| Docker with Compose | Container build and environment-specific local deployment | Container workflows |
| Draw.io (diagrams.net) | Edits `.drawio` sources and exports diagram screenshots | Creating or updating project diagrams; Desktop CLI is needed for command-line PNG export |
| Bun | Runs `bunx` for agent skill installation; can also manage JS/TS tooling | Running `scripts/install-skills.sh`, or optional JS/TS work |
| `jq` | Reads and validates the skill source catalog | Running `scripts/install-skills.sh` |

Ruff and Ty are declared in the `dev` group of [`pyproject.toml`](pyproject.toml); do not install separate global copies to satisfy this project's checks. GitNexus, Draw.io, and Bun are external tools and are not Python dependencies. On a fresh checkout, create the local GitNexus index with `scripts/gitnexus-refresh.sh`; later check `node .gitnexus/run.cjs status` and refresh through the same script when stale. See the [GitNexus guide](.agents/gitnexus-guidelines.md).

Installing GitNexus or its skills does not install Node.js. If `gitnexus --version` fails with `/usr/bin/env: node: No such file or directory`, install a supported Node.js runtime and ensure `node --version` works in the same shell before refreshing the index.

Optional coding-agent skills are listed in [`skills-catalog.json`](skills-catalog.json). With Bun and `jq` installed, run [`scripts/install-skills.sh`](scripts/install-skills.sh) to install each listed skill through `bunx skills add`. The entries identify upstream sources but do not pin revisions; review them before running the installer. The catalog remains unchanged; the CLI writes its own ignored `skills-lock.json` in the repository root. The installer attempts every entry, reports failed skill names, and exits with status 1 if any failed. An optional first argument selects another catalog file; its filename must differ from `skills-lock.json`.

The installer targets both Codex and Claude Code. Codex reads the downloaded skills in `.agents/skills/`; the CLI creates Claude Code links in `.claude/skills/`. Both directories are ignored by Git. [Codex](https://developers.openai.com/codex/skills/) can select skills from their descriptions or through an explicit `$skill-name` mention; [Claude Code](https://code.claude.com/docs/en/skills) can select them when relevant or through `/skill-name`. Discovery does not mean every skill runs on every request, and individual skill policies can disable automatic invocation. If a new skill does not appear, restart the agent session.

## Repository layout

```text
app/
  main.py       importable app and local server entry point
  api/          app factory, middleware, dependencies, versioned endpoints
  core/         settings, logging, request context
  mcp/          explicit MCP capabilities, HTTP authentication, stdio entry point
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

## Start with MCP

Follow the [MCP quickstart](docs/mcp/quickstart.md) to create a private token file
and connect over HTTP. HTTP is disabled by default, so a fresh clone needs no
MCP credential for REST. The local stdio example runs immediately:

```bash
uv run python examples/mcp_client.py stdio
```

Both transports expose `get_health_status` and the JSON resource `app://info`.
The [MCP documentation](docs/mcp/README.md) covers SDK research, capability
extension, configuration and remote deployment. Coding agents also read the
[MCP guidelines](.agents/mcp-guidelines.md). The shared bearer token is for
team-controlled internal clients; external-client OAuth is a separate integration.

## Configuration and deployment

[`app/core/config.py`](app/core/config.py) defines defaults and supported environment variables. `ENV_FILE` selects an environment file and defaults to `.env.dev`. [`.env.example`](.env.example), [`.env.dev`](.env.dev), [`.env.staging`](.env.staging) and [`.env.production`](.env.production) are versioned templates with all supported setting names, defaults and explicit placeholders. The three Compose files select `.env.dev`, `.env.staging`, and `.env.production` respectively.

Production mode rejects `CORS_ALLOW_ORIGINS=*`. Set explicit trusted origins, review `DOCS_ENABLED`, and disable `SERVER_RELOAD` for deployments. The production Compose command runs Uvicorn without reload. Store secrets through the deployment environment; tracked example or environment files must not contain real credentials.

Agree actual origins, MCP Host values and credentials with DevOps before
deployment. The MCP token placeholder cannot authenticate enabled HTTP.
Use deployment secret injection or ignored `.env.*.local` files for real
credentials; select a private file with `ENV_FILE` for local runs. Empty
Origin/exposed-header lists are intentional defaults rather than missing values.

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

The default lane runs unit and component tests, including local MCP stdio subprocesses, without optional infrastructure. `integration`, `acceptance`, and `live` are separate lanes for projects that add their fixtures and dependencies; live provider tests require explicit authorization. `scripts/test-report.sh default` writes local coverage artifacts under `reports/tests/` without a coverage threshold. See the [testing guide](.agents/testing-guidelines.md) for lane rules.

Coding agents start with [AGENTS.md](AGENTS.md); Claude Code uses [CLAUDE.md](CLAUDE.md) as a pointer to the same rules. The [contributor guide](.agents/README.md) maps conventions to each kind of task. For diagrams, use the [component library](assets/diagrams/README.md) and follow the [diagram guide](.agents/diagram-guidelines.md) for the editable source, screenshot, reading guide, and references.
