# Tools — Validation

| ID | Ação | Notas |
|----|------|-------|
| `lint` | linter / analyze nos tocados | auto |
| `typecheck` | typecheck / compile dry | auto |
| `security.scan` | SAST / dep scan do projeto | **ask** se pesado ou publicar relatório |
| `harness.spec.read` | Ler `.ai-harness/**` | auto |
| `harness.spec.write` | Atualizar Specification/Knowledge | auto se comportamento/decisão mudou |
| `harness.state.write` | Escrever Runtime/state | auto |

Adicione gates da empresa (policy-as-code, contract tests, etc.) com IDs estáveis.
