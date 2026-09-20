# Architecture — {{PROJECT}}

> Preencher na adoção.

## Estilo

<!-- Clean Architecture, hexagonal, modular monolith, microservices, … -->

**Feature-first (obrigatório):** pastas de código e de teste seguem a capacidade de negócio. Camadas técnicas ficam **dentro** da feature. Ver `Standards.md`.

**OSS-first:** deps e infra na ordem open source → self-host → cloud proprietário (ADR). Ver `Governance/cost.md`.

**Domínio rico** se o estilo for DDD/Clean Architecture: comportamento nas entidades; Application só orquestra. Ver `Standards.md`.

```text
{{raiz-do-codigo}}/
├── features/<id>/          # ou Features/<Name>/
│   ├── …                   # camadas da feature
│   └── …
└── …
```

## Camadas / módulos

```text
features/<id>/
├── …                       # domain / application / data / presentation — conforme o stack
└── …
```

Testes espelham a feature: `tests/.../Features/<id>/` ou `test/features/<id>/`.

## Cross-cutting

| Peça | Papel |
|------|--------|
| DI | … |
| Auth / tenancy | … |
| Messaging | … |
| Observability | … |

## Relação harness ↔ código

| Spec feature | Código |
|--------------|--------|
| `Specification/features/<id>/` | `{{path}}/<id>/` |

## Fora de escopo arquitetural (atual)

- …
