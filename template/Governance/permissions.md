# Governance — Permissions

Níveis:

| Nível | Significado |
|-------|-------------|
| **auto** | Agente executa sem pedir |
| **ask** | Só com pedido explícito nesta mensagem/tarefa |
| **deny** | Nunca |

## Matriz

| Ação | Nível | Observação |
|------|-------|------------|
| Ler código / Knowledge / Specification | auto | |
| Editar código no escopo | auto | |
| Build / test / lint no escopo | auto | |
| Atualizar Specification / ADR quando mudou | auto | |
| Escrever Runtime/state | auto | |
| Sandbox worktree | ask | Exceto se a tarefa pedir isolamento |
| `git commit` / `git push` | ask | |
| Adicionar dependências | ask | |
| Deploy / release / produção | ask | Alto impacto: confirmação reforçada |
| Apagar arquivos de produto | ask | |
| Force push / reset --hard / secrets | deny | |
| Upgrade global de toolchain | deny | |
| `--no-verify` | deny | |

## Decisão

1. Fora de `Tools/` → deny ou ask.
2. Dúvida auto vs ask → **ask**.
3. Pedido do usuário sobrescreve **ask** nesta tarefa.
4. Pedido **não** sobrescreve **deny** sem confirmação reforçada + justificativa.
5. IA de alto impacto → mais `ask` em modelo, dados e guardrails.
