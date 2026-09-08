# Agents — papéis

Papéis que o runtime assume. Workflows **orquestram** papéis; papéis **não** inventam o processo.

| Papel | Arquivo | Foco |
|-------|---------|------|
| Architect | [architect.md](./architect.md) | Desenho, ADR, limites, trade-offs |
| Developer | [developer.md](./developer.md) | Implementação no escopo da spec |
| Reviewer | [reviewer.md](./reviewer.md) | Diff vs Knowledge + Governance |
| Tester | [tester.md](./tester.md) | Estratégia e evidência de testes |

## Regras

1. Declare o papel ativo no `STATUS.md` / `LOG.md` da run.
2. Handoff explícito (ex.: Architect → Developer → Tester → Reviewer).
3. Em dúvida de escopo ou arquitetura → Architect ou BLOCKED, não “chutar”.
