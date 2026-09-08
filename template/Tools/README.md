# Tools

Catálogo de ações que o agente pode acionar. Nível efetivo: [Governance/permissions.md](../Governance/permissions.md).

| Área | Arquivo |
|------|---------|
| Build | [build.md](./build.md) |
| Test | [test.md](./test.md) |
| Git | [git.md](./git.md) |
| Validation | [validation.md](./validation.md) |

## Convenções

- **ID** estável — use no LOG da run.
- Fora deste catálogo = **deny** ou **ask** até autorização explícita.
- Remova stacks não usadas; adicione a stack real do projeto.

## IDE / agentes

Adapters (Cursor, Copilot, Claude Code, …) **não** são tools de shell — são como o agente carrega este harness. Ver `docs/ide-adapters.md` no kit.
