# Governance — Security

## Baseline rules

- Do not commit secrets, credentials, keystores or service accounts.
- Do not log tokens, PII or sensitive payloads.
- Respect the organization's data classification.
- New dependencies: assess CVEs / license before merge.
- Local config files (`.env`, `appsettings`, `dart_defines`, service accounts) stay gitignored.

## Secrets (default)

| Type | Where (expected) | Git |
|------|------------------|-----|
| Env / defines | `.env`, local config | gitignored |
| Cloud keys | service accounts / defines | gitignored |
| CI tokens | CI provider secrets | outside the repo |
| Cloud (AWS / Azure / GCP / OCI) | Secrets Manager / Key Vault / Secret Manager / OCI Vault; workloads via managed identity | never |
| IaC state | encrypted remote backend with lock | never |

## Cloud (AWS / Azure / GCP / OCI)

- CI and workloads authenticate via federated / managed identity (OIDC, IRSA, Managed Identity, Workload Identity) — no long-lived keys.
- Least privilege; action/resource wildcards only with an ADR.
- Resources private by default (no public endpoint, public bucket or open administrative port without justification).
- Details: `Knowledge/stacks/{aws,azure,gcp,oci}.md`; secret check on the diff: `harness.check`.

## Secure coding baseline (every implementation — mandatory)

Every change is verified against this list before DONE (Developer self-check, Reviewer gate, `harness.check` heuristics):

| # | Rule |
|---|------|
| S1 | **Input validation** at every boundary (API, messages, files, UI): type, size, format, allow-lists; reject by default. |
| S2 | **Authentication and authorization** on every new endpoint/handler/page; object-level checks (no IDOR); no anonymous access without spec/ADR. |
| S3 | **Injection**: parameterized queries/ORM only; no SQL, shell, LDAP, path or template built from input; no `eval`/dynamic code. |
| S4 | **Output encoding / XSS**: framework escaping; no raw HTML sinks without sanitization; CSP when applicable. |
| S5 | **Secrets**: never in code, config, logs, tests or IaC; secret manager + federated/managed identity. |
| S6 | **Sensitive data**: PII and secrets never logged; encryption in transit (TLS, certificate validation on) and at rest when the data class requires it. |
| S7 | **Dependencies**: new or upgraded packages checked for CVEs and license (`security.scan`); pinned versions and lock files. |
| S8 | **Errors**: no stack traces, internal ids or secrets returned to clients; failures logged with context server-side. |
| S9 | **Crypto**: platform libraries only; no MD5/SHA1/DES/ECB for security purposes; secure random for tokens. |
| S10 | **Web/API config**: restrictive CORS, CSRF protection for cookie auth, secure/HttpOnly/SameSite cookies, rate limiting on public endpoints. |
| S11 | **Infra**: least privilege IAM, private by default, no public storage or open admin ports (`Knowledge/stacks/devops.md`). |
| S12 | **Files and deserialization**: validate uploads (type, size, path); safe deserializers only. |

Evidence: record in the run `log.md` which rules applied and how they were verified (test, scan, review). Anything not applicable is marked N/A with a reason. A finding with no fix in scope → `BLOCKED`, never silently ignored.

## AI

- Prompts do not include sensitive production data without authorization.
- External models: prefer OSS/local; proprietary cloud only with a documented gap (ADR + `Governance/cost.md`).
- Input/output guardrails when the feature uses a model.
- Critical decisions with human approval (`ask`).
- A human approves commit/push/release (`ask`).

## Sensitive data (when the domain requires it)

- Clinical, financial or PII data only according to the product's classification.
- Never plain text remotely if the spec requires encryption (blobs/E2E).
- Do not infer "clinical data" just because the repo uses Firestore or e2e.

## Project

- …
