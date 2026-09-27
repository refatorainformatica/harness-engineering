# Sandbox

Isolar mudanças quando há WIP alheio ou risco.

```bash
SANDBOX_DIR="../{{PROJECT}}-harness-sandbox"
git worktree add -b "sandbox/<slug>" "$SANDBOX_DIR" HEAD
cd "$SANDBOX_DIR"
```

| Regra | Detalhe |
|-------|---------|
| Path | `../{{PROJECT}}-harness-sandbox` ou `Runtime/sandbox/worktrees/<slug>` (gitignored) |
| Secrets | Não copiar `.env` / credentials |
| Merge de volta | **ask** |

Não precisa de sandbox se working tree limpa e branch dedicada.
