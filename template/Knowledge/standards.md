# Standards — {{PROJECT}}

Engineering standards of the company/project. Complements [Governance/](../Governance/).

## Code

- Language / version:
- Style / formatter:
- Naming:
- Comments / API docs:

## Feature-first organization (mandatory)

Code is **always** organized by feature (business capability). The feature is the main folder axis; the technical layer is subordinate.

| Where | How |
|-------|-----|
| Specs | `Specification/features/<id>/` |
| Application code | folders/modules per feature (e.g. `Features/<Name>/`, `lib/features/<id>/`, `src/features/<id>/`) |
| Layers (domain/data/api/…) | **inside** the feature, not the other way around |
| Shared / core | only real cross-cutting concerns (DI, Result, logging, router). No business logic of a feature |

### Application rules

- **New** code is born feature-first. Legacy code migrates **when touched**.
- Generic `Common` / `Utils` / `Helpers` / `Entities` / `Models` for a feature's logic are forbidden — put it in the feature.
- Spec ↔ code: every new behavior maps to a feature in `Specification/features/<id>/`.
- Reviewer / Developer: reject diffs that introduce generic technical folders instead of features.

Adjust the concrete paths in [architecture.md](./architecture.md).

## Tests

- **Always implement unit tests** for every new or changed behavior, in the same change.
- **Coverage ≥ 80% line on every testable artifact** (floor — see `Governance/quality.md#coverage-mandatory`).

- Pyramid (unit / integration / e2e):
- Frameworks:
- Minimum coverage (if any):

### Feature-first organization (mandatory)

Tests are **always** created and stored **per feature**, mirroring the code and the spec.

| Layer | Path (examples — adapt to the stack) |
|-------|--------------------------------------|
| Backend / API | `tests/.../Features/<FeatureName>/…` |
| Frontend / mobile | `test/features/<id>/…` or `__tests__/features/<id>/…` |
| Spec / AC | Each AC-T\* points to a test under the feature folder |

- Shared fixtures (containers, app factories) live in `Shared/` — do **not** mix feature tests there.
- Tests of cross-cutting pieces → `Features/Common/` or `Shared/` with an explicit name.
- A **new** test is born under the feature. Legacy tests at the root migrate **when touched**.
- Creating loose tests at the root of the test project when the feature exists is forbidden.

### Naming (mandatory, English)

- Class: `{ClassName}Tests`
- Method: `MethodName_ShouldExpectedBehavior_WhenCondition` (e.g. `CreateUser_ShouldReturnSuccess_WhenDataIsValid`, `GetById_ShouldThrowNotFoundException_WhenEntityDoesNotExist`)
- File (Dart/JS): `{subject}_test.dart` / `{subject}.test.ts` inside the feature folder
- When renaming tests to the pattern: do **not** change the intent of the test.

### Mandatory scenarios (every public member)

- Success path
- Validation failures
- Exception scenarios
- Edge cases, when applicable

Coverage priority: Domain → Application → Infrastructure → API (only if it has business rules). Domain invariants are a critical target; Entities are tested by behavior; Value Objects validate invariants.

### Test quality

- AAA pattern (Arrange / Act / Assert)
- Deterministic: no real I/O, no network, no `sleep` / time-based waits
- Clear assertions; **one** logical behavior per test
- Always mock external dependencies: repositories, database access, HTTP clients, message brokers, filesystem, clock, external services
- Test and mock frameworks: defined by the active [stack pack](./stacks/readme.md) or in [Agents/project.md](../Agents/project.md)

### Idempotency

- Skip a file that already has tests with compliant naming, estimated coverage ≥ 80% and no obvious missing scenarios.
- Revisit only if: coverage < 80%, public members without tests, non-compliant naming or broken tests.
- Do not recreate existing tests, do not rename repeatedly, do not reformat without functional gain. Minimal diffs.

## Code preservation (mandatory)

Applies to every task — especially documentation, refactoring and tests:

- Do not remove class attributes/annotations.
- Do not remove property attributes/annotations (e.g. `[JsonPropertyName]`, `@JsonProperty`, `@SerializedName`, decorators).
- Do not change code logic outside the task's acceptance.
- Changing an existing business rule requires explicit confirmation (`ask` in `Governance/permissions.md`): present current vs. proposed behavior and impacted tests before editing.
- Do not remove code in a way that breaks functionality.
- Validate **all** applicable rules at the end of each processing step (see `Runtime/loop.md` → DONE).

## Implementation structure

- A new feature **mirrors the closest existing feature**: same folder layout, DI module/registration, controllers/routes, domain, integrations and tests in the matching path. Concrete paths in [architecture.md](./architecture.md) and [Agents/project.md](../Agents/project.md).
- Do not introduce a new architectural style, naming scheme or layer when an established pattern already exists (otherwise: Architect + ADR).

### Lean classes / orchestrators

- Private helper methods of handlers / use cases / controllers do **not** stay in the orchestrator: extract them into a Service (interface + implementation) **inside the feature** (e.g. `Features/<Name>/Services/`), register it in the feature module and inject it.
- Lean classes: split responsibilities into focused services instead of large classes.
- Each extracted service has its own unit tests.
- Domain entities hold only core business logic. Technical orchestration and complex flows go to lean Application/Domain Services.
- Small, highly cohesive classes: one reason to change each.

