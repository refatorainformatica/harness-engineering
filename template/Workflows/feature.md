# Workflow — Feature

Entregar uma capacidade nova ou evolução planejada.

## Passos

1. Run (`Runtime/RUN.md`) + CONTEXT (feature id, gates).
2. Se feature nova: copiar `Specification/templates/*` → `features/<id>/` e registrar no INDEX.
3. **Architect** (se desenho/API/limites novos) → ADR se preciso.
4. **Developer** implementa conforme requirements/use-cases.
5. **Tester** prova acceptance.
6. **Reviewer** valida diff + Governance.
7. Loop até DONE; commit só com `ask`.

## DoR

- [ ] Requirements + use-cases + acceptance preenchidos
- [ ] Knowledge relevante lido
- [ ] Permissions compreendidas

## DoD

- [ ] AC marcados ou justificados
- [ ] INDEX/status atualizados
- [ ] Sem ação deny
- [ ] STATUS = DONE
