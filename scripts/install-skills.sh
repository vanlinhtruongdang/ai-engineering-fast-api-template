#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname -- "$SCRIPT_DIR")"
LOCK_FILE="${1:-$ROOT_DIR/skills-lock.json}"

if [[ ! -f "$LOCK_FILE" ]]; then
  printf 'Skill lockfile not found: %s\n' "$LOCK_FILE" >&2
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
' "$LOCK_FILE" >/dev/null; then
  printf 'Invalid skill lockfile: expected a map of skills with supported source fields.\n' >&2
  exit 1
fi

while IFS= read -r skill; do
  source_type="$(jq -r --arg skill "$skill" '.[$skill].sourceType' "$LOCK_FILE")"

  if [[ "$source_type" == "github" ]]; then
    source="$(jq -r --arg skill "$skill" '.[$skill].source' "$LOCK_FILE")"
    package="$source@$skill"
  else
    package="$(jq -r --arg skill "$skill" '.[$skill].sourceUrl' "$LOCK_FILE")"
  fi

  printf 'Installing %s from %s\n' "$skill" "$package"
  bunx --yes skills add "$package" -y
done < <(jq -r 'keys[]' "$LOCK_FILE")
