# Git Conventions

## Branch naming

Use a short, purpose-based branch name:

- `feat/<short-description>`
- `fix/<short-description>`
- `refactor/<short-description>`
- `docs/<short-description>`
- `chore/<short-description>`

## Commit messages

Use Conventional Commits in the form `<type>(<scope>): <summary>`.

Common types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `build`.

## Commit discipline

- Make each commit a coherent, reviewable change.
- Do not include caches, bytecode, generated artifacts, or unrelated work.
- Split changes spanning independent concerns into separate commits.
- Review `git diff` and `git status` before staging.
- Run GitNexus `detect_changes` before committing code changes.
- Do not discard someone else's work with `git reset --hard` or `git checkout --`.
- Rewrite history only when the repository owner explicitly requests it.
