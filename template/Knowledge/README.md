# Knowledge — {{PROJECT}}

Verdade **estável** do sistema. Muda com ADR ou decisão explícita — não a cada feature.

| Documento | Conteúdo |
|-----------|----------|
| [Architecture.md](./Architecture.md) | Estilo, pastas, DI, fluxos, mapa harness ↔ código |
| [Domain.md](./Domain.md) | Glossário, linguagem ubíqua, limites de contexto |
| [Standards.md](./Standards.md) | Padrões de código, naming, testing, docs |
| [ADR/](./ADR/) | Architecture Decision Records |

## Regras

1. Antes de implementar, o agente lê o Knowledge tocado pela tarefa.
2. Conflito Spec ↔ Knowledge → `BLOCKED` (pedir qual fonte prevalece).
3. Mudança de arquitetura relevante → novo ADR antes ou na mesma run.
