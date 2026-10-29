# Governance — Cost

FinOps / cost of cloud, CI and AI tokens.

## OSS preference (mandatory)

When proposing a dependency, model or infra, **in this order**:

1. Open source library/model (local or self-hosted)
2. Self-hosted OSS API/service (Docker/K8s)
3. Proprietary cloud **only** with an ADR justifying the gap (not convenience)

Checklist: can it be done with OSS? If so, do it with OSS. Paid cloud only with a real, documented gap.

## Baseline rules

- Avoid cloud SKU/plan upgrades without `ask`.
- Prefer free tier / self-host while it fits.
- Avoid expensive jobs/pipelines in the agent loop without need.
- Minimal verification (feature/run tests) — not the whole monolith suite on every iteration.
- Do not start the full compose stack just for a unit test.
- Use of paid models/APIs: only within the authorized scope; prefer local (e.g. Ollama).
- Max. ~12 iterations/run (see `Runtime/loop.md`); avoid expensive rebuilds in the loop.

## Cloud (AWS / Azure / GCP / OCI)

- Choice of provider and of each proprietary managed service = ADR (gap vs. portable option: Kubernetes, PostgreSQL, OpenTelemetry, Terraform/OpenTofu).
- Mandatory cost tags/labels (`owner`, `env`, `app`, `cost-center`); budgets with alerts per environment.
- Non-prod environments can be shut down/scaled to zero when possible; no premium SKU in dev.
- Estimate the cost of the change in the Reviewer (e.g. Infracost) when the plan creates a paid resource.

## Limits (company)

| Resource | Policy |
|----------|--------|
| Cloud SKU | no upgrade without `ask`; prefer free tier / self-host |
| CI / build | tests within the feature/run scope |
| LLM tokens | local first; paid API only with authorization |
| Containers | full compose is not a prerequisite for unit tests |
| Agent | ~12 iterations/run; BLOCKED with a summary if exceeded |

## Project

- …
