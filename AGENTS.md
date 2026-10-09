# Repository Instructions

These instructions apply to every file in this repository.

## Mandatory startup

Before analyzing, planning, editing, reviewing, or testing this repository:

1. Read `.agents/README.md` completely.
2. Read `.agents/gitnexus-guidelines.md` completely before exploring or changing code.
3. Run `git status --short` and preserve any pre-existing changes outside the task scope.
4. Read every additional guide that matches the task from the routing table below.

## Guidance routing

| Task | Required guide |
| --- | --- |
| Any repository work | `.agents/README.md` |
| Code exploration, impact analysis, implementation, refactoring, or review | `.agents/gitnexus-guidelines.md`, `.agents/evidence-and-scope.md` |
| Python or FastAPI changes | `.agents/python-fastapi-conventions.md` |
| Tests, fixtures, coverage, or test reports | `.agents/testing-guidelines.md` |
| Performance-sensitive changes | `.agents/performance-guidelines.md` |
| Agent, prompt, or workflow design | `.agents/agent-design-principles.md` |
| Documentation diagrams or Draw.io assets | `.agents/diagram-guidelines.md` |
| Git operations or commits | `.agents/git-conventions.md` |
| Implementation and final verification | `.agents/workflow-checklist.md` |

## GitNexus enforcement

- Treat `.agents/gitnexus-guidelines.md` as the canonical GitNexus rule set.
- Refresh the index only with `scripts/gitnexus-refresh.sh`; never run a plain `gitnexus analyze`.
- Run impact analysis before editing a function, class, or method.
- Run `gitnexus detect_changes --repo fastapi_template --scope staged` before committing and refresh the index after a commit.

## Authority and workspace safety

- Do not discard, stage, format, or rewrite changes outside the active task scope.
- Do not expose secrets or copy credentials into code, logs, test fixtures, or documentation.
- Ask for explicit authorization before pushing, opening external pull requests, releasing, applying destructive migrations, or changing external systems.
- Prefer reversible operations. Resolve exact targets before any deletion or overwrite.
