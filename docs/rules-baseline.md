# Baseline de regras (consolidado da frota)

Regras canônicas extraídas dos harness implantados nos repositórios Refatora (Flow, Flow-1.0, RadzenCRM, dotr*, fato-ou-fake, felipe360, design-patterns, sldc-ia, documentation-instructions, etc.) e promovidas para o template deste kit.

O que era **específico de produto** (paths .NET, tabela GCP do FatoOuFake, dados clínicos) **não** entra aqui.

## Obrigatórias (todo projeto)

| Regra | Onde |
|-------|------|
| Feature-first: código e testes na pasta da feature; legado migra ao ser tocado | `template/Knowledge/Standards.md` |
| OSS-first: open source → self-host → cloud proprietário só com ADR | `template/Governance/cost.md` |
| Aceite = **AC-T\*** (teste) ou **AC-G\*** (lacuna + stub na pasta da feature) | `Agents/tester.md`, `Workflows/feature.md`, `Specification/templates/acceptance.md` |
| Secrets / keystores / service accounts nunca no git; PII fora de logs | `template/Governance/security.md` |
| Commit/push/`--no-verify`/force-push conforme matriz | `Governance/permissions.md`, `Tools/git.md` |
| Não expandir escopo para desbloquear; ~12 iterações/run | `Runtime/LOOP.md`, `Agents/developer.md` |
| Tools usam `auto` / `ask` / `deny` (não “OK”) | `Tools/*.md` |

## Condicionais

| Quando | Regra | Onde |
|--------|-------|------|
| DDD / Clean Architecture | Domínio rico; Application não seta campos internos; não mockar Entities/VOs | `Governance/architecture.md`, `Knowledge/Standards.md`, adapter `rich-domain.mdc` |
| Feature de IA | Prompts sem dados de produção; modelos OSS/local primeiro | `Governance/security.md`, `cost.md` |
| .NET + XML docs | Docs em inglês; parity interface/implementação; passe só-docs não muda lógica | `Knowledge/Standards.md` |
| Docker | Não subir compose completo só para unit test | `Governance/cost.md` |

## Adapters Cursor

`init-harness.sh --adapters=cursor` copia todos os `.mdc`:

- `harness-sdd.mdc` — protocolo (always)
- `opensource-first.mdc` — OSS (always)
- `rich-domain.mdc` — DDD (globs `*.cs` / `*.dart`)

## O que o fill/enrich **não** pode apagar

A partir desta consolidação, `fill-harness.py` e `enrich-harness.py` **mesclam** overlays `<!-- HARNESS:PROJECT-* -->` e gravam `Agents/project.md`. Não substituem Agents, Workflows nem a baseline de Governance.

## Explicitamente fora da baseline

- EXECUTION-FIRST / auto-approve de `documentation-instructions` (conflita com `permissions.md`)
- Heurística “dados clínicos porque tem Firestore”
- Comandos e paths de um único repo
- SDLC/RACI corporativo de `sldc-ia` (já mapeado em `docs/sdlc-mapping.md`)
