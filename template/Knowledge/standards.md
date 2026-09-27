# Standards — {{PROJECT}}

Padrões de engenharia da empresa/projeto. Complementa [Governance/](../Governance/).

## Código

- Linguagem / versão:
- Estilo / formatter:
- Naming:
- Comentários / docs de API:

## Organização por feature (obrigatório)

Código **sempre** organizado por feature (capacidade de negócio). A feature é o eixo principal de pastas; a camada técnica é subordinada.

| Onde | Como |
|------|------|
| Specs | `Specification/features/<id>/` |
| Código de aplicação | pastas/módulos por feature (ex.: `Features/<Name>/`, `lib/features/<id>/`, `src/features/<id>/`) |
| Camadas (domain/data/api/…) | **dentro** da feature, não o contrário |
| Shared / core | só cross-cutting real (DI, Result, logging, router). Sem lógica de negócio de uma feature |

### Regras de aplicação

- Código **novo** nasce feature-first. Código legado migra **ao ser tocado**.
- Proibido `Common` / `Utils` / `Helpers` / `Entities` / `Models` genéricos para lógica de uma feature — coloque na feature.
- Spec ↔ código: cada comportamento novo mapeia para uma feature em `Specification/features/<id>/`.
- Reviewer / Developer: rejeitar diffs que introduzam pastas técnicas genéricas no lugar de feature.

Ajuste os paths concretos em [Architecture.md](./Architecture.md).

## Testes

- Pirâmide (unit / integration / e2e):
- Frameworks:
- Cobertura mínima (se houver):

### Organização por feature (obrigatório)

Testes **sempre** criados e guardados **por feature**, espelhando o código e a spec.

| Camada | Path (exemplos — adaptar ao stack) |
|--------|-------------------------------------|
| Backend / API | `tests/.../Features/<FeatureName>/…` |
| Frontend / mobile | `test/features/<id>/…` ou `__tests__/features/<id>/…` |
| Spec / AC | Cada AC-T\* aponta para um teste sob a pasta da feature |

- Fixtures partilhadas (containers, factories de app) ficam em `Shared/` — **não** misturar testes de feature aí.
- Testes de peças cross-cutting → `Features/Common/` ou `Shared/` com nome explícito.
- Teste **novo** nasce sob a feature. Testes legados na raiz migram **ao serem tocados**.
- Proibido criar testes soltos na raiz do projeto de testes quando a feature existe.

### Nomenclatura (sugerida)

- Classe: `{ClassName}Tests`
- Método: `MethodName_ShouldExpectedBehavior_WhenCondition`
- Arquivo (Dart/JS): `{subject}_test.dart` / `{subject}.test.ts` dentro da pasta da feature

## Git / PR

- Branching:
- Mensagem de commit:
- Checklist mínimo de PR:

## Dependências

- Como adicionar pacotes: **ask** (`Governance/permissions.md`)
- Vendors / libs: **OSS primeiro** (`Governance/cost.md`); cloud proprietário só com ADR
- Vendors / libs aprovadas (se houver):

## Domínio rico (quando DDD / Clean Architecture)

- Estado muda só via métodos/factories de domínio; Application/API não seta campos internos.
- Value Objects para conceitos com invariantes; exceções de domínio explícitas.
- Nunca mockar Entities/Value Objects em testes de domínio — instâncias reais.
- Mockar só bordas: repositórios, DbContext, HTTP, brokers, filesystem, relógio.

## Documentação XML (.NET, se aplicável)

- XML docs em **inglês** (`summary` + `remarks` com contexto de domínio).
- Parity: interface e implementação com a mesma documentação de membro.
- Em passes só-de-docs: não alterar lógica nem remover attributes.
- Logs de produto em inglês quando o projeto já adota esse padrão.

## Taxonomia de aceite

| ID | Significado |
|----|-------------|
| AC-T\* | Teste automatizado existente |
| AC-P\* | Processo (spec, governance, pasta da feature) |
| AC-G\* | Lacuna — stub na pasta da feature + regenerar acceptance |

## Docs

- Onde vive documentação de produto/design:
- Idioma das specs: português (kit); XML de código .NET em inglês
