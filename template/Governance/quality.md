# Governance — Quality

## Regras base

- Sem issues **novos** de lint/analyze nos arquivos tocados (salvo acordo explícito).
- Regras de negócio novas com testes proporcionais ao risco.
- Sem expandir escopo para “melhorar qualidade” fora do aceite.
- Aceite = testes: **AC-T\*** verdes, **ou** **AC-G\*** justificado + stub na pasta da feature.

## Testes

- Novos testes **sempre** na pasta da feature (`Knowledge/Standards.md`).
- Nunca mockar Entities / Value Objects de domínio — instâncias reais.
- Mockar só bordas (repositórios, HTTP, clock, filesystem, brokers).
- Naming sugerido: `MethodName_ShouldExpectedBehavior_WhenCondition`.

## Gates sugeridos (ajuste à empresa)

- [ ] Build verde no escopo
- [ ] Testes da feature / regressão (AC-T\* ou AC-G\* + stub)
- [ ] Lint/analyze nos tocados
- [ ] Review humano antes de merge (MATRIX)

## Cobertura (se a empresa definir)

- Alvo típico de domínio: **80% line** por artefato — cobertura significativa, não inflação.
- Prioridade: Domain → Application → Infrastructure → API (só se houver regra de negócio).

## Projeto

- Cobertura mínima:
- Ferramentas obrigatórias:
