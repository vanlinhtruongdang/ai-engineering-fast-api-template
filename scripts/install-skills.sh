#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname -- "$SCRIPT_DIR")"
CATALOG_FILE="${1:-$ROOT_DIR/skills-catalog.json}"

for tool in jq bunx; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$tool" >&2
    exit 1
  fi
done

# The CLI writes skills-lock.json in its working directory.
if [[ "$(basename -- "$CATALOG_FILE")" == "skills-lock.json" ]]; then
  printf 'Use a source catalog named differently from skills-lock.json (reserved for CLI output).\n' >&2
  exit 1
fi

if [[ ! -f "$CATALOG_FILE" ]]; then
  printf 'Skill catalog not found: %s\n' "$CATALOG_FILE" >&2
  exit 1
fi

if ! jq -e '
  type == "object" and length > 0 and
  all(to_entries[];
    (.key | type == "string" and length > 0) and
    (.value | type == "object") and
    (.value.source | type == "string" and length > 0) and
    (
      .value.sourceType == "github" or
      (.value.sourceType == "well-known" and
       (.value.sourceUrl | type == "string" and length > 0))
    )
  )
' "$CATALOG_FILE" >/dev/null; then
  printf 'Invalid skill catalog: expected a map of skills with supported source fields.\n' >&2
  exit 1
fi

entries="$(jq -r 'to_entries[] | [.key, (if .value.sourceType == "github" then .value.source else .value.sourceUrl end)] | @tsv' "$CATALOG_FILE")"
failed=()
installed=0
cd "$ROOT_DIR"

while IFS=$'\t' read -r skill package; do
  printf 'Installing %s from %s\n' "$skill" "$package"
  if bunx --yes skills add "$package" --skill "$skill" --agent codex claude-code --full-depth -y </dev/null; then
    installed=$((installed + 1))
  else
    failed+=("$skill")
    printf 'Failed to install %s; continuing.\n' "$skill" >&2
  fi
done <<< "$entries"

printf 'Installed: %s; failed: %s\n' "$installed" "${#failed[@]}"
if (( ${#failed[@]} > 0 )); then
  printf 'Failed skill: %s\n' "${failed[@]}" >&2
  exit 1
fi
