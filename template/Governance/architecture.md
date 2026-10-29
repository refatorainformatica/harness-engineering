# Governance — Architecture

## Baseline rules

- Follow `Knowledge/architecture.md` and `standards.md`.
- **Feature-first organization (mandatory):** new code and tests per business capability (`Features/<Name>/`, `lib/features/<id>/`, `test/features/<id>/`, …). Legacy code migrates when touched. See `standards.md`.
- Structural change → ADR in `Knowledge/ADR/`.
- Do not introduce a new layer/pattern without Architect + acceptance.
- OSS preference for deps and infra (`Governance/cost.md`). Proprietary cloud only with an ADR.

## Rich domain model (always — mandatory)

- State changes only through domain methods and factories; Application/API does **not** set internal fields.
- Value Objects for concepts with invariants; explicit domain exceptions.
- Repositories: interfaces in Domain; persistence in Infrastructure.
- Never an anemic domain (DTO with setters and logic in Application).
- DDD: rules and validations inside aggregates, entities and value objects; Bounded Contexts are not coupled through shared domain models.

## Gates

- [ ] Aligned with the documented style
- [ ] Code and tests in the feature folder
- [ ] ADR when applicable (includes proprietary cloud)
- [ ] No forbidden coupling (list below)

## Forbidden coupling / imports

- A feature's business logic outside the feature folder (e.g. shared helpers with feature rules)
- Application/API setting the internal state of a domain entity
- …
