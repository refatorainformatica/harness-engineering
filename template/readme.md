# AI Engineering Harness

Template operacional de engenharia com IA para qualquer empresa ou produto.

```text
.ai-harness/
├── Knowledge/        # Verdade estável do sistema
├── Specification/    # O que entregar (por feature)
├── Agents/           # Papéis (Architect, Developer, Reviewer, Tester)
├── Workflows/        # Feature, Bug, Refactoring, Migration
├── Tools/            # Build, Test, Git, Validation
├── Governance/       # Security, Quality, Architecture, Cost, Permissions
└── Runtime/          # Loop, runs, sandbox
```

## Entrypoint

Todo agente começa em [AGENTS.md](./AGENTS.md).

## Checklist de capacidade

| Pilar | Onde |
|-------|------|
| Knowledge | [Knowledge/](./Knowledge/) |
| Specification | [Specification/](./Specification/) |
| Agents | [Agents/](./Agents/) |
| Workflows | [Workflows/](./Workflows/) |
| Tools | [Tools/](./Tools/) |
| Governance | [Governance/](./Governance/) |
| Runtime | [Runtime/](./Runtime/) |

## Princípios

- Spec antes de código — sem aceite claro → `BLOCKED`.
- IA produz, humano aprova o que a matriz marca como `ask`.
- Knowledge e Governance prevalecem sobre preferência do agente.
- Workflow escolhe o papel; o papel não inventa o processo.
