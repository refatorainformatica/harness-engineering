# CLAUDE.md — AI Engineering Harness

Canonical entrypoint: `.ai-harness/AGENTS.md`.

## Protocol

1. Run: `.ai-harness/Runtime/RUN.md` + `LOOP.md`
2. Workflow: `.ai-harness/Workflows/`
3. Knowledge + Specification for the feature
4. Agent role: Architect | Developer | Reviewer | Tester
5. Tools + `Governance/permissions.md`

Continue `auto` steps; stop only on `ask` or ambiguity. Update specs/ADR when things change.

Code and tests are always organized by feature. See `.ai-harness/Knowledge/Standards.md`.

OSS-first (`Governance/cost.md`). Acceptance = AC-T* or AC-G* + stub. No commit/push/secrets off the permission matrix.
