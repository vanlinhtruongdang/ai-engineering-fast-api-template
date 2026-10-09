# GitNexus guidelines

GitNexus is a navigation and impact aid for code changes. Its index describes a particular checkout and commit; it does not replace source inspection, contract review, or tests. The repository alias is `fastapi_template`, and `.gitnexusrc` enables PDG analysis.

## Index lifecycle

1. Before relying on a graph result, run `node .gitnexus/run.cjs status`. Check the reported branch, indexed commit, current commit, and freshness.
2. If stale or absent, refresh with `scripts/gitnexus-refresh.sh`. That script is the only supported refresh entry point; it runs the configured index-only PDG analysis. Never run plain `gitnexus analyze` or generate replacement `AGENTS.md` or skills from GitNexus.
3. A relationship-affecting source or configuration edit after refresh makes graph findings stale for the next query, even when `HEAD` has not changed. Refresh before using the graph again.
4. Documentation-only work does not need a graph query. Do not claim current graph coverage when the status says stale.

The local `.gitnexus/` directory is ignored by Git. On a fresh checkout, the status helper may not exist yet; run the refresh script to create local state, then check status. A branch or commit mismatch is a stale index even when the graph database can still answer queries.

## Before changing a symbol

1. Identify the function, class, or method and search its callers, route entry points, and tests in the current checkout.
2. For an unfamiliar flow, query GitNexus to locate relevant relationships, then read the cited source. The graph is a lead, not the contract.
3. Run `gitnexus impact <symbol> --repo fastapi_template --direction upstream` before editing an existing symbol. Inspect affected callers and state any HIGH or CRITICAL finding before editing.
4. If the index cannot resolve the symbol, use direct source search and tests, describe the missing graph coverage, and avoid making claims about absent dependencies.

For a new file or documentation-only change there may be no existing symbol to query. Analyze the existing entry point or contract whose behavior the addition will extend when code behavior changes.

## Before and after a commit

- Review the staged diff and run `gitnexus detect_changes --repo fastapi_template --scope staged` before committing. Reconcile affected flows with the intended change; an empty result is not proof that documentation or behavior is correct.
- After committing, run `scripts/gitnexus-refresh.sh`, then confirm current status with `node .gitnexus/run.cjs status`.
- If GitNexus is unavailable, record the command and failure, use static source and test evidence where sufficient, and report reduced graph confidence. Do not invent a successful check or refresh by another method.

```bash
node .gitnexus/run.cjs status
scripts/gitnexus-refresh.sh
gitnexus impact <symbol> --repo fastapi_template --direction upstream
gitnexus detect_changes --repo fastapi_template --scope staged
```
