# Acceptance Criteria — <id>

> **Fonte da verdade:** testes unitários do repositório/solução. Cada AC-Txx = um teste existente.

## Comando de validação (escopo)

```bash
# Ex.: dotnet test … --filter FullyQualifiedName~Features.<Name>
# Ex.: flutter test test/features/<id>/
```

## Critérios (= testes existentes)

- [ ] AC-T01 — `Features/<FeatureName>/…` ou `test/features/<id>/…` :: nome do teste
- [ ] AC-P01 — Use cases coerentes com os testes acima
- [ ] AC-P02 — Sem violação de Knowledge / Governance
- [ ] AC-P03 — Testes na pasta da feature (`Standards.md`)

## Evidências

| AC | Teste | Arquivo | Comando | Resultado |
|----|-------|---------|---------|-----------|
| AC-T01 | … | `…` | `…` | pending |

## Lacunas (AC-G*)

- Comportamento sem teste automatizado → **AC-Gxx** + stub mínimo **na pasta da feature**; regenerar este arquivo.
- DoD de feature: AC-T\* verdes **ou** AC-G\* justificado + stub criado.
- Não marcar DONE só com AC-P\* de processo.
