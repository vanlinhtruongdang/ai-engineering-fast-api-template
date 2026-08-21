# Internal Contributor Guide

This guide applies to developers and coding agents working in this FastAPI template.

## Goals

- Python code follows the repository's Ruff configuration.
- Static type checking uses Ty.
- HTTP APIs follow the FastAPI conventions documented here.
- Git history follows the shared Git conventions.
- Code changes receive GitNexus impact analysis before modification.

## Related guides

- [Python and FastAPI conventions](python-fastapi-conventions.md)
- [Git conventions](git-conventions.md)
- [Performance guidelines](performance-guidelines.md)
- [GitNexus guidelines](gitnexus-guidelines.md)
- [Agent design principles](agent-design-principles.md)
- [Working checklist](workflow-checklist.md)

## General principles

- Fix the root cause rather than applying a temporary patch.
- Keep changes small, explicit, and easy to review.
- Keep template extension packages available for discoverability; add implementation only when a project has a clear consumer or extension contract.
- Verify changes with the appropriate tools before finishing.
- Identify the source of truth—schema, service, configuration, documentation, or test—before changing a contract.
