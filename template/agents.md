# AGENTS — AI Engineering Harness entrypoint

Mandatory for **any** AI agent or person changing this repository — regardless of tool, IDE or model.

## Protocol for every task

1. **Run** — create/continue `.ai-harness/Runtime/state/runs/<run-id>/` ([Runtime/run.md](./Runtime/run.md)).
2. **Workflow** — choose from [Workflows/](./Workflows/): `feature` | `bug` | `refactoring` | `migration` | `infra`.
3. **Knowledge** — read what is relevant in [Knowledge/](./Knowledge/) (architecture, domain, standards, ADR) + **only** the active stack pack (`Knowledge/stacks/`, see `Agents/project.md`). **Code and tests always by feature** (`standards.md`).
4. **Specification** — read `Specification/features/<id>/` (requirements, use-cases, acceptance). Acceptance = **AC-T\*** (test) or **AC-G\*** (gap + stub).
5. **Governance** — apply [Governance/](./Governance/) + [permissions](./Governance/permissions.md). **OSS first** (`cost.md`); secrets never.
6. **Agent role** — take the appropriate role in [Agents/](./Agents/) (handoff within the same run is allowed).
7. **Tools** — only IDs in [Tools/](./Tools/) with level `auto` | `ask` | `deny`.
8. **Loop** — [Runtime/loop.md](./Runtime/loop.md) until `DONE` | `BLOCKED` | `FAILED`.
9. **Sandbox** — if there is someone else's WIP or risk: [Runtime/sandbox/readme.md](./Runtime/sandbox/readme.md).

## Role handoff (same run)

| Situation | Role |
|-----------|------|
| Design decision / ADR / boundaries | [Architect](./Agents/architect.md) |
| Implementation within the spec scope | [Developer](./Agents/developer.md) |
| Diff vs Knowledge + Governance | [Reviewer](./Agents/reviewer.md) |
| Test strategy and evidence | [Tester](./Agents/tester.md) |

Record handoffs in the run's `log.md`.

## Canonical rules

- Feature-first: code and tests in the feature folder; legacy code migrates when touched.
- OSS-first: open source → self-host → proprietary cloud only with an ADR.
- Do not expand scope to get unblocked; max. ~12 iterations/run.
- Commit/push/secrets only as the matrix allows (`ask` / `deny`).
- Rich domain always: business rules in entities/value objects; application code orchestrates and never sets internal state.
- **Business-rule changes require confirmation**: if a task would change an existing business rule (behavior, invariant, calculation, validation, acceptance), stop in `BLOCKED` and ask before editing — never destroy a working implementation without need.
- Code preservation, structure, logging, tests and documentation: single source in [Knowledge/standards.md](./Knowledge/standards.md) — no delivered docs, no DONE.
- Execution in `auto` steps: edit instead of only analyzing, batches, idempotency — [Runtime/loop.md](./Runtime/loop.md#execution-bias-within-the-matrix). Never overrides `ask`/`deny`.

## On completion

- Run `harness.check` ([Tools/validation.md](./Tools/validation.md)) and validate **all** applicable rules (Standards + Governance); record in the LOG
- STATUS → `DONE`
- Acceptance updated if the behavior changed (AC-T\* / AC-G\*)
- New ADR if there was an architectural or cloud vendor decision
- Summarize files + how to validate

## Quick map

| Need | Path |
|------|------|
| Loop / Run | `Runtime/` |
| Specs | `Specification/features/` |
| Roles | `Agents/` |
| Processes | `Workflows/` |
| Action catalog | `Tools/` |
| Stack packs (language, framework, DevOps/cloud) | `Knowledge/stacks/` |
| Policies | `Governance/` |
| System truth | `Knowledge/` |
