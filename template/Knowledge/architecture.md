# Architecture — {{PROJECT}}

> Fill in on adoption.

## Style

<!-- Clean Architecture, hexagonal, modular monolith, microservices, … -->

**Feature-first (mandatory):** code and test folders follow the business capability. Technical layers live **inside** the feature. See `standards.md`.

**OSS-first:** deps and infra in the order open source → self-host → proprietary cloud (ADR). See `Governance/cost.md`.

**Rich domain (always):** behavior lives in entities/value objects; the application layer only orchestrates. See `standards.md`.

```text
{{code-root}}/
├── features/<id>/          # or Features/<Name>/
│   ├── …                   # feature layers
│   └── …
└── …
```

## Layers / modules

```text
features/<id>/
├── …                       # domain / application / data / presentation — per the stack
└── …
```

Tests mirror the feature: `tests/.../Features/<id>/` or `test/features/<id>/`.

## Cross-cutting

| Piece | Role |
|-------|------|
| DI | … |
| Auth / tenancy | … |
| Messaging | … |
| Observability | … |

## Harness ↔ code mapping

| Spec feature | Code |
|--------------|------|
| `Specification/features/<id>/` | `{{path}}/<id>/` |

## Out of architectural scope (current)

- …
