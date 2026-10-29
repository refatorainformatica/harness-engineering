# Governance — Permissions

Levels:

| Level | Meaning |
|-------|---------|
| **auto** | Agent executes without asking |
| **ask** | Only with an explicit request in this message/task |
| **deny** | Never |

## Matrix

| Action | Level | Notes |
|--------|-------|-------|
| Read code / Knowledge / Specification | auto | |
| Edit code within scope | auto | |
| Build / test / lint within scope | auto | |
| Update Specification / ADR when it changed | auto | |
| Write Runtime/state | auto | |
| Sandbox worktree | ask | Unless the task requests isolation |
| `git commit` / `git push` | ask | |
| Add dependencies | ask | Prefer OSS (`cost.md`) |
| Proprietary cloud / paid LLM | ask | Only with an ADR justifying the gap |
| Deploy / release / production | ask | High impact: reinforced confirmation |
| Delete product files | ask | |
| Change an existing business rule (behavior, invariant, calculation, validation, acceptance criterion) | ask | Show current vs. proposed behavior and impact; never remove a working implementation without confirmation |
| IaC fmt / validate / lint / plan in dev | auto | `Tools/infra.md` |
| IaC apply / deploy / image push | ask | Prod: reinforced confirmation + reviewed plan |
| Change IAM / RBAC | ask | ADR if it widens privileges |
| Create/change a cloud resource outside IaC | deny | Everything as code |
| Destroy / delete a resource holding data | deny | |
| Apply a migration to a shared dev/staging database | ask | `Tools/infra.md` |
| Destructive migration (`DROP`, `TRUNCATE`, irreversible data change) | ask | Backup/restore plan; expand → contract |
| Apply migrations or run data changes in production | deny | Release process only |
| Mobile release (signing, store upload) | deny | Release process only |
| Create a long-lived key (access key, SA key, client secret) | deny | Federated identity (OIDC) |
| Force push / reset --hard / secrets | deny | |
| Global toolchain upgrade | deny | |
| `--no-verify` | deny | |

## Decision

1. Outside `Tools/` → deny or ask.
2. In doubt between auto and ask → **ask**.
3. A user request overrides **ask** for this task.
4. A request does **not** override **deny** without reinforced confirmation + justification.
5. High-impact AI → more `ask` on model, data and guardrails.
