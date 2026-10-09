# Evidence and scope control

Use this guide whenever an agent explores, changes, reviews, or describes the repository. It prevents a plausible guess from becoming a project rule.

## Classify claims

- **Fact:** supported by the current user request, source, configuration, schema, test, or command output. Name the supporting file or observed result when the claim matters.
- **Assumption:** plausible but unverified. Mark it and verify it when cheap; do not turn it into a requirement or shipped capability.
- **Decision:** the selected way to satisfy the task. State the ownership boundary and any material tradeoff.

When sources disagree, use this order: explicit user instruction; current public contract and tests; current source and configuration; accepted architecture decision; current documentation; earlier conversation or memory. Investigate apparent disagreement before changing a contract. A failing test may expose a stale test or a regression; inspect both before choosing.

Examples of evidence boundaries in this template:

| Observation | Supported conclusion | Conclusion that still needs evidence |
| --- | --- | --- |
| `get_readiness_status()` returns `ok` | Baseline readiness is green without external checks | A future database or provider is healthy |
| `app/agents/__init__.py` exists | The extension package is importable | An AI agent or provider integration exists |
| `scripts/verify.sh` passes | Configured Ruff, Ty, and default local tests passed | Integration, live-provider, or production behavior passed |
| GitNexus returns no affected symbols | No affected symbols were reported by that index/query | No caller, contract, or undocumented dependency exists |

## Set a change boundary

1. Write down the requested outcome and its observable acceptance condition.
2. Identify the responsible layer and every affected caller, public schema, fixture, configuration, document, and verification command. Search for references before changing a shared symbol.
3. Add or change only files that serve that outcome, a necessary regression fix, or its verification. Preserve existing work outside the boundary, including untracked files and environment files.
4. If the boundary expands, explain which newly discovered contract requires it. Record unrelated cleanup as a follow-up instead of slipping it into the change.

Do not introduce a dependency, service, abstraction, workflow state, prompt fragment, or config option without a current consumer and acceptance case. Empty template packages are not evidence that an implementation is needed.

For a public API change, the boundary normally includes route, schema, service, API tests, and README or reference docs that describe the contract. For a new setting, inspect `app/core/config.py`, `.env.example`, selected Compose files, tests that isolate environment variables, and documentation. Add only the parts the actual change affects.

## Handle uncertainty and blocked work

Do not infer a feature from a package name, diagram, old README, or green lint result. Say what you inspected and what it proves. If a required source cannot be read, a public or security contract is ambiguous, or an action needs new authority, stop the dependent action and request the missing input. Continue independent work when possible.

If a tool is unavailable, use other evidence only where it supports the same conclusion and report the limitation. A GitNexus miss does not prove there are no callers; no collected integration tests does not prove integration behavior works.

## Handoff

Report the changed behavior or artifact, the relevant files and checks, and any material unverified boundary. Distinguish a focused check, `scripts/verify.sh`, infrastructure test lane, and manual inspection. Do not label work production ready without the corresponding system and operational evidence. Never reveal private reasoning or credentials; give concise, inspectable rationale.
