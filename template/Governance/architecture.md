# Governance — Architecture

## Regras base

- Seguir `Knowledge/Architecture.md` e `Standards.md`.
- **Organização por feature (obrigatório):** código e testes novos por capacidade de negócio (`Features/<Name>/`, `lib/features/<id>/`, `test/features/<id>/`, …). Legado migra ao ser tocado. Ver `Standards.md`.
- Mudança estrutural → ADR em `Knowledge/ADR/`.
- Não introduzir camada/padrão novo sem Architect + aceite.
- Preferência OSS para deps e infra (`Governance/cost.md`). Cloud proprietário só com ADR.

## Domínio rico (quando o estilo for DDD / Clean Architecture)

- Estado muda só via métodos e factories de domínio; Application/API **não** seta campos internos.
- Value Objects para conceitos com invariantes; exceções de domínio explícitas.
- Repositórios: interfaces no Domain; persistência na Infrastructure.
- Nunca domínio anêmico (DTO com setters e lógica na Application).

## Gates

- [ ] Alinhado ao estilo documentado
- [ ] Código e testes na pasta da feature
- [ ] ADR quando aplicável (inclui cloud proprietário)
- [ ] Sem acoplamento proibido (listar abaixo)

## Acoplamentos / imports proibidos

- Lógica de negócio de uma feature fora da pasta da feature (ex.: helpers compartilhados com regras de feature)
- Application/API setando estado interno de entidade de domínio
- …
