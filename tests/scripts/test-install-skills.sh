#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_DIR="$(mktemp -d)"
trap 'rm -rf -- "$TEST_DIR"' EXIT
mkdir -p "$TEST_DIR/project/scripts" "$TEST_DIR/bin" "$TEST_DIR/caller"
cp "$ROOT_DIR/scripts/install-skills.sh" "$TEST_DIR/project/scripts/"
cp "$ROOT_DIR/skills-catalog.json" "$TEST_DIR/project/"
cp "$ROOT_DIR/tests/scripts/fixtures/bunx" "$TEST_DIR/bin/bunx"
chmod +x "$TEST_DIR/bin/bunx"
export PATH="$TEST_DIR/bin:$PATH"
export INSTALL_TEST_ROOT="$TEST_DIR/project"
cd "$TEST_DIR/caller"

expected="$(jq 'length' "$ROOT_DIR/skills-catalog.json")"
export INSTALL_TEST_FAIL_BUN=1
status=0
bash "$TEST_DIR/project/scripts/install-skills.sh" > "$TEST_DIR/output" 2>&1 || status=$?
[[ "$status" == 1 ]]
[[ "$(wc -l < "$TEST_DIR/project/calls.tsv")" == "$expected" ]]
rg -q 'Failed skill: bun' "$TEST_DIR/output"
rg -q $'^bun\thttps://bun.sh/docs$' "$TEST_DIR/project/calls.tsv"
rg -q $'fastapi-templates\twshobson/agents' "$TEST_DIR/project/calls.tsv"
cmp "$ROOT_DIR/skills-catalog.json" "$TEST_DIR/project/skills-catalog.json"

export INSTALL_TEST_FAIL_BUN=0
bash "$TEST_DIR/project/scripts/install-skills.sh" > "$TEST_DIR/output" 2>&1
[[ "$(wc -l < "$TEST_DIR/project/calls.tsv")" == "$((expected * 2))" ]]
rg -q "Installed: $expected; failed: 0" "$TEST_DIR/output"
cmp "$ROOT_DIR/skills-catalog.json" "$TEST_DIR/project/skills-catalog.json"

status=0
bash "$TEST_DIR/project/scripts/install-skills.sh" "$TEST_DIR/project/skills-lock.json" > "$TEST_DIR/output" 2>&1 || status=$?
[[ "$status" == 1 ]]
rg -q 'reserved for CLI output' "$TEST_DIR/output"
[[ "$(wc -l < "$TEST_DIR/project/calls.tsv")" == "$((expected * 2))" ]]
printf 'Installer regression checks passed (%s skills per run).\n' "$expected"