### Reuse

- Maximize reuse: extract shared logic, common validations and generic utilities into reusable components instead of duplicating them.
- Respect Bounded Context limits: share generic/technical code (shared kernel, utilities); never share domain models across contexts — integrate through contracts.

## Logging

- Rich logs to trace each service end to end: start, key decisions, external calls and the outcome of each operation.
- Structured logs with templates and named placeholders carrying the flow identifiers (entity ids, job/run ids, counts, elapsed time). **Never** string interpolation/concatenation in the message — values go as structured arguments.
- Failures: log the exception with the same context.
- Deliberate levels: info for milestones; warning for recoverable anomalies; error for failures; debug for details.
- Log messages in English; PII and secrets kept out of logs (`Governance/security.md`).

### Logging verification (every implementation — mandatory)

Before DONE, each new or changed service/handler/controller/job is checked:

- [ ] L1 — Start of the operation logged with the flow identifiers (entity id, job/run id, correlation id).
- [ ] L2 — Key decisions and branches logged (why a path was taken, counts, skipped items).
- [ ] L3 — Every external call (HTTP, database, broker, cloud SDK) logged with target and elapsed time.
- [ ] L4 — Outcome logged (success, counts, elapsed time).
- [ ] L5 — Every failure path logs the exception with the same context; no empty `catch`/swallowed errors.
- [ ] L6 — Structured placeholders only (no interpolation/concatenation); deliberate levels.
- [ ] L7 — No secrets or PII in any log field (S6 in `Governance/security.md`).
- [ ] L8 — Correlation/trace id propagated across calls (OpenTelemetry when adopted).

Automated support: `harness.check --diff <base>` flags interpolated logs, sensitive values in log calls and orchestrators without a logger. Record L1–L8 in the run `log.md`.

## Git / PR

- Branching:
- Commit message:
- Minimum PR checklist:

## Dependencies

- How to add packages: **ask** (`Governance/permissions.md`)
- Vendors / libs: **OSS first** (`Governance/cost.md`); proprietary cloud only with an ADR
- Approved vendors / libs (if any):

## Rich domain model (always — mandatory)

Applies to every stack and style: business rules, invariants and state transitions live in domain entities and value objects, exposed through intention-revealing methods (`order.Cancel(reason)`, not `order.Status = Cancelled`). Handlers, services, controllers and repositories orchestrate only.


- State changes only through domain methods/factories; Application/API does not set internal fields.
- Value Objects for concepts with invariants; explicit domain exceptions.
- DDD with rich domains: business rules, validations and behavior are encapsulated in aggregates, entities and value objects; one aggregate root per consistency boundary.
- Never mock Entities/Value Objects in domain tests — use real instances.
- Mock only the edges (see [Test quality](#test-quality)).

## Code documentation

Native format of the stack (XML doc, KDoc, JSDoc/TSDoc, dartdoc, docstrings…). Format details: the active [stack pack](./stacks/readme.md).

- Always in **English**. Logs found during the documentation pass are translated to English.
- When documenting: **replace** the existing docs and document the **whole file** — fields, properties, constructors, methods and enums/values.
- Every public **and** private member has a **summary** and **remarks** (domain context, usage, constraints or behavior) — remarks are never empty nor a repeat of the summary.
  - **Exception (conservative):** simple, self-explanatory properties (optional filter flags, optional primitive fields) whose summary is already complete may omit the remarks.
- Concise and direct: short sentences, no long paragraphs; at most 1–2 examples per section.
- Remove documentation comments inside method bodies.
- Parity: when a type implements an interface/contract, the docs of each member (summary, remarks, parameters, return, responses) are **identical** in both.
- Strict consistency: follow the pattern already in the code as the template; do not invent formats. **Do not hallucinate** constraints, examples or behaviors — only what is in the code or the known domain.
- A request to document/refactor docs = rewrite of the **whole file**; no partial edits nor old docs mixed in.
- Namespaces/packages/modules reflect the physical path relative to the project, whenever the stack allows.
- In docs-only passes: apply [Code preservation](#code-preservation-mandatory).

### Documentation delivery (Definition of Done)

- Every implementation delivers: code docs on all new or changed members **and** updates to the affected Markdown pages in `docs/` (API, workers, architecture, development…), keeping the style of the existing pages.
- An implementation is **not done** without the documentation delivered.

## Acceptance taxonomy

| ID | Meaning |
|----|---------|
| AC-T\* | Existing automated test |
| AC-P\* | Process (spec, governance, feature folder) |
| AC-G\* | Gap — stub in the feature folder + regenerate acceptance |

## Stack packs

Language/framework-specific rules live in [stacks/](./stacks/readme.md) — the agent reads **only** the active pack (recorded in [Agents/project.md](../Agents/project.md)). The baseline above applies to any stack.

## Languages

| Layer | Language |
|-------|----------|
| Harness (`.ai-harness/`), specs, ADRs, adapters | English |
| Code: identifiers, code docs, log messages, test names | English |
| Product docs (`docs/`) | the language the project already uses |

## Docs

- Where product/design documentation lives:
- Languages: see [Languages](#languages)
