# Knowledge — {{PROJECT}}

**Stable** truth of the system. Changes via ADR or explicit decision — not with every feature.

| Document | Content |
|----------|---------|
| [architecture.md](./architecture.md) | Style, folders, DI, flows, harness ↔ code map |
| [domain.md](./domain.md) | Glossary, ubiquitous language, context boundaries |
| [standards.md](./standards.md) | Code, **feature-first organization**, rich domain, naming, docs |
| [ADR/](./ADR/) | Architecture Decision Records |

## Rules

1. Before implementing, the agent reads the Knowledge touched by the task.
2. Spec ↔ Knowledge conflict → `BLOCKED` (ask which source prevails).
3. Relevant architecture change → new ADR before or in the same run.
