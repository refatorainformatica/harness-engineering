# Rules baseline

Canonical rules of the kit. Adjust to the company/product; anything specific to one repository belongs in the generated overlay (`<!-- HARNESS:PROJECT-* -->` sections and `Agents/project.md`). Every rule has **one** owner file; the others link to it.

## Mandatory (every project)

| Rule | Owner |
|------|-------|
| Feature-first: code and tests in the feature folder; legacy code migrates when touched | `Knowledge/standards.md` |
| New features mirror the closest existing feature's structure; no new styles/layers without Architect + ADR | `Knowledge/standards.md` |
| Lean classes: private handler helpers become feature services (interface + implementation + tests) | `Knowledge/standards.md` |
| Rich domain always: rules in entities/value objects; handlers/services orchestrate | `Knowledge/standards.md`, `Governance/architecture.md` |
| Small cohesive classes (entities = core business logic only; orchestration in lean services); reuse shared code without crossing Bounded Contexts | `Knowledge/standards.md` |
| Code preservation: never remove class/property attributes; never change logic or remove code that breaks behavior | `Knowledge/standards.md` |
| Business-rule changes require human confirmation (`ask`) | `Governance/permissions.md` |
| Unit tests in every change; ≥ 80% line coverage on every testable artifact (floor) | `Governance/quality.md` |
| Test naming (English), mandatory scenarios, AAA, deterministic, mocks only at the edges, idempotent test work | `Knowledge/standards.md` |
| Rich structured logging, verified with L1–L8 on every implementation | `Knowledge/standards.md#logging` |
| Security baseline S1–S12 verified on every implementation | `Governance/security.md` |
| Code docs in English for every new/changed member + affected `docs/` pages; no DONE without docs | `Knowledge/standards.md` |
| Final validation of every rule + `harness.check` before DONE | `Runtime/loop.md` |
| Execution bias within `auto` (edit instead of analysis-only, batches, idempotency) — never overrides `ask`/`deny` | `Runtime/loop.md` |
| OSS first: open source → self-host → proprietary cloud only with an ADR | `Governance/cost.md` |
| Acceptance = **AC-T\*** (test) or **AC-G\*** (gap + stub in the feature folder) | `Knowledge/standards.md` |
| Secrets / keystores / service-account keys never in git; PII out of logs | `Governance/security.md` |
| Commit/push/`--no-verify`/force push per the matrix | `Governance/permissions.md`, `Tools/git.md` |
| Do not expand scope to unblock; ~12 iterations per run | `Runtime/loop.md` |
| Tools use `auto` / `ask` / `deny` (never "OK") | `Tools/*.md` (checked by `harness.check`) |
| One language: the harness is in English; code docs, logs and test names in English | `Knowledge/standards.md#languages` |

## Conditional (stack packs and workflows)

| When | Rule | Owner |
|------|------|-------|
| .NET / Blazor / Java-Kotlin / Android / TypeScript / Node / Angular / React / React Native / Vue / Flutter / iOS / Python / Go / Rust / PHP / Ruby | Doc format, test and coverage tooling, logging API, attributes to preserve, structure | `Knowledge/stacks/<pack>.md` |
| Schema migrations | Versioned migrations only; expand → contract; destructive changes `ask`; production `deny` | `Knowledge/stacks/database.md`, `Tools/infra.md` |
| Data & ML | Tested transformations, data-quality gates, PII masking, no outputs in committed notebooks | `Knowledge/stacks/data.md` |
| Mobile (Android / iOS / React Native) | Secrets never in the app bundle; secure storage; no cleartext traffic; releases `deny` for agents | `Knowledge/stacks/{android,ios,react-native}.md` |
| Infra, pipelines, containers | IaC-only changes; plan → `ask` apply; `destroy` denied; pinned versions; tags/labels | `Knowledge/stacks/devops.md`, `Workflows/infra.md`, `Tools/infra.md` |
| AWS / Azure / GCP / OCI | Federated/managed identity, least privilege, secret managers, private by default, budgets | `Knowledge/stacks/{aws,azure,gcp,oci}.md` |
| AI features | No production data in prompts; OSS/local models first | `Governance/security.md`, `Governance/cost.md` |
| Docker | Do not bring up the whole compose stack for a unit test | `Governance/cost.md` |

## Automated checks (`Tools/bin/check-harness.py`)

| Check | Mode |
|-------|------|
| Harness structure, legacy names, Tools levels, index ↔ folders, AC-T\* ↔ files, active packs, placeholders | always |
| Removed attributes/annotations and IaC protections | `--diff` / `--staged` |
| Cloud secrets, sensitive files (`.env`, tfstate, keys) | `--diff` / `--staged` |
| Insecure code/IaC/manifest patterns (injection, TLS off, eval/unsafe deserialization, shell from input, XSS sinks, auth bypass, open CORS, weak crypto, public storage, open ingress, IAM wildcards, mobile cleartext/ATS, exported Android components, destructive SQL migrations) | `--diff` / `--staged` |
| Logging: interpolated messages, sensitive values in log calls, orchestrators without a logger | `--diff` / `--staged` |
| New code without unit tests, tests outside a feature folder, test naming | `--diff` / `--staged` |
| Line coverage ≥ 80% per artifact (Cobertura, JaCoCo, LCOV) | `--coverage` |

Heuristics complement human review; they never replace the S1–S12 / L1–L8 verification recorded in the run log.

## What fill/enrich **cannot** delete

`fill-harness.py` and `enrich-harness.py` **merge** `<!-- HARNESS:PROJECT-* -->` overlays and write `Agents/project.md`. They never replace Agents, Workflows or the Governance baseline.

## Explicitly out of the baseline

- Unrestricted EXECUTION-FIRST / auto-approve (conflicts with `permissions.md`) — only the execution bias within `auto` is part of the baseline
- Inferring data classification from the stack alone (e.g. "uses Firestore ⇒ clinical data")
- Commands and paths of a single repository
- Corporate SDLC/RACI (map yours in `docs/sdlc-mapping.md`)
