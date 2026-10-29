# Workflow — Feature

Deliver a new capability or a planned evolution.

## Steps

1. Run (`Runtime/run.md`) + CONTEXT (feature id, gates).
2. If it is a new feature: copy `Specification/templates/*` → `features/<id>/` and register it in the INDEX.
3. **Architect** (if there is new design/API/boundaries) → ADR if needed (mandatory for proprietary cloud).
4. **Developer** implements according to requirements/use-cases **in the feature folder**.
5. **Tester** proves acceptance (**AC-T\***; **AC-G\*** → stub).
6. **Reviewer** validates diff + Governance.
7. Loop until DONE; commit only with `ask`.

## DoR

- [ ] Changes to existing business rules identified and confirmed by a human
- [ ] Requirements + use-cases + acceptance filled in
- [ ] Relevant Knowledge read
- [ ] Permissions understood
- [ ] Paths in `Agents/project.md` checked

## DoD

- [ ] AC-T\* green **or** AC-G\* justified + stub created in the feature folder
- [ ] Code and tests in the feature folder
- [ ] Code docs + `docs/` delivered
- [ ] Final validation of all rules in the LOG
- [ ] INDEX/status updated
- [ ] No deny action
- [ ] Unit tests for every new/changed behavior; coverage ≥ 80% line on every testable artifact
- [ ] Security baseline S1–S12 verified (`Governance/security.md`) — evidence in the log
- [ ] Logging verification L1–L8 (`Knowledge/standards.md#logging`) — evidence in the log
- [ ] STATUS = DONE
