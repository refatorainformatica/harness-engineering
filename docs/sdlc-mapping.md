# Mapeamento SDLC + IA ↔ AI Engineering Harness

Adapte nomes de fases/gates ao modelo da sua empresa.

| Fase | Gate (ex.) | Harness | Evidência |
|------|------------|---------|-----------|
| Descoberta | G1 | `Knowledge/Domain.md` | Criticidade no CONTEXT |
| Arquitetura | G2 | Knowledge/Architecture + ADR | Specs `planned` |
| Construção | G3 | Workflows + Agents Developer/Tester | Runs VERIFY no LOG |
| Validação | G4 | Acceptance + Agent Reviewer | AC marcados; riscos no STATUS |
| Release | G5 | Governance + permissions `ask` | Rollback conforme processo |
| Evolução | G6 | INDEX + ADR review | Specs `stable`/`partial` |

## Controles de IA

| Controle | Onde |
|----------|------|
| Humano responsável | permissions `ask` |
| Modelo / dados | Spec + Knowledge/Standards + security |
| Guardrails / fallback | Specification + Governance/security |
| Sem secrets em prompt | permissions deny + security |
| Custo de tokens/cloud | Governance/cost.md |

## DoR / DoD

**Ready:** acceptance claro, Knowledge lido, workflow escolhido, run em PLAN.  
**Done:** AC OK, gates OK, sem deny, STATUS=DONE, specs/ADR atualizados se preciso.
