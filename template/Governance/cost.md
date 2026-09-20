# Governance — Cost

FinOps / custo de cloud, CI e tokens de IA. Consolidado a partir do uso do harness na frota de repositórios.

## Preferência OSS (obrigatório)

Ao propor dependência, modelo ou infra, **nesta ordem**:

1. Biblioteca/modelo open source (local ou self-hosted)
2. API/serviço OSS auto-hospedado (Docker/K8s)
3. Cloud proprietário **somente** com ADR motivando o gap (não conveniência)

Checklist: dá para fazer com OSS? Se sim, faça com OSS. Cloud pago só com gap real documentado.

## Regras base

- Evitar upgrades de SKU/planos cloud sem `ask`.
- Preferir free tier / self-host enquanto couber.
- Evitar jobs/pipelines caros em loop de agente sem necessidade.
- Verificação mínima (testes da feature/run) — não a suíte monólito a cada iteração.
- Não subir stack compose completa só para um teste unitário.
- Uso de modelos/APIs pagas: só no escopo autorizado; preferir local (ex.: Ollama).
- Máx. ~12 iterações/run (ver `Runtime/LOOP.md`); evitar rebuilds caros em loop.

## Limites (empresa)

| Recurso | Política |
|---------|----------|
| Cloud SKU | sem upgrade sem `ask`; preferir free tier / self-host |
| CI / build | testes do escopo da feature/run |
| Tokens LLM | local primeiro; API paga só com autorização |
| Containers | compose completo não é pré-requisito de unit test |
| Agente | ~12 iterações/run; BLOCKED com resumo se estourar |

## Projeto

- …
