# Diagram assets

This directory contains reusable visual assets; it is separate from project
documentation so diagrams can reference a stable, source-controlled palette.

## Use the component library

Open [`component-library.drawio`](component-library.drawio) in Draw.io. Each
card and block is a grouped component: copy it into the target diagram, then
rename the role text to match the current design. The library contains 487
source SVGs across 17 pages: 219 technology logos, 216 Fluent regular icons,
52 Fluent color icons, and a page of six composable blocks.

| Technology page | Logos | Examples |
| --- | ---: | --- |
| AI and ML technologies | 36 | DeepSeek, Mistral AI, LangGraph, PyTorch, TensorFlow, Hugging Face, MLflow |
| Backend and API technologies | 39 | FastAPI, Django, Flask, Pydantic, Go, NestJS, GraphQL, Celery |
| Database and storage technologies | 43 | PostgreSQL, DuckDB, Qdrant, Milvus, Neo4j, MongoDB, ClickHouse, MinIO |
| Network and security technologies | 29 | NGINX, Kong, Envoy, Cisco, Wireshark, WireGuard, Tailscale, Vault |
| Platform and delivery technologies | 47 | Kubernetes, Docker, Helm, Terraform, OpenTofu, Argo, GitHub Actions |
| Observability and data pipelines | 25 | OpenTelemetry, Prometheus, Grafana, Jaeger, Kafka, RabbitMQ, Airflow, Spark |

| Fluent component pages | Regular | Color | Examples |
| --- | ---: | ---: | --- |
| AI and retrieval | 32 | 10 | Bot, Brain Circuit, Search Sparkle, Scan Text, Person Feedback |
| Backend and workflow | 53 | 14 | Code, Plug Connected, Flowchart, Pipeline, Timer, Document Queue |
| Data and document | 49 | 10 | Database Stack, Storage, Table Link, Data Funnel, Document PDF |
| Network and security | 35 | 10 | Router, Network Adapter, Globe Shield, Lock, Key, Certificate |
| Compute and operations | 47 | 8 | Server, Cloud Database, Cube Tree, Developer Board, Gauge, Alert |

Each Fluent family has a regular SVG; color variants are included only where
that upstream family provides one. Color variants have their own pages and
use the `-color.svg` filename suffix. Pick one visual style for a diagram.

The composable blocks cover RAG, a tool-using agent, an asynchronous worker,
public ingress, observability, and delivery. They are illustrative starting
points; rename components and connectors to match the actual architecture.

The embedded images make the Draw.io file portable. The source SVGs are also
available for direct import:

- `icons/simple-icons/`: technology logos.
- `icons/fluent/`: product-neutral component icons.

[`catalog.json`](catalog.json) indexes every SVG by title, category, variant,
local path, upstream URL, pinned revision, and SHA-256 checksum. Search it
when selecting assets; it also records upstream brand-license and guideline
metadata when Simple Icons provides it.

Original upstream license texts are retained in `licenses/`. Source SVGs are
unmodified, including the original fills and gradients of Fluent color icons.

Create project-specific diagrams under `docs/diagrams/`; agent behavior and
diagram rules are defined in
[`.agents/diagram-guidelines.md`](../../.agents/diagram-guidelines.md).

Do not use a logo to claim a dependency, integration, certification, or
deployment that the project does not have. Use the semantic component instead.

See [third-party notices](THIRD_PARTY_NOTICES.md) before redistributing or
changing the imported assets.
