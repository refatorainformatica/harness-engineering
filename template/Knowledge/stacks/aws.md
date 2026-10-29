# Stack pack — AWS

Layer on top of [devops.md](./devops.md) (read both). AWS usage recorded in an ADR (`Governance/cost.md`).

## Identity and access

- IAM Identity Center (SSO) for people; **roles** for workloads (IRSA / EKS Pod Identity, ECS task role, Lambda execution role).
- CI via OIDC (`sts:AssumeRoleWithWebIdentity`) — IAM user access keys in pipelines are forbidden.
- Least privilege: policies per resource/ARN, no `"Action": "*"` / `"Resource": "*"` without justification in an ADR; permission boundaries and SCPs when Organizations is used.

## Secrets and config

- Secrets Manager (rotation) or SSM Parameter Store `SecureString`; KMS with a CMK for sensitive data.
- Never an `AKIA…`/secret key in code, tfvars or CI variables.

## IaC

- Terraform/OpenTofu (`hashicorp/aws`) with state in S3 (versioned, encrypted, block public access) + lock (DynamoDB or native S3 lock); or CDK/CloudFormation/SAM when already adopted.
- `default_tags` in the provider with the mandatory tags.

## Network and security

- VPC with private subnets for workloads; minimal security groups; VPC endpoints for AWS services; no `0.0.0.0/0` on administrative ports.
- S3: block public access, encryption, versioning for data; CloudTrail + GuardDuty + Security Hub/Config per company policy.

## Compute / data (portable first)

- Containers: EKS or ECS/Fargate; serverless (Lambda) when the ADR justifies it.
- Database: RDS/Aurora (OSS engines — PostgreSQL/MySQL) before a proprietary service (DynamoDB) unless required.

## Observability and cost

- CloudWatch (logs/metrics/alarms) or OTel → the adopted backend; X-Ray/ADOT for traces.
- AWS Budgets + alerts; Cost Allocation Tags enabled; Savings Plans/rightsizing review outside the agent loop.

## Tools

- `aws` CLI read-only (`describe`/`list`/`get`) with a non-prod profile: see [Tools/infra.md](../../Tools/infra.md).
