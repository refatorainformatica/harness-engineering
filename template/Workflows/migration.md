# Workflow — Migration

Mudança estrutural de dados, plataforma, dependência major ou cutover.

## Passos

1. Run + CONTEXT (origem → destino, downtime, rollback).
2. **Architect** obrigatório: plano, ADR, impacto Cost/Security.
3. Spec de migração em `Specification/features/<id>/` (ou feature `migrate-*`).
4. Developer: scripts/código de migração + dual-write/read se necessário.
5. Tester: dry-run, validação de dados, rollback testado.
6. Reviewer + Governance (security, cost, architecture).
7. Execução em produção = sempre `ask` (e processo da empresa).

## DoR

- [ ] ADR aceito (ou decisão humana registrada)
- [ ] Plano de rollback
- [ ] Janela / owners definidos

## DoD

- [ ] Dry-run evidenciado
- [ ] Rollback testado ou aceito formalmente
- [ ] STATUS = DONE (ou BLOCKED aguardando go-live humano)
