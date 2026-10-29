# Specification

What the system must **deliver**. Organized by feature.

```text
Specification/
├── readme.md
├── features/
│   ├── index.md
│   └── <id>/
│       ├── requirements.md
│       ├── use-cases.md
│       └── acceptance.md
└── templates/
```

## Feature status

| Status | Meaning |
|--------|---------|
| `planned` | Spec exists; code absent or minimal |
| `wip` | On an active branch |
| `partial` | Incomplete flow |
| `stable` | In use on the main branch |

## Rules

1. No clear `acceptance.md` → do not enter `ACT` (stay in PLAN or BLOCKED).
2. Behavior change → update requirements/use-cases/acceptance in the same run.
3. Use cases in Given/When/Then (or equivalent BDD).
