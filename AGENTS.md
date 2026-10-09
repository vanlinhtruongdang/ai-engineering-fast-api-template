# Repository instructions for coding agents

These instructions apply to every file in this repository. `AGENTS.md` is the entry point; `.agents/` holds the detailed rules. Read the relevant guides before making a decision, including for documentation-only changes.

## Start every task

1. Read [`.agents/README.md`](.agents/README.md) and [`.agents/gitnexus-guidelines.md`](.agents/gitnexus-guidelines.md) completely.
2. Run `git status --short`. Record existing staged, unstaged, and untracked work; preserve anything outside the active task.
3. Read the task-specific guides below. Inspect the current source, configuration, contracts, tests, and scripts that support the task before editing.
4. State the change boundary and the smallest useful verification. If evidence conflicts, follow [`.agents/evidence-and-scope.md`](.agents/evidence-and-scope.md).

| Task | Read |
| --- | --- |
| Any repository work | [Contributor guide](.agents/README.md), [GitNexus rules](.agents/gitnexus-guidelines.md), [evidence and scope](.agents/evidence-and-scope.md), [working checklist](.agents/workflow-checklist.md) |
| Python, FastAPI, API contracts, configuration | [Python and FastAPI conventions](.agents/python-fastapi-conventions.md) |
| Tests, fixtures, coverage, test reports | [Testing guidelines](.agents/testing-guidelines.md) |
| Measured performance work | [Performance guidelines](.agents/performance-guidelines.md) |
| Agents, prompts, tools, AI workflows | [Agent design principles](.agents/agent-design-principles.md) |
| Documentation, reviews, natural-language deliverables | [Evidence-led writing harness](.agents/ai-writing-harness.md) |
| Diagrams and Draw.io assets | [Diagram guidelines](.agents/diagram-guidelines.md) |
| Branches, staging, commits, or other Git operations | [Git conventions](.agents/git-conventions.md) |

## Working rules

- Locate the responsible layer before changing behavior. Keep HTTP validation and response contracts in `app/api/` and `app/schemas/`, business behavior in `app/services/`, and runtime settings and infrastructure in `app/core/`. Empty extension packages are invitations to add a concrete capability, not prebuilt implementations.
- Check all callers and affected contracts before editing a function, class, or method. Refresh GitNexus with `scripts/gitnexus-refresh.sh` when its index is stale, then run upstream impact analysis as described in the GitNexus guide. Never invoke plain `gitnexus analyze`.
- Match verification to the change. `scripts/verify.sh` is the default Python quality gate; focused checks and test lanes are described in `.agents/`. Report what was actually run and any remaining limitation.
- Before a commit, run `gitnexus detect_changes --repo fastapi_template --scope staged`; after a commit, refresh the index. Stage only task files and use the Git conventions guide for commit boundaries.
- Never expose credentials or copy them into source, logs, fixtures, or documentation. Do not discard, format, stage, or rewrite unrelated work. Resolve exact targets before deleting or overwriting files.
- Ask for explicit authorization before pushing, opening an external pull request, releasing, applying a destructive migration, or changing an external system. Local reading, editing, verification, and review do not require separate approval.

If GitNexus or another required tool is unavailable, use source and test evidence where sufficient, say which check could not run, and do not claim a graph result you did not obtain.
