# Adapters de IDE e agentes

O harness (`.ai-harness/`) é a fonte da verdade. Adapters são ponteiros curtos.

| ID | Ferramenta | Destino |
|----|------------|---------|
| `cursor` | Cursor | `.cursor/rules/*.mdc` (sdd + OSS + domínio rico) |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` |
| `claude` | Claude Code | `CLAUDE.md` |
| `windsurf` | Windsurf | `.windsurfrules` |
| `continue` | Continue | `.continue/rules/harness-sdd.md` |
| `aider` | Aider | `CONVENTIONS.md` |
| `agents-md` | Codex / genéricos | `AGENTS.md` |
| `jetbrains` | JetBrains AI | `.aiassistant/rules/harness.md` |
| `all` / `none` | todos / nenhum | — |

```bash
./scripts/init-harness.sh ~/proj/api AcmeApi --adapters=cursor,copilot,claude
./scripts/init-harness.sh ~/proj/cli AcmeCli --adapters=aider,agents-md
./scripts/init-harness.sh ~/proj/demo Demo --adapters=all
```

Todos apontam para `.ai-harness/AGENTS.md` e os sete pilares.
