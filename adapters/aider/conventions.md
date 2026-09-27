# CONVENTIONS — AI Engineering Harness (Aider)

Before editing code, read `.ai-harness/AGENTS.md`.

1. Create/continue a run in `.ai-harness/Runtime/state/runs/`.
2. Use the matching Workflow (feature/bug/refactoring/migration).
3. Follow Knowledge + Specification for the feature.
4. Act as Developer (or hand off via Agents docs).
5. Respect Tools + Governance/permissions.md.

Do not commit unless the user explicitly requested it.
Update acceptance criteria when behavior changes.
Organize code and tests always by feature (`.ai-harness/Knowledge/Standards.md`).
Prefer OSS; proprietary cloud only with ADR (`.ai-harness/Governance/cost.md`).
Acceptance = AC-T* or AC-G* + stub.
