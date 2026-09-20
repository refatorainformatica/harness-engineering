# Workflow — Bug

Corrigir defeito com reprodução e regressão controlada.

## Passos

1. Run + CONTEXT (sintoma, severidade, feature id se conhecida).
2. Reproduzir (Tester/Developer) — evidência no LOG.
3. Se causa for arquitetural → Architect; senão Developer no menor fix **na pasta da feature**.
4. Tester: teste de regressão que falharia antes / passa depois (criar se **AC-G\***).
5. Reviewer: escopo mínimo, sem “refactor de carona”.
6. DONE com link ao sintoma original.

## DoR

- [ ] Sintoma claro e passos de reprodução
- [ ] Impacto / severidade estimados

## DoD

- [ ] Fix no escopo
- [ ] Teste de regressão existe (criar se AC-G\*) na pasta da feature
- [ ] STATUS = DONE
