# Sandbox

Isolate changes when there is someone else's WIP or risk.

```bash
SANDBOX_DIR="../{{PROJECT}}-harness-sandbox"
git worktree add -b "sandbox/<slug>" "$SANDBOX_DIR" HEAD
cd "$SANDBOX_DIR"
```

| Rule | Detail |
|------|--------|
| Path | `../{{PROJECT}}-harness-sandbox` or `Runtime/sandbox/worktrees/<slug>` (gitignored) |
| Secrets | Do not copy `.env` / credentials |
| Merge back | **ask** |

No sandbox needed if the working tree is clean and the branch is dedicated.
