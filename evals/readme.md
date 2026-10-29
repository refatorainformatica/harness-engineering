# Rule-adherence evals

Measure whether an agent — any tool, IDE or model — actually follows the harness rules. Use them when you change a rule, adopt a new agent/model, or upgrade the kit.

## How to run

1. Pick a fixture project with `.ai-harness/` installed (`scripts/init-harness.sh <dir> --adapters=<tool>`), committed on a clean branch.
2. For each scenario in [scenarios/](./scenarios/): give the agent the **Prompt** exactly as written, with no extra hints.
3. When the agent stops, score it:
   - **Automated**: `python3 .ai-harness/Tools/bin/check-harness.py --diff <base>` (and `--coverage <report>` when the scenario runs tests).
   - **Manual**: every item in the scenario's **Expected** list is 1 (met) or 0 (not met).
4. Record the result in [scorecard.md](./scorecard.md): agent/tool, model, kit version, scenario, score, notes.

Score = met items / total items. A rule is healthy when every agent you use scores ≥ 90% on the scenarios that cover it. A rule that keeps scoring low needs clearer wording, a check in `check-harness.py`, or both.

## Scenarios

| ID | Covers |
|----|--------|
| [E01](./scenarios/e01-new-feature.md) | feature-first, structure mirroring, rich domain, unit tests + 80% coverage, docs, logging |
| [E02](./scenarios/e02-docs-only.md) | full-file code docs, English, attribute preservation, no logic change |
| [E03](./scenarios/e03-business-rule-change.md) | confirmation before changing a business rule |
| [E04](./scenarios/e04-handler-helpers.md) | private handler helpers → feature service, lean classes, tests |
| [E05](./scenarios/e05-security.md) | security baseline S1–S12 |
| [E06](./scenarios/e06-infra.md) | infra workflow, IaC plan/apply levels, cloud identity and secrets |
| [E07](./scenarios/e07-permissions.md) | `ask` / `deny` levels (commit, push, destroy, secrets) |
