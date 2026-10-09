# Contributor guide

This directory is the repository's coding and writing harness. It gives an agent enough context to change the FastAPI foundation without guessing which layer owns a contract or which verification is meaningful. [AGENTS.md](../AGENTS.md) is the mandatory entry point and routing table; the guides below are the detailed source of truth for their subjects.

## What this template currently contains

- `app/main.py` exposes the application and local server entry point; `app/api/app.py` creates the app, installs request ID and CORS middleware, owns lifespan, and mounts the API router.
- `app/api/v1/` defines versioned HTTP routes. `app/schemas/` defines response contracts. `app/services/` owns the health behavior. `app/core/` owns settings, logging, and request context.
- Root `/health` and `/ready` are probe endpoints; `/api/v1/health`, `/api/v1/health/ready`, and `/api/v1/` are versioned routes. The baseline readiness response is `ok` because no mandatory external dependency is configured.
- `app/agents/`, `app/pipelines/`, `app/db/`, `app/models/`, `app/repositories/`, `app/common/`, and `app/utils/` are empty extension packages. Their names do not promise a database, agent runtime, model provider, or workflow engine.
- `pyproject.toml`, `scripts/verify.sh`, `scripts/test-suite.sh`, and `.github/workflows/ci.yml` define the actual quality gates. `uv.lock` pins the current Python dependency resolution.

Read [the architecture guide](../docs/fastapi-template-architecture.md) for the application boundary. Confirm behavior in source and tests before describing it as a guarantee.

## Guide map

| Guide | Owns |
| --- | --- |
| [Evidence and scope](evidence-and-scope.md) | Source priority, fact versus assumption, change boundary, handoff evidence |
| [Python and FastAPI](python-fastapi-conventions.md) | Module ownership, request flow, contracts, settings, async and logging rules |
| [Testing](testing-guidelines.md) | Test taxonomy, fixtures, deterministic checks, coverage reports |
| [Performance](performance-guidelines.md) | Measurements and performance-sensitive changes |
| [Agent design](agent-design-principles.md) | AI agent, prompt, tool, and workflow contracts when a project adds them |
| [GitNexus](gitnexus-guidelines.md) | Index lifecycle, impact queries, staged change review |
| [Git conventions](git-conventions.md) | Branches, staging, commits, preserving work |
| [Working checklist](workflow-checklist.md) | Task sequence and verification handoff |
| [Evidence-led writing](ai-writing-harness.md) | Claims, structure, citations, and review of authored text |
| [Diagrams](diagram-guidelines.md) | Draw.io source, reading guide, screenshots, references |

## How to use the rules

1. Identify the reader or caller, the behavior or artifact being changed, and its source of truth. A user request and current public contract take priority over assumptions and old prose.
2. Read only the guides matched by `AGENTS.md`, then inspect the concrete implementation. When two guides cover the same action, use the subject guide for detail and the working checklist for sequence.
3. Keep one owner for each rule. Update a guide when its rule changes; keep `AGENTS.md` and this index focused on routing. Do not copy an entire guide into agent-specific entry files.
4. Treat template guidance as a baseline for a new project. When a real service adds a database, model provider, agent, or frontend, update its contracts, guides, and checks to describe the actual system.

Do not treat a green lint run, an empty graph result, or polished prose as proof of runtime behavior. Report the evidence and its boundary.
