# GitNexus Guidelines

GitNexus provides dependency and control/data-flow analysis for this template.
The repository configuration keeps the index focused on this checkout.

## Index lifecycle

- Refresh only with `scripts/gitnexus-refresh.sh`.
- Keep the registry alias as `fastapi_template` and PDG analysis enabled.
- Before graph-assisted exploration, use `node .gitnexus/run.cjs status`. Refresh when it is stale.
- Do not depend on generated agent instructions or local GitNexus skills; `AGENTS.md` remains the source of repository routing.

## Before changing code

1. Confirm the index is current.
2. Query an unfamiliar behavior before deciding its edit boundary.
3. Run upstream impact analysis before changing a function, class, or method.
4. Report HIGH or CRITICAL findings before editing.

## Before committing

1. Run `detect_changes` and reconcile every affected flow with the intended scope.
2. Refresh the index after the commit and confirm `node .gitnexus/run.cjs status` is current.

## Local configuration

`.gitnexusrc` pins the alias and enables PDG analysis. The refresh script is the only supported way to generate local `.gitnexus/` state.
