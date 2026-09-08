# AGENTS — Entrypoint do AI Engineering Harness

Obrigatório para **qualquer** agente (Cursor, Copilot, Claude Code, Windsurf, Continue, Aider, JetBrains AI, Codex, etc.).

## Protocolo de toda tarefa

1. **Run** — criar/continuar `.ai-harness/Runtime/state/runs/<run-id>/` ([Runtime/RUN.md](./Runtime/RUN.md)).
2. **Workflow** — escolher em [Workflows/](./Workflows/): `feature` | `bug` | `refactoring` | `migration`.
3. **Knowledge** — ler o que for relevante em [Knowledge/](./Knowledge/) (Architecture, Domain, Standards, ADR).
4. **Specification** — ler `Specification/features/<id>/` (requirements, use-cases, acceptance).
5. **Governance** — aplicar [Governance/](./Governance/) + [permissions](./Governance/permissions.md).
6. **Agent role** — assumir o papel adequado em [Agents/](./Agents/) (pode haver handoff na mesma run).
7. **Tools** — só IDs em [Tools/](./Tools/) com nível `auto` | `ask` | `deny`.
8. **Loop** — [Runtime/LOOP.md](./Runtime/LOOP.md) até `DONE` | `BLOCKED` | `FAILED`.
9. **Sandbox** — se WIP alheio ou risco: [Runtime/sandbox/README.md](./Runtime/sandbox/README.md).

## Handoff de papéis (na mesma run)

| Situação | Papel |
|----------|-------|
| Decisão de desenho / ADR / limites | [Architect](./Agents/architect.md) |
| Implementação no escopo da spec | [Developer](./Agents/developer.md) |
| Diff vs Knowledge + Governance | [Reviewer](./Agents/reviewer.md) |
| Estratégia e evidência de testes | [Tester](./Agents/tester.md) |

Registre handoffs no `LOG.md` da run.

## Ao concluir

- STATUS → `DONE`
- Acceptance atualizado se o comportamento mudou
- ADR novo se houve decisão arquitetural
- Resumir arquivos + como validar

## Mapa rápido

| Precisa | Path |
|---------|------|
| Loop / Run | `Runtime/` |
| Specs | `Specification/features/` |
| Papéis | `Agents/` |
| Processos | `Workflows/` |
| Catálogo de ações | `Tools/` |
| Políticas | `Governance/` |
| Verdade do sistema | `Knowledge/` |
