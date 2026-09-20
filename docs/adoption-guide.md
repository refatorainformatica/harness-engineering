# Guia de Adoção — AI Engineering Harness

## 1. Bootstrap

```bash
./scripts/init-harness.sh /caminho/projeto MeuApp --adapters=cursor,copilot,claude
```

Instala `.ai-harness/` + adapters escolhidos + gitignore de runs.

## 2. Preencher Knowledge (obrigatório)

Manualmente ou em lote:

```bash
# Preenche Knowledge, Tools, Governance e INDEX a partir do README/estrutura
python3 /caminho/harness-engineering/scripts/fill-harness.py /caminho/projeto

# Todos os repos com .ai-harness/ sob Refatora
python3 /caminho/harness-engineering/scripts/fill-harness.py
```

Após o bootstrap, rode a cadeia de preenchimento:

```bash
python3 /caminho/harness-engineering/scripts/fill-harness.py /caminho/projeto
python3 /caminho/harness-engineering/scripts/deep-fill-harness.py /caminho/projeto
python3 /caminho/harness-engineering/scripts/enrich-harness.py /caminho/projeto   # 2º enriquecimento
```

| Script | Faz |
|--------|-----|
| `fill-harness.py` | Knowledge/Tools/INDEX + overlay de stack (não apaga regras canônicas) |
| `deep-fill-harness.py` | Specs + **acceptance = testes unitários** |
| `enrich-harness.py` | ADR, glossário, use-cases, overlay Governance, `Agents/project.md`, stubs AC-G* na pasta da feature |

Regras canônicas da frota: [rules-baseline.md](./rules-baseline.md). `fill`/`enrich` **não** substituem Agents, Workflows nem a baseline de Governance.

Revise ADR e glossário — ainda pedem curadoria humana pontual.

| Arquivo | Conteúdo |
|---------|----------|
| `Knowledge/Architecture.md` | Estilo e pastas reais |
| `Knowledge/Domain.md` | Glossário, contextos, criticidade |
| `Knowledge/Standards.md` | Código, testes, git, deps |
| `Knowledge/ADR/` | Decisões duradouras |

## 3. Governance + Tools

- `Governance/*` — security, quality, architecture, cost, permissions
- `Tools/*` — comandos reais da stack (remova o que não usa)

## 4. Primeiras features

1. Copiar `Specification/templates/` → `features/<id>/`
2. Registrar em `features/INDEX.md`
3. Remover `features/example`
4. Rodar workflow `Workflows/feature.md`

## 5. Validar com qualquer agente

> Leia `.ai-harness/AGENTS.md`. Qual workflow e papel usaria para a feature X?

Esperado: citar Runtime, Specification, Agents e permissions.

## Operação

| Evento | Caminho |
|--------|---------|
| Nova feature | `Workflows/feature.md` |
| Bug | `Workflows/bug.md` |
| Refactor | `Workflows/refactoring.md` |
| Migration | `Workflows/migration.md` |
| Decisão arquitetural | `Knowledge/ADR/` + Architect |

## Anti-padrões

- Harness vazio (Knowledge nunca preenchido)
- Tools com stack fantasma
- Implementar sem acceptance
- Agent “faz-tudo” sem declarar papel
- Commit/push sem `ask`
