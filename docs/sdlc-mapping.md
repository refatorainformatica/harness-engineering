# SDLC + AI ↔ AI Engineering Harness mapping

Adapt phase and gate names to your company's model.

| Phase | Gate (e.g.) | Harness | Evidence |
|-------|-------------|---------|----------|
| Discovery | G1 | `Knowledge/domain.md` | Criticality in the run `context.md` |
| Architecture | G2 | `Knowledge/architecture.md` + ADR + stack packs | Specs `planned` |
| Build | G3 | Workflows + Developer/Tester roles | Unit tests, coverage ≥ 80%, VERIFY entries in the run log |
| Validation | G4 | Acceptance + Reviewer role + `harness.check` | AC checked; S1–S12 and L1–L8 recorded; risks in `status.md` |
| Release | G5 | Governance + `ask` permissions + `infra` workflow | Plan reviewed, apply approved, rollback per process |
| Evolution | G6 | Feature index + ADR review + evals | Specs `stable`/`partial`; eval scorecard |

## AI controls

| Control | Where |
|---------|-------|
| Accountable human | `ask` permissions; business-rule changes need confirmation |
| Model / data | Spec + `Knowledge/standards.md` + `Governance/security.md` |
| Guardrails / fallback | Specification + `Governance/security.md` |
| No secrets in prompts or code | `deny` permissions + security + `harness.check` secret scan |
| Token / cloud cost | `Governance/cost.md` |
| Rule adherence per agent/model | [evals/](../evals/readme.md) |

## DoR / DoD

**Ready:** clear acceptance, Knowledge read, workflow chosen, business-rule changes confirmed, run in PLAN.
**Done:** AC OK, unit tests + coverage ≥ 80%, S1–S12 and L1–L8 recorded, `harness.check` clean, no `deny` action, STATUS=DONE, specs/ADR/docs updated.
