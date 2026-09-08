# Workflow — Refactoring

Melhorar estrutura **sem** mudar comportamento observável (salvo aceite explícito).

## Passos

1. Run + CONTEXT (motivação, área, métrica de sucesso).
2. Architect: limites do refactor; ADR se mudar estilo/padrão.
3. Capturar baseline de testes (Tester) **antes**.
4. Developer: mudanças internas; sem alterar acceptance de features.
5. Tester: mesma suíte verde; sem novos comportamentos.
6. Reviewer: confirmar “behavior-preserving”.

## DoR

- [ ] Motivação e limites claros
- [ ] Suíte de segurança (testes) identificada

## DoD

- [ ] Comportamento externo inalterado
- [ ] Testes relevantes passando
- [ ] STATUS = DONE
