# Governance — Security

## Regras base

- Não commitutar secrets, credentials, keystores ou service accounts.
- Não logar tokens, PII ou payloads sensíveis.
- Respeitar classificação de dados da organização.
- Dependências novas: avaliar CVE / licença antes do merge.
- Arquivos locais de config (`.env`, `appsettings`, `dart_defines`, service accounts) permanecem gitignored.

## Secrets (padrão)

| Tipo | Onde (esperado) | Git |
|------|-----------------|-----|
| Env / defines | `.env`, config local | gitignored |
| Cloud keys | service accounts / defines | gitignored |
| Tokens CI | secrets do provedor CI | fora do repo |

## IA

- Prompts não incluem dados sensíveis de produção sem autorização.
- Modelos externos: preferir OSS/local; cloud proprietário só com gap documentado (ADR + `Governance/cost.md`).
- Guardrails de entrada/saída quando a feature usar modelo.
- Decisões críticas com aprovação humana (`ask`).
- Humano aprova commit/push/release (`ask`).

## Dados sensíveis (quando o domínio exigir)

- Dados clínicos, financeiros ou PII só conforme a classificação do produto.
- Nunca texto plano em remoto se a spec exigir criptografia (blobs/E2E).
- Não inferir “dado clínico” só porque o repo usa Firestore ou e2e.

## Projeto

- …
