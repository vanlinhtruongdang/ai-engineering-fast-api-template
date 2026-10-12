# Testing guidelines

The test system has one primary taxonomy marker per test. `tests/pytest_contract.py` assigns a marker from the path unless a test declares one explicitly, and rejects multiple explicit taxonomy markers. `slow` is a supplemental marker, not a primary lane.

## Choose a lane

| Lane | Intended boundary | How to run |
| --- | --- | --- |
| `unit` | Pure logic without filesystem, database, or network boundaries | `scripts/test-suite.sh unit` |
| `component` | In-process API/service behavior and controlled local CLI/MCP subprocesses | `scripts/test-suite.sh component` |
| `integration` | Declared local infrastructure with isolated fixtures | `scripts/test-suite.sh integration` |
| `acceptance` | Versioned representative business dataset | `scripts/test-suite.sh acceptance` |
| `live` | External provider or credentials; run only with explicit authorization | `scripts/test-suite.sh live` |

`scripts/test-suite.sh default` selects unit and component tests while excluding `slow`. `scripts/test-suite.sh slow` selects tests marked slow. `scripts/test-suite.sh all` includes every primary lane, including slow tests, so inspect its dependencies before using it. The template currently has only local tests; a lane name alone does not supply infrastructure or credentials.

## Write a useful check

- Place tests near the matching application area. `tests/api/` exercises HTTP status, headers, validation, and response contracts; `tests/services/` exercises service behavior. `tests/mcp/` belongs to the component lane and checks discovery, typed results, HTTP security/lifecycle and real local stdio processes. Put pure functions under `tests/unit/` when that boundary exists.
- Prefer deterministic inputs and explicit assertions about externally visible behavior. A regression check should fail for the reported bug and pass for the fix. Avoid tests that simply duplicate implementation branches or snapshot unstable text.
- Keep tests independent of order, wall clock, ambient environment, and network unless their lane owns that dependency. Use fixtures with explicit scope and cleanup; do not share mutable state across tests.
- `tests/conftest.py` removes known settings environment variables and selects `os.devnull` as the environment file before importing the app, so developer secrets cannot change the suite. When adding settings, update this isolation boundary. Clear settings caches after environment overrides and restore them on fixture teardown. REST component tests use `httpx.ASGITransport`; SDK v2 MCP clients use `httpx2.ASGITransport`. Enter the parent app lifespan explicitly for MCP tests; ASGI transports do not start it.
- MCP tests cover both `auto` (`2026-07-28`) and `legacy` (`2025-11-25`) clients, bearer failures, Host/Origin rejection, allowed preflight, request IDs, settings validation, independent factories, shutdown and startup failure. Stdio subprocess tests use the locked interpreter, isolated settings and bounded cleanup; stdout must contain protocol only. They require local process/pipe support rather than external credentials.
- Mark exceptions to path inference explicitly, with exactly one primary marker. Do not weaken assertions or move tests into a different lane to make a failing default suite pass.

## Coverage and results

`scripts/test-report.sh default` writes branch coverage to `reports/tests/` and has no coverage threshold. Coverage is evidence of execution, not correctness. Report the selected lane, whether tests were actually collected, and the result. The CI quality job runs `scripts/verify.sh`, which includes the default lane; integration, acceptance, and live behavior need their own declared setup and run evidence.
