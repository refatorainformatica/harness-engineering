# Copilot — AI Engineering Harness

Follow `.ai-harness/AGENTS.md` for any code or spec change.

1. Create/continue a run under `.ai-harness/Runtime/state/runs/`.
2. Pick a Workflow: feature | bug | refactoring | migration.
3. Read Knowledge + `Specification/features/<id>/`.
4. Use the right Agent role (architect, developer, reviewer, tester).
5. Obey `Tools/` + `Governance/permissions.md` (`auto` / `ask` / `deny`).
6. Update acceptance/ADR when behavior or architecture changes.

Do not commit, push, or touch secrets unless explicitly allowed.
Ambiguous spec → BLOCKED and ask.
