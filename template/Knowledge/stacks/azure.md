# Stack pack — Azure

Layer on top of [devops.md](./devops.md) (read both). Azure usage recorded in an ADR (`Governance/cost.md`).

## Identity and access

- Microsoft Entra ID for people (PIM for privileged access); **Managed Identity** for workloads (Workload Identity on AKS).
- CI via federated credentials (OIDC) on an App Registration/Managed Identity — no client secret in pipelines.
- RBAC at the minimum scope (resource group/resource); avoid `Owner`/`Contributor` on the subscription for workloads; Azure Policy for guardrails.

## Secrets and config

- Key Vault (RBAC, soft delete + purge protection) referenced via Managed Identity; App Configuration for non-secret config.
- Never a connection string with `AccountKey=` / `SharedAccessKey=` in code or pipelines — prefer identity-based auth.

## IaC

- Terraform/OpenTofu (`azurerm`/`azapi`) with state in a Storage Account (encrypted, lease lock, identity-based access); or Bicep when already adopted (`az bicep build` + what-if as `plan`).
- Mandatory tags via `tags` + Azure Policy for inheritance/enforcement.
- Naming per the Cloud Adoption Framework (or the company standard).

## Network and security

- VNet with dedicated subnets; Private Endpoints for PaaS; minimal NSGs; no public RDP/SSH (Bastion).
- Defender for Cloud per company policy; diagnostic settings to Log Analytics.

## Compute / data (portable first)

- Containers: AKS or Container Apps; App Service/Functions when the ADR justifies it.
- Database: Azure Database for PostgreSQL/MySQL before a proprietary service (Cosmos DB) unless required.

## Observability and cost

- Azure Monitor / Application Insights via OpenTelemetry (Azure Monitor OTel Distro) or an OSS backend.
- Budgets + alerts in Cost Management; mandatory cost tags.

## CI/CD

- Azure Pipelines (`azure-pipelines.yml`) or GitHub Actions with federated `azure/login`; environments with approval for prod.

## Tools

- `az` CLI read-only (`show`/`list`) and `what-if` on non-prod: see [Tools/infra.md](../../Tools/infra.md).
