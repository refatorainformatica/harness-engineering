# Agents — roles

Roles the runtime takes on. Workflows **orchestrate** roles; roles do **not** invent the process.

| Role | File | Focus |
|------|------|-------|
| Architect | [architect.md](./architect.md) | Design, ADR, boundaries, trade-offs, OSS-first |
| Developer | [developer.md](./developer.md) | Implementation within the spec scope |
| Reviewer | [reviewer.md](./reviewer.md) | Diff vs Knowledge + Governance |
| Tester | [tester.md](./tester.md) | Test strategy and evidence (AC-T\* / AC-G\*) |

Context for this repo (paths/commands): [project.md](./project.md).

## Rules

1. Declare the active role in the run's `status.md` / `log.md`.
2. Explicit handoff (e.g. Architect → Developer → Tester → Reviewer).
3. When in doubt about scope or architecture → Architect or BLOCKED; do not guess.
4. `fill`/`enrich` do **not** replace these roles — they only update `project.md`.
