# Git conventions

Git history should let another contributor review one concern at a time. Repository changes begin with `git status --short`; existing staged, unstaged, and untracked work belongs to its owner unless the active task includes it.

## Branches and commits

- Use a short purpose-based branch name such as `feat/<topic>`, `fix/<topic>`, `refactor/<topic>`, `docs/<topic>`, or `chore/<topic>` when a branch is requested or needed to isolate a change. Honor an explicitly requested base branch; inspect ancestry and the worktree before switching.
- Use Conventional Commits: `<type>(<scope>): <summary>`. Common types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `build`. The scope should name the affected area, and the summary should describe the outcome.
- Keep a commit coherent and reviewable. Separate independent runtime, test, and documentation concerns when that improves review, but do not split a contract change so that intermediate commits are misleading or broken.

If a shared file contains another contributor's edits, use selective staging for only the task's hunks. If separation is unsafe, leave the file unstaged and explain the overlap before committing. A clean `git status` is not a reason to overwrite or absorb unrelated changes.

## Safe staging sequence

1. Review `git status --short` and the relevant working-tree diff. Identify task files and any pre-existing edits in shared files.
2. Stage only the intended paths or hunks. Do not stage `.env.*`, credentials, caches, bytecode, generated reports, or unrelated user work.
3. Inspect the staged diff and run `git diff --cached --check`.
4. Run `gitnexus detect_changes --repo fastapi_template --scope staged` before committing and reconcile its results with source and test evidence.
5. Commit with a focused Conventional Commit message. After commit, refresh GitNexus with `scripts/gitnexus-refresh.sh` and check its status.

Before claiming a branch is ready for review, confirm the current branch and commit range, and say whether it is local or published. A commit command succeeding does not imply a push or an open pull request. For documentation-only commits, GitNexus may report no symbol changes; still run the staged check required by `AGENTS.md` and verify the document itself.

Do not use `git reset --hard`, `git checkout --`, or history rewriting to remove someone else's work. Resolve the exact target and obtain explicit authorization before destructive Git operations. Do not push or open an external pull request without explicit authorization. A local branch and local commit do not imply permission to publish.
