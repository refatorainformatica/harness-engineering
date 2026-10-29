# Acceptance Criteria — <id>

> **Source of truth:** the repository/solution unit tests. Each AC-Txx = one existing test.

## Validation command (scope)

```bash
# E.g.: dotnet test … --filter FullyQualifiedName~Features.<Name>
# E.g.: flutter test test/features/<id>/
```

## Criteria (= existing tests)

- [ ] AC-T01 — `Features/<FeatureName>/…` or `test/features/<id>/…` :: test name
- [ ] AC-P01 — Use cases consistent with the tests above
- [ ] AC-P02 — No violation of Knowledge / Governance
- [ ] AC-P03 — Tests in the feature folder (`standards.md`)

## Evidence

| AC | Test | File | Command | Result |
|----|------|------|---------|--------|
| AC-T01 | … | `…` | `…` | pending |

## Gaps (AC-G*)

- Behavior without an automated test → **AC-Gxx** + minimal stub **in the feature folder**; regenerate this file.
- Feature DoD: AC-T\* green **or** AC-G\* justified + stub created.
- Do not mark DONE with only process AC-P\*.
