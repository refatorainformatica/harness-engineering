# Stack pack — DevOps / Platform

Base for [aws.md](./aws.md), [azure.md](./azure.md), [gcp.md](./gcp.md) and [oci.md](./oci.md). Complements [standards.md](../standards.md) and [Governance/](../../Governance/). Workflow: [Workflows/infra.md](../../Workflows/infra.md) · Tools: [Tools/infra.md](../../Tools/infra.md).

## Principles

- **Portable first** (`Governance/cost.md`): container images (Open Container Initiative), Kubernetes, Terraform/OpenTofu, Helm, OpenTelemetry. Proprietary managed service only with an ADR (real gap).
- Everything as code: infra, pipelines, policies, dashboards/alerts. Nothing created by hand in the console (if it is, import it into IaC and record it in the LOG).
- Environments (dev / staging / prod) with **the same** parameterized definition; differences only in variables.
- Infra change = reviewed `plan` → `apply` with **ask** (prod: reinforced confirmation). `destroy` = **deny**.

## IaC (Terraform / OpenTofu; Bicep, CDK, Pulumi when already adopted)

- Structure: reusable `infra/modules/<component>/` + `infra/envs/<env>/` that only compose modules; no loose resources in the root.
- Pinned versions: `required_version`, providers and modules with explicit versions; lock file committed.
- Remote state with lock and encryption (provider bucket/storage or OSS backend); **never** state in git.
- Variables with `description` + `type` + `validation` when there is a rule; sensitive outputs with `sensitive = true`.
- Mandatory tags/labels on every resource: `owner`, `env`, `app`, `cost-center` (or the company standard).
- Gates: `fmt -check`, `validate`, linter (tflint), policy/security scan (Checkov, Trivy, tfsec, OPA/Conftest).
- Preserve `lifecycle` (`prevent_destroy`, `ignore_changes`), `moved`/`import` blocks and `depends_on` — they are the "attributes" of infra (preservation rule).
- Drift: a `plan` with no changes is expected after apply; drift detected → record it and fix it via code.

## Containers

- Multi-stage Dockerfile, minimal base image with pinned version/digest, non-root user, `HEALTHCHECK` when applicable, `.dockerignore`.
- One image for all environments (config via env/secret); immutable tag (commit SHA), never only `latest`.
- Image scan (Trivy/Grype) in CI; SBOM when the company requires it.

## Kubernetes / Helm

- `resources.requests/limits`, `readinessProbe`/`livenessProbe`, `securityContext` (non-root, read-only FS when possible), `PodDisruptionBudget` and HPA for critical workloads.
- Secrets via the secret manager's operator/CSI (External Secrets, Secrets Store CSI) — not in `values.yaml`.
- Rendered manifests validated (kubeconform/kube-linter) before applying; GitOps (Argo CD / Flux) when adopted.

## CI/CD

- Pipeline as code (GitHub Actions, Azure Pipelines, GitLab CI, Cloud Build, CodePipeline, Jenkins — whatever the project uses).
- Cloud authentication via **federated identity (OIDC / workload identity)** — no long-lived key in CI secrets.
- Stages: build → test (scope) → scan → package → deploy dev → promotion with human approval for prod.
- Third-party actions/images with pinned versions (SHA/digest).
- Deploy with a defined rollback strategy (blue/green, canary or rolling + automatic rollback on health).

## Coverage

- IaC modules with logic (conditionals, loops, validations) are testable artifacts: `terraform test`/Terratest covering their variables and outputs. Pipelines and manifests are validated, not coverage-measured.

## Observability

- OpenTelemetry for traces/metrics/logs; exporters to the provider's backend or OSS (Prometheus, Grafana, Loki, Tempo, Jaeger).
- Structured JSON logs with correlation/trace id (`standards.md` → Logging).
- SLO-based alerts (latency, errors, saturation) versioned together with the service.

## Infra tests

- `terraform test` / Terratest for modules; `plan` as evidence in the PR (AC-T\* may point to the module test).
- Pipelines and manifests validated locally without prod credentials.
