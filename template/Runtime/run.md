# Runtime — Iniciar uma run

## Quando criar

Toda tarefa que altere código ou specs deve ter uma run em `.ai-harness/Runtime/state/runs/`.

## Passos

1. `run-id`: `YYYYMMDD-HHMM-<slug>`
2. Criar pasta com STATUS, CONTEXT, CHECKLIST, LOG (templates em `state/templates/`).
3. Escolher Workflow + papel inicial (Agents).
4. Ler Specification + Knowledge + permissions.
5. Entrar no LOOP: `INIT` → `PLAN`.

## CONTEXT (mínimo)

- Pedido do usuário
- Branch
- Workflow (`feature` \| `bug` \| `refactoring` \| `migration`)
- Feature id(s)
- Papel ativo
- Gates / criticidade
- Isolamento: raiz ou sandbox

## Encerrar

- `DONE` — checklist + resumo no LOG
- `BLOCKED` / `FAILED` — motivo claro no STATUS
