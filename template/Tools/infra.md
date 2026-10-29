# Tools — Infra / DevOps

Levels aligned with `Governance/permissions.md`. Per-provider details: `Knowledge/stacks/{devops,aws,azure,gcp,oci}.md`. Remove what the project does not use.

## IaC (Terraform / OpenTofu — `tf` = `terraform` or `tofu`)

| ID | Command | Notes |
|----|---------|-------|
| `iac.fmt` | `tf fmt -recursive` | auto |
| `iac.validate` | `tf init -backend=false && tf validate` | auto |
| `iac.lint` | `tflint` / `checkov -d infra` / `trivy config infra` | auto |
| `iac.test` | `tf test` / Terratest | auto (no prod credentials) |
| `iac.plan` | `tf plan -out=plan.tfplan` | auto only in dev/sandbox with read-only credentials; **ask** in staging/prod |
| `iac.apply` | `tf apply plan.tfplan` | **ask** (prod: reinforced confirmation + reviewed plan) |
| `iac.import` | `tf import` / `import` block | **ask** |
| `iac.state.edit` | `tf state rm/mv`, `force-unlock` | **ask** |
| `iac.destroy` | `tf destroy` / remove a resource holding data | **deny** |

Bicep / CDK / Pulumi / CloudFormation: same levels (`what-if`/`diff`/`preview` = plan; deploy = apply).

## Containers / Kubernetes

| ID | Command | Notes |
|----|---------|-------|
| `container.build` | `docker build` / `podman build` | auto |
| `container.scan` | `trivy image` / `grype` | auto |
| `container.push` | push to registry | **ask** |
| `k8s.render` | `helm template` / `kustomize build` | auto |
| `k8s.validate` | `kubeconform` / `kube-linter` | auto |
| `k8s.read` | `kubectl get/describe/logs` | **ask** (may expose data) |
| `k8s.apply` | `kubectl apply` / `helm upgrade` | **ask** |
| `k8s.delete` | `kubectl delete` on a shared cluster | **deny** |

## Cloud CLI

| ID | Command | Notes |
|----|---------|-------|
| `cloud.read` | `aws … describe/list/get`, `az … show/list`, `gcloud … describe/list`, `oci … get/list` | **ask** (non-prod account/project/compartment) |
| `cloud.write` | create/change a resource via CLI | **deny** — use IaC (`iac.apply`) |
| `cloud.iam.change` | change IAM/RBAC/roles | **ask** + ADR if it broadens privilege |
| `cloud.credentials.create` | create access key / client secret / SA key | **deny** — use federated identity |

## Database migrations

| ID | Command | Notes |
|----|---------|-------|
| `db.migrate.new` | create a migration with the project tool | auto |
| `db.migrate.validate` | `flyway validate` / `liquibase validate` / `alembic check` / `prisma validate` / dry-run | auto |
| `db.migrate.local` | apply migrations to a local/ephemeral database | auto |
| `db.migrate.shared` | apply to a shared dev/staging database | **ask** |
| `db.migrate.prod` | apply to production | **deny** for agents — release process only |
| `db.destructive` | `DROP` / `TRUNCATE` / irreversible data change in a migration | **ask** + backup/restore plan (`Knowledge/stacks/database.md`) |

## CI/CD

| ID | Action | Notes |
|----|--------|-------|
| `ci.pipeline.edit` | edit pipeline as code | auto within scope |
| `ci.pipeline.lint` | `actionlint` / provider validation | auto |
| `ci.pipeline.run` | trigger pipeline | **ask** |
| `ci.secrets.edit` | change CI secrets/variables | **deny** |
