# Workflow — Migration

Structural change of data, platform, major dependency or cutover.

## Steps

1. Run + CONTEXT (source → target, downtime, rollback).
2. **Architect** mandatory: plan, ADR, Cost/Security impact.
3. Migration spec in `Specification/features/<id>/` (or a `migrate-*` feature).
4. Developer: migration scripts/code + dual-write/read if needed.
5. Tester: dry-run, data validation, tested rollback.
6. Reviewer + Governance (security, cost, architecture).
7. Production execution = always `ask` (plus the company's process).

## DoR

- [ ] ADR accepted (or human decision recorded)
- [ ] Rollback plan
- [ ] Window / owners defined

## DoD

- [ ] Dry-run evidenced
- [ ] Rollback tested or formally accepted
- [ ] Unit tests for every new/changed behavior; coverage ≥ 80% line on every testable artifact
- [ ] Security baseline S1–S12 verified (`Governance/security.md`) — evidence in the log
- [ ] Logging verification L1–L8 (`Knowledge/standards.md#logging`) — evidence in the log
- [ ] STATUS = DONE (or BLOCKED awaiting human go-live)
