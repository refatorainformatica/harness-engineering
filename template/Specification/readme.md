# Specification

O que o sistema deve **entregar**. Organizado por feature.

```text
Specification/
├── README.md
├── features/
│   ├── INDEX.md
│   └── <id>/
│       ├── requirements.md
│       ├── use-cases.md
│       └── acceptance.md
└── templates/
```

## Status de feature

| Status | Significado |
|--------|-------------|
| `planned` | Spec existe; código ausente ou mínimo |
| `wip` | Em branch ativa |
| `partial` | Fluxo incompleto |
| `stable` | Em uso na branch principal |

## Regras

1. Sem `acceptance.md` claro → não entrar em `ACT` (ficar em PLAN ou BLOCKED).
2. Mudança de comportamento → atualizar requirements/use-cases/acceptance na mesma run.
3. Use cases em Given/When/Then (ou equivalente BDD).
