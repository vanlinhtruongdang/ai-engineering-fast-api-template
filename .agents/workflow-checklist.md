# Working Checklist

## Before coding

- Read the exact files in scope and define the change boundary.
- Identify the source of truth: schema, service, configuration, documentation, or test.
- Confirm the relevant FastAPI conventions.
- Run GitNexus impact analysis before changing an existing function, class, or method.
- For agent work, define input, output, failure, and audit contracts first.

## While coding

- Keep changes small and use names that describe their purpose.
- Keep template placeholder packages intact; do not add implementation, aliases, or infrastructure without a consumer.
- Confirm a potential hot path is measured before optimizing it.
- Prefer deterministic validation and reusable contracts over prompt-only behavior.

## Before finishing

```bash
uv run ruff format --check
uv run ruff check
uv run ty check
uv run pytest
```

- Record performance measurements when relevant.
- Recheck public documentation after a public contract changes.
- Review `git status` and `git diff`.
- Run `gitnexus detect_changes` before commit, then refresh the index after commit.

## Containers

- Use official base images and non-root runtime users.
- Do not bake secrets or runtime environment files into images.
- Keep development and production Compose configurations explicit.
- Avoid `container_name` unless it is a concrete deployment requirement.
