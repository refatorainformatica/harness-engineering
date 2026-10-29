# Stack pack — Google Cloud (GCP)

Layer on top of [devops.md](./devops.md) (read both). GCP usage recorded in an ADR (`Governance/cost.md`).

## Identity and access

- Cloud Identity/Workspace for people; **dedicated service accounts per workload** (Workload Identity on GKE).
- CI via Workload Identity Federation (OIDC) — service account JSON keys in the repo or pipeline are forbidden.
- IAM per resource/project with minimal predefined roles — avoid `roles/owner`/`roles/editor`; Organization Policies as guardrails.

## Secrets and config

- Secret Manager (versions + rotation) accessed by the workload's service account; CMEK via Cloud KMS when required.
- Never `"private_key"` / `"type": "service_account"` in a versioned file.

## IaC

- Terraform/OpenTofu (`google`/`google-beta`) with state in GCS (versioned, uniform access, encryption) — native lock of the GCS backend.
- Mandatory `labels` on every resource (equivalent to tags); one GCP project per environment.

## Network and security

- VPC with private subnets, Cloud NAT, Private Service Connect / Private Google Access; minimal firewall; IAP for administrative access.
- Security Command Center and Cloud Audit Logs per company policy.

## Compute / data (portable first)

- Containers: GKE (Autopilot when it fits) or Cloud Run; Cloud Functions when the ADR justifies it.
- Database: Cloud SQL (PostgreSQL/MySQL) / AlloyDB before a proprietary service (Firestore/Spanner/BigQuery) unless required.

## Observability and cost

- Cloud Logging/Monitoring/Trace via OpenTelemetry or an OSS backend.
- Budgets + alerts in Billing; billing export for analysis; mandatory cost labels.

## CI/CD

- Cloud Build (`cloudbuild.yaml`) / Cloud Deploy or GitHub Actions with federated `google-github-actions/auth`; Artifact Registry for images.

## Tools

- `gcloud` CLI read-only (`describe`/`list`) on a non-prod project: see [Tools/infra.md](../../Tools/infra.md).
