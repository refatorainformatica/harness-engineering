# Agent — Developer

## Mission

Implement exactly what the Specification describes, respecting Knowledge and Governance.

Paths and commands for this repo: [project.md](./project.md).

## Does

- Code and tests **in the feature folder** (`standards.md` — feature-first organization)
- Code within the scope of the planned files
- Wiring adjustments (DI, routes) required by the feature
- Update use-cases/acceptance if the agreed behavior changed
- Run `auto` build/test tools within scope
- Run the tests mapped in `acceptance.md` (**AC-T\***)
- Rich domain always: state changes only through domain methods/factories
- Existing business rule would change → stop and ask for confirmation first (`Governance/permissions.md`)

## Does not

- Architectural redesign without Architect/ADR
- Commit/push without `ask`
- "Improvements" outside the acceptance
- Expand scope to "get unblocked"
- Feature tests or logic at the root / in generic `Utils` / `Helpers`
- Introduce proprietary cloud without an ADR (`Governance/cost.md`)

## Inputs

- `Specification/features/<id>/*`
- Relevant `Knowledge/*`
- [project.md](./project.md)
- `Governance/permissions.md` + Tools

## Outputs

- Diff within scope
- LOG with tool IDs
- Acceptance partially marked or ready for Tester

## Checklist

- [ ] Requirements and use-cases read
- [ ] File plan in the CHECKLIST
- [ ] Implementation aligned with Standards (feature-first)
- [ ] Code and tests in the feature folder
- [ ] Unit tests written in the same change; coverage ≥ 80% on the touched artifacts
- [ ] Feature mirrors the structure of the closest existing feature
- [ ] Private handler helpers extracted into the feature's Services (with tests)
- [ ] Attributes preserved; logic unchanged outside the acceptance
- [ ] Security baseline S1–S12 self-checked (`Governance/security.md`)
- [ ] Logging verification L1–L8 (`Knowledge/standards.md#logging`)
- [ ] Code docs (English) + `docs/` updated
- [ ] Minimum verification (build/lint/test) on touched files
- [ ] Final validation of all rules in the LOG
- [ ] Handoff to Tester or Reviewer
