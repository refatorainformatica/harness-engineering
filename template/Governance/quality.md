# Governance — Quality

## Baseline rules

- No **new** lint/analyze issues in the touched files (unless explicitly agreed).
- **Every implementation ships unit tests** (new and changed behavior) — no exceptions for "small" changes; AC-G\* only for behavior that is not unit-testable, with a stub and a reason.
- Do not expand scope to "improve quality" outside the acceptance.
- Acceptance = tests: **AC-T\*** green, **or** a justified **AC-G\*** + stub in the feature folder.

## Tests

- New tests **always** in the feature folder (`Knowledge/standards.md`).
- Never mock domain Entities / Value Objects — use real instances.
- Mock only the edges (repositories, HTTP, clock, filesystem, brokers).
- Naming, mandatory scenarios, quality and idempotency: [standards.md](../Knowledge/standards.md#tests).

## Cross-cutting rules (source: `Knowledge/standards.md`)

| Rule | Section |
|------|---------|
| Code preservation | [standards.md#code-preservation-mandatory](../Knowledge/standards.md#code-preservation-mandatory) |
| Code documentation + delivery in `docs/` | [standards.md#code-documentation](../Knowledge/standards.md#code-documentation) |
| Structured logging | [standards.md#logging](../Knowledge/standards.md#logging) |
| Structure / lean orchestrators | [standards.md#implementation-structure](../Knowledge/standards.md#implementation-structure) |

Automated check: `harness.check` ([Tools/validation.md](../Tools/validation.md)).

## Suggested gates (adjust to the company)

- [ ] Green build within scope
- [ ] Unit tests for every new/changed behavior; feature/regression tests green (AC-T\* or AC-G\* + stub)
- [ ] Coverage ≥ 80% line on every testable artifact (`harness.check --coverage`)
- [ ] Lint/analyze on touched files
- [ ] Attributes preserved; logic unchanged outside the acceptance
- [ ] Code docs + `docs/` updated
- [ ] Security baseline S1–S12 + logging verification L1–L8 with evidence
- [ ] `harness.check` without errors + final validation of all rules recorded in the LOG
- [ ] Human review before merge (MATRIX)

## Coverage (mandatory)

- **Minimum 80% line coverage on every testable artifact** (assembly/project, module, package, library, app). This is a floor: a company or project may raise it, never lower it.
- Testable artifact = anything containing logic. Exclusions only for generated code, DI/bootstrap wiring (`Program`/`main`), migrations, pure DTOs and configuration — listed explicitly in the coverage tool config, never excluded to hit the number.
- Measured with the stack's coverage tool (see the active stack pack) and checked with `harness.check --coverage <report>`.
- Meaningful coverage, not inflation: assertions on behavior; no tests without assertions.
- Priority: Domain → Application → Infrastructure → API (only if it has business rules).

## Project

- Minimum coverage:
- Mandatory tools:
