# Adapters de IDE / Agentes

O harness em `.ai-harness/` é **agnóstico de ferramenta**. Cada adapter só aponta para `.ai-harness/AGENTS.md`.

| Ferramenta | Path no projeto | Fonte |
|------------|-----------------|-------|
| Cursor | `.cursor/rules/*.mdc` (harness-sdd, opensource-first, rich-domain) | [cursor/](./cursor/) |
| GitHub Copilot | `.github/copilot-instructions.md` | [github-copilot/](./github-copilot/) |
| Claude Code | `CLAUDE.md` | [claude-code/](./claude-code/) |
| Windsurf | `.windsurfrules` | [windsurf/](./windsurf/) |
| Continue | `.continue/rules/harness-sdd.md` | [continue/](./continue/) |
| Aider | `CONVENTIONS.md` | [aider/](./aider/) |
| Codex / genéricos | `AGENTS.md` | [agents-md/](./agents-md/) |
| JetBrains AI | `.aiassistant/rules/harness.md` | [jetbrains/](./jetbrains/) |

```bash
./scripts/init-harness.sh /proj MeuApp --adapters=cursor,copilot,claude
./scripts/init-harness.sh /proj MeuApp --adapters=all
./scripts/init-harness.sh /proj MeuApp --adapters=none
```

Detalhes: [../docs/ide-adapters.md](../docs/ide-adapters.md).
