# Tools — Git

| ID | Command / action | Notes |
|----|------------------|-------|
| `git.status` | `git status`, `branch --show-current` | auto |
| `git.diff` | `git diff`, `git log` | auto (read) |
| `git.add` | `git add <paths>` | auto within scope |
| `git.commit` | `git commit` | **ask** |
| `git.push` | `git push` | **ask** |
| `git.stash` | stash / pop | **ask** if discarding |
| `git.checkout` | switch / branch -b | **ask** if leaving the branch |
| `git.destructive` | reset --hard, clean -fd, push --force | **deny** |
| `harness.sandbox.init` | git worktree sandbox | **ask** (see `Runtime/sandbox/readme.md`) |

## Forbidden

- Changing `git config`
- Committing secrets
- `--no-verify`
