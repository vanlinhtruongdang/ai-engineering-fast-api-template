#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SUITE="${1:-default}"
if (( $# > 0 )); then
  shift
fi

case "$SUITE" in
  default) MARK_EXPRESSION="not integration and not acceptance and not live and not slow" ;;
  unit) MARK_EXPRESSION="unit and not slow" ;;
  component) MARK_EXPRESSION="component and not slow" ;;
  integration) MARK_EXPRESSION="integration and not slow" ;;
  acceptance) MARK_EXPRESSION="acceptance and not slow" ;;
  live) MARK_EXPRESSION="live and not slow" ;;
  slow) MARK_EXPRESSION="slow" ;;
  all) MARK_EXPRESSION="unit or component or integration or acceptance or live" ;;
  *)
    echo "Usage: scripts/test-suite.sh [default|unit|component|integration|acceptance|live|slow|all] [pytest args...]" >&2
    exit 2
    ;;
esac

exec uv run pytest -m "$MARK_EXPRESSION" "$@"
