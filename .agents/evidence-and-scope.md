# Evidence and Scope Control

Apply this guide to code exploration, implementation, refactoring, and review.

## Evidence first

Classify material conclusions as one of the following:

- **Fact**: verified from the user request, current source, schema, test, configuration, or command output.
- **Assumption**: plausible but unverified; state it explicitly and verify it when cheap.
- **Decision**: a chosen implementation approach, supported by facts and any remaining assumptions.

When sources disagree, use this priority order: explicit user request, current public contract and tests, current source, architecture decisions, documentation, then prior conversation or memory. Do not present an assumption as a fact.

## Scope budget

- Every changed file or behavior must map directly to a user requirement, accepted plan item, regression, or verification requirement.
- Do not add a dependency, abstraction, package, workflow state, prompt fragment, tool, or retrieval layer without a concrete consumer and acceptance case.
- Record adjacent cleanup or possible enhancements as follow-up work instead of silently expanding the active change.
- Keep small tasks to one cohesive concern. If scope must expand, state the reason and recheck the affected contract and impact.

## Stop conditions

Stop and ask for direction when a required source of truth cannot be read, a material contract is ambiguous, a needed action requires new authority, or two high-priority sources conflict. If GitNexus is unavailable, use static source inspection where sufficient and report the reduced confidence; never invent graph findings.

## Evidence-bound handoff

Report results using only claims supported by evidence. Distinguish targeted checks from the default suite, full integration suite, and checks that were not run. Use this compact format when relevant:

```text
Completed: <implemented behavior>
Evidence: <commands, tests, or inspected contract>
Limitation: <what was not verified or remains uncertain>
Deferred: <out-of-scope follow-up, if any>
```

Do not request or reveal private chain-of-thought. Provide concise conclusions, rationale, and evidence instead.
