# Tools — Git

| ID | Comando / ação | Notas |
|----|----------------|-------|
| `git.status` | `git status`, `branch --show-current` | auto |
| `git.diff` | `git diff`, `git log` | auto (leitura) |
| `git.add` | `git add <paths>` | auto no escopo |
| `git.commit` | `git commit` | **ask** |
| `git.push` | `git push` | **ask** |
| `git.stash` | stash / pop | **ask** se descartar |
| `git.checkout` | switch / branch -b | **ask** se sair da branch |
| `git.destructive` | reset --hard, clean -fd, push --force | **deny** |
| `harness.sandbox.init` | git worktree sandbox | conforme Runtime/sandbox |

## Proibido

- Alterar `git config`
- Commitar secrets
- `--no-verify`
