# Testing Guidelines

## Taxonomy and selection

Every test belongs to exactly one primary lane: `unit`, `component`, `integration`, `acceptance`, or `live`. The test collection hook infers the lane from the test path when no explicit marker is present.

- `default` runs local unit and component tests without infrastructure or credentials.
- `integration` requires declared local infrastructure and isolated fixtures.
- `acceptance` uses a versioned representative dataset.
- `live` requires explicit authorization and must never be selected by default or CI.

Use `scripts/test-suite.sh <lane>` rather than duplicating marker expressions in documentation or CI.

## Test design

- Tests must be deterministic and independent of environment variables, network services, wall-clock timing, and ordering unless the lane explicitly owns that dependency.
- Prefer fixtures with explicit scope and cleanup. Do not share mutable state between tests.
- Keep API tests focused on contracts and service tests focused on behavior.
- A regression test must fail before the fix and pass after it; do not weaken assertions to make a suite green.

## Coverage and reporting

`scripts/test-report.sh default` produces local coverage artifacts without a coverage gate. Coverage indicates exercised code, not correctness; review assertions and selected lanes as well as the percentage.
