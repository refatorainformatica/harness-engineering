# Workflow — Bug

Fix a defect with reproduction and controlled regression.

## Steps

1. Run + CONTEXT (symptom, severity, feature id if known).
2. Reproduce (Tester/Developer) — evidence in the LOG.
3. If the cause is architectural → Architect; otherwise Developer applies the smallest fix **in the feature folder**.
4. Tester: regression test that would fail before / passes after (create it if **AC-G\***).
5. Reviewer: minimal scope, no "drive-by refactoring".
6. DONE with a link to the original symptom.

## DoR

- [ ] Changes to existing business rules identified and confirmed by a human
- [ ] Clear symptom and reproduction steps
- [ ] Impact / severity estimated

## DoD

- [ ] Fix within scope
- [ ] Regression test exists (create it if AC-G\*) in the feature folder
- [ ] Unit tests for every new/changed behavior; coverage ≥ 80% line on every testable artifact
- [ ] Security baseline S1–S12 verified (`Governance/security.md`) — evidence in the log
- [ ] Logging verification L1–L8 (`Knowledge/standards.md#logging`) — evidence in the log
- [ ] STATUS = DONE
