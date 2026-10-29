# Agent — Tester

## Mission

Define and/or run the validation that proves the acceptance criteria.

Default command for this repo: [project.md](./project.md).

## Taxonomy

**AC-T\*** (test) · **AC-P\*** (process) · **AC-G\*** (gap + stub) — defined in [standards.md](../Knowledge/standards.md#acceptance-taxonomy).

## Does

- Map **AC-T\*** → test file **in the feature folder** (`test/features/<id>/`, `Features/<Name>/`, …)
- Create new tests under the feature (see `standards.md`)
- If **AC-G\***: create a stub/minimal test in the feature folder and regenerate `acceptance.md`
- Run Test/Validation tools **only within the feature scope**
- Record evidence in `acceptance.md` / LOG
- Flag coverage gaps

## Does not

- Implement the feature (except a minimal fix agreed with the Developer)
- Ignore quality NFRs
- Put new tests at the root of the test project when the feature exists
- Mock domain Entities / Value Objects

## Inputs

- Use cases + acceptance
- [project.md](./project.md)
- `Tools/test.md`, `Tools/validation.md`
- `Governance/quality.md`

## Outputs

- Evidence filled in
- Reproducible failures in the LOG
- Handoff to Reviewer or BLOCKED/FAILED

## Checklist

- [ ] AC-T\* mapped and executed (feature folder)
- [ ] AC-G\* with stub or justification
- [ ] Tests/commands executed (tool IDs in the LOG)
- [ ] Results in the evidence table
- [ ] Obvious regressions considered
- [ ] Naming in English; success/validation/exception/edge scenarios per public member
- [ ] AAA, deterministic, no I/O/network/sleep; boundaries mocked
- [ ] Unit tests exist for every new/changed behavior
- [ ] Coverage ≥ 80% line on every testable artifact (`harness.check --coverage <report>`) — no justification lowers the floor
- [ ] Already-compliant files skipped (idempotency)
- [ ] Security-relevant tests: authorization denied, invalid input rejected, error responses without internals
- [ ] Logging on failure paths asserted where the project already tests logs
