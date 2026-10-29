# Workflow — Infra / DevOps

Change to infrastructure, pipeline, container, cluster or cloud resource (AWS, Azure, GCP, OCI or self-host).

Packs: `Knowledge/stacks/devops.md` + active provider(s). Tools: [Tools/infra.md](../Tools/infra.md).

## Steps

1. Run + CONTEXT (target environment, provider, blast radius, rollback).
2. **Architect**: new proprietary managed service, network, IAM or data → ADR (`Governance/cost.md`, `security.md`).
3. Spec in `Specification/features/<id>/` (an `infra-*` feature when it does not belong to a product feature).
4. **Developer**: changes **only in code** (IaC, manifests, pipeline) — nothing manual in the console.
5. **Tester**: `iac.fmt` + `iac.validate` + `iac.lint` + `iac.test`/`k8s.validate`; `iac.plan` in dev/sandbox attached to the LOG as evidence.
6. **Reviewer**: plan with no unexpected destruction, tags/labels, least privilege, secrets via secret manager, estimated cost.
7. `iac.apply` / deploy = **ask** (prod: reinforced confirmation, window and rollback defined).
8. Post-apply: `plan` with no drift + health/SLO verified.

## DoR

- [ ] Environment and provider defined; ADR if there is a new service/IAM
- [ ] Rollback defined
- [ ] Credentials via federated identity (no long-lived key)

## DoD

- [ ] IaC/manifest gates green
- [ ] Plan reviewed and recorded; no unapproved `destroy`
- [ ] Tags/labels + budgets/alerts when there is new cost
- [ ] Docs (infra/runbook `docs/`) updated
- [ ] `harness.check` without errors + final validation in the LOG
- [ ] Unit tests for every new/changed behavior; coverage ≥ 80% line on every testable artifact
- [ ] Security baseline S1–S12 verified (`Governance/security.md`) — evidence in the log
- [ ] Logging verification L1–L8 (`Knowledge/standards.md#logging`) — evidence in the log
- [ ] STATUS = DONE (or BLOCKED awaiting human apply)
