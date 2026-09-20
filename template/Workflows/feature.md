# Workflow — Feature

Entregar uma capacidade nova ou evolução planejada.

## Passos

1. Run (`Runtime/RUN.md`) + CONTEXT (feature id, gates).
2. Se feature nova: copiar `Specification/templates/*` → `features/<id>/` e registrar no INDEX.
3. **Architect** (se desenho/API/limites novos) → ADR se preciso (obrigatório se cloud proprietário).
4. **Developer** implementa conforme requirements/use-cases **na pasta da feature**.
5. **Tester** prova acceptance (**AC-T\***; **AC-G\*** → stub).
6. **Reviewer** valida diff + Governance.
7. Loop até DONE; commit só com `ask`.

## DoR

- [ ] Requirements + use-cases + acceptance preenchidos
- [ ] Knowledge relevante lido
- [ ] Permissions compreendidas
- [ ] Paths em `Agents/project.md` conferidos

## DoD

- [ ] AC-T\* verdes **ou** AC-G\* justificado + stub criado na pasta da feature
- [ ] Código e testes na pasta da feature
- [ ] INDEX/status atualizados
- [ ] Sem ação deny
- [ ] STATUS = DONE
