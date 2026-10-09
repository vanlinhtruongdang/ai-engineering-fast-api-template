# Working checklist

Use this sequence for implementation and final handoff. Subject-specific rules live in the other `.agents/` guides; this checklist ties them to the task flow.

## Before editing

1. Follow the startup in `AGENTS.md`: read the guide map and GitNexus rules, run `git status --short`, then read the matching guides.
2. Define the requested outcome, acceptance condition, and affected files. Identify the source of truth for each public contract. Separate verified facts from assumptions and decisions.
3. Trace the current flow through entry point, callers, schemas, settings, tests, and deployment configuration as needed. Before editing an existing function, class, or method, refresh a stale GitNexus index and run upstream impact analysis.
4. Confirm that new infrastructure, dependencies, options, or extension code have a current consumer. Preserve out-of-scope work and secret-bearing files.

## While editing

- Change the layer that owns the invariant. Keep validation, authorization, errors, and data-loss protection intact.
- Update affected callers, tests, fixtures, configuration, documentation, and examples as one contract change. Avoid broad formatting or unrelated cleanup.
- For agent work, define input, output, failure, permission, and audit contracts before prompt text. For diagrams, deliver the editable source, reading guide, screenshot, and references together.
- If a new finding expands the task, explain the reason and recheck scope and impact before editing more files.

## Before finishing

1. Review the working-tree diff and `git status --short`. Check links, commands, examples, and claims in changed documentation against their sources.
2. Run the smallest checks that cover the actual change. For Python changes, `scripts/verify.sh` is the default gate; use the lane-specific scripts when the feature requires more. Documentation-only edits need link/claim review and `git diff --check`; do not describe them as runtime-tested.
3. Record any relevant benchmark with its workload if performance was changed. Recheck public docs when API or settings contracts changed.
4. Report the completed artifact or behavior, evidence, and material unverified boundary. Do not claim broader verification than was run.
5. If committing, stage only task files, inspect the staged diff, run `gitnexus detect_changes --repo fastapi_template --scope staged`, then refresh the index after the commit.

For container changes, preserve non-root runtime, avoid baking secrets into images, and review the affected development, staging, and production Compose files. Add an environment-specific value only when the runtime contract needs it.
