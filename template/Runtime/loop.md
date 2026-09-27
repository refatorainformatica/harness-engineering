# Runtime — Loop

## Estados

| Estado | Significado |
|--------|-------------|
| `INIT` | Run criada |
| `PLAN` | Plano no state |
| `ACT` | Implementando (Developer) / decidindo (Architect) |
| `VERIFY` | Tester / validation |
| `REVIEW` | Reviewer |
| `UPDATE_SPEC` | Specification/ADR alinhados |
| `DONE` | Aceite OK |
| `BLOCKED` | Precisa do usuário |
| `FAILED` | Gate falhou sem fix seguro no escopo |

## Loop

```
while state not in {DONE, BLOCKED, FAILED}:
  1. Ler STATUS.md
  2. Próximo item do CHECKLIST
  3. Uma unidade de trabalho (tool permitida / papel ativo)
  4. Registrar no LOG (tool ID + papel)
  5. Verificar se código mudou
  6. Atualizar CHECKLIST + STATUS
  7. Aceite OK → DONE; ask → BLOCKED; erro sem fix → FAILED
```

## DONE

1. Escopo cumprido  
2. Acceptance marcado ou justificado  
3. Gates pedidos passaram  
4. Nenhuma ação deny  
5. STATUS = DONE  

## BLOCKED

- ask sem autorização  
- Spec ambígua / conflito com Knowledge  
- WIP misturado sem sandbox  

## Anti-loop

- Máx. ~12 iterações → BLOCKED com resumo  
- Mesmo comando falho > 2 vezes → mudar abordagem  
- Não expandir escopo para desbloquear  

## Relação com o IDE

Continuar passos `auto` sem pedir “pode seguir”; parar só em ask/ambiguidade. Indicar `run-id` e estado.
