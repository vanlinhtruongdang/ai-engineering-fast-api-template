#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PROFILE="${1:-default}"
if (( $# > 0 )); then
  shift
fi

case "$PROFILE" in
  default) MARK_EXPRESSION="not integration and not acceptance and not live and not slow" ;;
  all) MARK_EXPRESSION="unit or component or integration or acceptance or live" ;;
  *)
    echo "Usage: scripts/test-report.sh [default|all] [pytest args...]" >&2
    exit 2
    ;;
esac

REPORT_DIR="${REPORT_DIR:-reports/tests}"
mkdir -p "$REPORT_DIR"

exec uv run pytest \
  -m "$MARK_EXPRESSION" \
  --cov=app \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report="xml:$REPORT_DIR/coverage.xml" \
  --cov-report="json:$REPORT_DIR/coverage.json" \
  "$@"
