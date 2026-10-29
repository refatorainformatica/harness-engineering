# Stack pack — Oracle Cloud Infrastructure (OCI)

Layer on top of [devops.md](./devops.md) (read both). Use of OCI recorded in an ADR (`Governance/cost.md`).

## Identity and access

- Identity domains for people (MFA); **instance principals / resource principals / OKE workload identity** for workloads.
- CI through OIDC/workload identity federation where supported — no API signing keys in pipelines; if a key is unavoidable, it lives in the CI secret store with rotation and an ADR.
- IAM policies per compartment with least privilege (`use`/`read` before `manage`); no `manage all-resources in tenancy` for workloads.

## Secrets and config

- OCI Vault (keys + secrets); never private keys, auth tokens or `~/.oci/config` in the repository.

## IaC

- Terraform/OpenTofu (`oracle/oci`) with state in Object Storage (versioned, private, encrypted) or OCI Resource Manager; freeform/defined tags mandatory.
- One compartment per environment.

## Network and security

- VCN with private subnets, NAT/Service Gateways, NSGs with minimum rules; Bastion service for admin access; Cloud Guard as the company requires.

## Compute / data (portable first)

- Containers: OKE or Container Instances; Functions when the ADR justifies it.
- Database: MySQL HeatWave / PostgreSQL before Autonomous Database, unless a requirement calls for it.

## Observability and cost

- OCI Logging/Monitoring/APM via OpenTelemetry or an OSS backend; budgets with alerts per compartment; cost-tracking tags.

## Tools

- CLI `oci` read-only (`get`/`list`) in a non-prod compartment: see [Tools/infra.md](../../Tools/infra.md).
