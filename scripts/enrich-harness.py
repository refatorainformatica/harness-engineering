#!/usr/bin/env python3
"""
2º script de enriquecimento do .ai-harness/

Completa o que fill/deep-fill deixaram raso:
- ADR a partir de decisões reais (stack, estilo, integrações)
- Glossário de domínio a partir do código (entities, enums, features)
- Use cases derivados de testes + tipos públicos do código
- Governance security/cost específicos do projeto detectado
- Agents/Workflows customizados com paths e comandos do repo
- Stubs de teste para features com lacuna de coverage (AC-G*)

Uso:
  python3 enrich-harness.py [/caminho/repo ...]
  (sem args: todos os .ai-harness sob Refatora)
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


fill = load("fill_harness", SCRIPT_DIR / "fill-harness.py")
deep = load("deep_fill_harness", SCRIPT_DIR / "deep-fill-harness.py")

SKIP = fill.SKIP_DIRS | {"packages", "artifacts-local", ".ai-harness"}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


# ── Código → glossário / tipos ──────────────────────────────────────────────


def extract_csharp_domain(repo: Path) -> list[tuple[str, str, str]]:
    """(termo, kind, path)"""
    out: list[tuple[str, str, str]] = []
    patterns = [
        (r"\b(?:public\s+)?(?:sealed\s+)?(?:partial\s+)?class\s+(\w+)", "class"),
        (r"\b(?:public\s+)?(?:sealed\s+)?record\s+(\w+)", "record"),
        (r"\b(?:public\s+)?enum\s+(\w+)", "enum"),
        (r"\b(?:public\s+)?interface\s+I(\w+)", "interface"),
    ]
    for path in repo.rglob("*.cs"):
        if any(p in path.parts for p in SKIP):
            continue
        if "Tests" in path.parts or path.name.endswith("Tests.cs"):
            continue
        # prioriza Domain / Entities / ValueObjects / Features
        rel = str(path.relative_to(repo))
        weight = any(x in rel for x in ("Domain", "Entities", "ValueObjects", "Features", "Aggregates"))
        if not weight and "src/" not in rel and "Apis/" not in rel and "lib/" not in rel:
            continue
        text = read(path)
        for pat, kind in patterns:
            for m in re.finditer(pat, text):
                name = m.group(1)
                if name.startswith("_") or len(name) < 3:
                    continue
                if name.endswith("Tests") or name.endswith("Test"):
                    continue
                out.append((name, kind, rel))
    return out[:80]


def extract_dart_domain(repo: Path) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for path in repo.rglob("*.dart"):
        if any(p in path.parts for p in SKIP | {".dart_tool"}):
            continue
        if path.parts[0] == "test" or path.name.endswith("_test.dart"):
            continue
        rel = str(path.relative_to(repo))
        if not any(x in rel for x in ("domain", "entities", "models", "features", "core")):
            continue
        text = read(path)
        for m in re.finditer(r"\b(?:class|enum|typedef|mixin)\s+(\w+)", text):
            name = m.group(1)
            if name.startswith("_") or name.endswith("State") and "Bloc" in name:
                pass
            if len(name) < 3:
                continue
            kind = "class"
            if f"enum {name}" in text:
                kind = "enum"
            out.append((name, kind, rel))
    return out[:80]


def extract_docs_terms(repo: Path) -> list[tuple[str, str, str]]:
    out = []
    docs = repo / "docs"
    if not docs.is_dir():
        return out
    for path in docs.rglob("*.md"):
        stem = path.stem
        if stem.lower() in ("readme", "index", "template"):
            continue
        out.append((stem.replace("-", " ").title(), "doc", str(path.relative_to(repo))))
    return out[:40]


def build_glossary(repo: Path, stack: dict, features: list[tuple[str, str, str]]) -> str:
    rows: list[tuple[str, str, str]] = [
        ("Harness", "Estrutura `.ai-harness/` deste repositório", "—"),
        ("Feature", "Unidade em `Specification/features/<id>/`", "—"),
        ("Run", "Execução do agente em `Runtime/state/runs/`", "—"),
        ("Acceptance", "Critérios derivados de testes unitários (AC-T*)", "—"),
    ]
    seen = {r[0].lower() for r in rows}

    for fid, code, desc in features:
        if fid.lower() in seen:
            continue
        seen.add(fid.lower())
        rows.append((fid, desc[:120] or f"Módulo `{code}`", code))

    types = []
    if stack.get("dotnet"):
        types = extract_csharp_domain(repo)
    elif stack.get("flutter"):
        types = extract_dart_domain(repo)
    else:
        types = extract_docs_terms(repo)

    for name, kind, path in types:
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        rows.append((name, f"{kind} em `{path}`", path))
        if len(rows) >= 60:
            break

    table = "\n".join(f"| {t} | {m} | `{p}` |" for t, m, p in rows)
    return f"""# Domain — {repo.name}

> Glossário enriquecido em {date.today().isoformat()} a partir de features + código.

## Glossário

| Termo | Significado | Origem |
|-------|-------------|--------|
{table}

## Como manter

1. Novo conceito de domínio → linha neste glossário **na mesma PR**.
2. Mesmo identificador em SPEC, código e testes.
3. ADR se o termo implica trade-off arquitetural.
"""


# ── Use cases a partir de testes / código ───────────────────────────────────


def humanize_test_name(name: str) -> tuple[str, str, str]:
    """Converte nome de teste em Given/When/Then aproximado."""
    raw = name
    # snake/camel → espaços
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    s = s.replace("_", " ").strip()
    s = re.sub(r"\s+", " ", s)

    given = "o sistema está no estado inicial do teste"
    when = f"executa o cenário `{raw}`"
    then = f"o comportamento `{s}` é satisfeito"

    low = s.lower()
    if "should" in low:
        parts = re.split(r"\bshould\b", s, flags=re.I)
        when = parts[0].strip() or when
        then = ("should " + parts[1].strip()) if len(parts) > 1 else then
    if "emits" in low:
        then = s
        when = "o evento/ação do cenário é disparado"
    if "deve" in low or "fail" in low or "throw" in low or "falhar" in low:
        then = s
    if "given" in low or "quando" in low:
        given = s

    return given[:160], when[:160], then[:200]


def rewrite_use_cases(
    dest: Path,
    fid: str,
    tests: list,
    description: str,
) -> None:
    ucs = []
    if tests:
        for i, t in enumerate(tests[:12], 1):
            g, w, th = humanize_test_name(t.name)
            try:
                rel = t.rel_path if not Path(t.rel_path).is_absolute() else Path(t.rel_path).name
            except Exception:
                rel = t.file_name
            ucs.append(
                f"""## UC-{i:02d} — {t.name[:80]}

- **Actor:** sistema sob teste
- **Fonte:** `{rel}` ({t.kind})
- **Given** {g}
- **When** {w}
- **Then** {th}
"""
            )
    else:
        ucs.append(
            f"""## UC-01 — Comportamento principal de `{fid}`

- **Actor:** usuário / consumidor da API
- **Given** o módulo `{fid}` está disponível
- **When** a operação principal descrita em requirements é executada
- **Then** {description[:180] or "o resultado esperado na SPEC é obtido"}

## UC-02 — Lacuna de teste

- **Actor:** engenharia
- **Given** não há testes unitários mapeados para `{fid}`
- **When** a feature evolui
- **Then** um teste automatizado é adicionado e o acceptance é regenerado
"""
        )
    write(dest / "use-cases.md", f"# Use Cases — {fid}\n\n> Derivados de testes/código em {date.today().isoformat()}.\n\n" + "\n".join(ucs))


# ── ADR ─────────────────────────────────────────────────────────────────────


def detect_integrations(repo: Path, stack: dict, readme: str) -> list[str]:
    hits = []
    blob = readme.lower() + " " + " ".join(p.name.lower() for p in repo.iterdir())
    checks = [
        ("Firebase / Firestore", ["firebase", "firestore"]),
        ("Ollama (LLM local)", ["ollama"]),
        ("MongoDB", ["mongodb", "mongo"]),
        ("PostgreSQL", ["postgres", "postgresql"]),
        ("MySQL", ["mysql"]),
        ("Redis", ["redis"]),
        ("RabbitMQ", ["rabbitmq"]),
        ("Docker Compose", ["docker-compose", "compose"]),
        ("Semantic Kernel", ["semantic kernel", "semantickernel"]),
        ("MediatR-style / Mediator", ["dotrmediator", "imediator", "mediatr"]),
        ("Flutter", ["flutter", "pubspec"]),
        ("ASP.NET Core", ["aspnetcore", "asp.net", "microsoft.aspnetcore"]),
        ("Qdrant / FAISS", ["qdrant", "faiss"]),
        ("MinIO", ["minio"]),
        ("GCP / Terraform", ["terraform", "gcp", "vertex"]),
    ]
    text = blob
    # peek a few key files
    for f in list(repo.rglob("*.csproj"))[:5] + list(repo.rglob("pubspec.yaml"))[:1]:
        if any(p in f.parts for p in SKIP):
            continue
        text += " " + read(f).lower()[:2000]
    for label, kws in checks:
        if any(k in text for k in kws):
            hits.append(label)
    if stack.get("dotnet"):
        hits.append(".NET SDK / solution")
    if stack.get("flutter"):
        hits.append("Flutter / Dart")
    if stack.get("node"):
        hits.append("Node.js tooling")
    # unique preserve order
    seen = set()
    out = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


def write_adr(repo: Path, harness: Path, stack: dict, readme: str, arch_style: str) -> None:
    integrations = detect_integrations(repo, stack, readme)
    adr_dir = harness / "Knowledge" / "ADR"
    adr_path = adr_dir / "ADR-0001-baseline-architecture.md"

    alts = []
    if stack.get("dotnet"):
        alts = ["Monólito anêmico sem camadas", "Microserviços prematuros", "Mediator in-process vs gRPC"]
    elif stack.get("flutter"):
        alts = ["Online-only com API REST", "State management único global", "Sem criptografia E2E"]
    elif stack.get("docs_only"):
        alts = ["Wiki não versionada", "PDF único sem gates"]
    else:
        alts = ["Stack proprietária cloud-first", "Sem padronização de pastas"]

    write(
        adr_path,
        f"""# ADR-0001: Baseline architecture — {repo.name}

| Campo | Valor |
|-------|-------|
| Status | accepted |
| Data | {date.today().isoformat()} |
| Decisores | engineering (inferido do repositório) |

## Context

O repositório `{repo.name}` precisa de uma linha-base arquitetural explícita para agentes e humanos.
Decisões foram inferidas do código, README e dependências em {date.today().isoformat()}.

## Decision

- **Estilo:** {arch_style}
- **Integrações adotadas:** {', '.join(integrations) if integrations else 'ver README'}
- **Harness:** pasta `.ai-harness/` como contrato operacional (Specs + Agents + Governance)
- **Aceite:** critérios de aceitação amarrados a testes unitários existentes (`AC-T*`)

## Alternatives considered

{chr(10).join(f'{i}. {a}' for i, a in enumerate(alts, 1))}

## Consequences

### Positivas
- Agentes têm âncora clara (Knowledge + ADR)
- Mudanças estruturais exigem novo ADR
- Testes viram contrato de aceite

### Negativas / riscos
- ADR inferido pode precisar revisão humana
- Integrações listadas refletem o estado atual do código, não o roadmap

## Links

- `Knowledge/Architecture.md`
- `Knowledge/Domain.md`
- README.md
""",
    )

    write(
        adr_dir / "README.md",
        f"""# ADR — Architecture Decision Records

## Índice

| ID | Título | Status | Data |
|----|--------|--------|------|
| ADR-0001 | [Baseline architecture](./ADR-0001-baseline-architecture.md) | accepted | {date.today().isoformat()} |

## Quando criar

- Nova dependência significativa
- Mudança de estilo arquitetural
- Integração externa / vendor
- Trade-off de performance, segurança ou custo

## Template

Ver [template.md](./template.md).
""",
    )


# ── Governance ──────────────────────────────────────────────────────────────


def write_governance(repo: Path, harness: Path, stack: dict, integrations: list[str], readme: str) -> None:
    has_ai = any(x in " ".join(integrations).lower() for x in ("ollama", "llm", "semantic", "openai", "whisper", "ai"))
    has_cloud = any(x in " ".join(integrations).lower() for x in ("firebase", "gcp", "firestore", "aws", "azure"))
    has_secrets = any(
        (repo / p).exists()
        for p in (
            ".env",
            "config/dart_defines.json",
            "Apis/Application/appsettings.json",
            "Apis/Application/ServiceAccountKey.json",
        )
    )

    sec_rules = [
        "Não commitutar secrets, credentials, keystores ou service accounts.",
        "Não logar tokens, PII ou payloads sensíveis.",
        "Dependências novas: avaliar CVE / licença antes do merge.",
    ]
    if has_secrets or "firebase" in " ".join(integrations).lower():
        sec_rules.append("Arquivos locais de config (`dart_defines`, `appsettings`, service accounts) permanecem gitignored.")
    if has_ai:
        sec_rules.append("Prompts não podem incluir dados sensíveis de produção sem autorização.")
        sec_rules.append("Modelos externos: preferir OSS/local; cloud proprietário só com gap documentado (ADR).")
    if "firestore" in " ".join(integrations).lower() or "e2e" in readme.lower():
        sec_rules.append("Dados clínicos/sensíveis só como blobs criptografados — nunca texto plano no remoto.")
    if stack.get("dotnet"):
        sec_rules.append("Domain rico: estado muda via métodos de domínio; Application não seta campos internos.")

    write(
        harness / "Governance/security.md",
        f"""# Governance — Security ({repo.name})

> Específico do projeto — gerado em {date.today().isoformat()}.

## Regras

{chr(10).join('- ' + r for r in sec_rules)}

## Integrações sob controle

{chr(10).join('- ' + i for i in integrations) if integrations else '- Ver Knowledge/Architecture.md'}

## Secrets

| Tipo | Onde (esperado) | Git |
|------|-----------------|-----|
| Env / defines | `.env`, `config/*` local | gitignored |
| Cloud keys | service accounts / dart_defines | gitignored |
| Tokens CI | secrets do provedor CI | fora do repo |

## IA

- Humano aprova commit/push/release (`ask`)
- Decisões críticas com aprovação humana
{"- Guardrails de entrada/saída nas features de IA" if has_ai else "- Sem feature de IA detectada — revisar se isso mudar"}
""",
    )

    cost_rows = []
    if has_cloud:
        cost_rows.append("| Cloud (Firebase/GCP/etc.) | Preferir free tier / self-host; upgrade de SKU = **ask** |")
    if has_ai:
        cost_rows.append("| Tokens LLM | Preferir Ollama/local; APIs pagas só com autorização |")
    if stack.get("dotnet") or stack.get("flutter"):
        cost_rows.append("| CI / build | Rodar testes focados no escopo da feature, não a suíte inteira a cada iteração |")
    cost_rows.append("| Agente (loops) | Máx. ~12 iterações/run; evitar rebuilds caros em loop |")
    if "docker" in " ".join(integrations).lower():
        cost_rows.append("| Containers | Não subir stacks compose completas só para um teste unitário |")

    write(
        harness / "Governance/cost.md",
        f"""# Governance — Cost ({repo.name})

> FinOps / custo de compute e tokens — gerado em {date.today().isoformat()}.

## Políticas

{chr(10).join(cost_rows)}

## Preferência OSS

1. Biblioteca/modelo open source (local ou self-hosted)
2. API/serviço OSS auto-hospedado
3. Cloud proprietário **somente** com ADR motivando o gap

## Limites sugeridos (ajuste à empresa)

| Recurso | Política |
|---------|----------|
| Cloud SKU | sem upgrade sem `ask` |
| CI minutos | testes do escopo da run |
| Tokens LLM | local primeiro; pago com autorização |
""",
    )


# ── Agents / Workflows ──────────────────────────────────────────────────────


def write_agents_workflows(repo: Path, harness: Path, stack: dict) -> None:
    sln = fill.dotnet_solution(repo)
    if stack.get("flutter"):
        build_c = "flutter analyze && flutter test"
        test_c = "flutter test <path>"
        code_root = "lib/features/<id>"
    elif stack.get("dotnet"):
        build_c = f"dotnet build {sln}" if sln else "dotnet build"
        test_c = f"dotnet test {sln}" if sln else "dotnet test"
        code_root = "src/ ou Apis/Services/Features/"
    else:
        build_c = "ver README"
        test_c = "ver README"
        code_root = "."

    write(
        harness / "Agents/README.md",
        f"""# Agents — {repo.name}

Papéis customizados para este repositório.

| Papel | Arquivo | Foco neste projeto |
|-------|---------|-------------------|
| Architect | [architect.md](./architect.md) | ADR + `Knowledge/Architecture.md` |
| Developer | [developer.md](./developer.md) | Código em `{code_root}` |
| Reviewer | [reviewer.md](./reviewer.md) | Diff vs Governance + AC-T* |
| Tester | [tester.md](./tester.md) | `{test_c}` |

Build de referência: `{build_c}`
""",
    )

    write(
        harness / "Agents/developer.md",
        f"""# Agent — Developer ({repo.name})

## Missão

Implementar a Specification no código real deste repo.

## Paths canônicos

- Código: `{code_root}`
- Specs: `Specification/features/<id>/`
- Knowledge: `Knowledge/`

## Comandos (`auto`)

```bash
{build_c}
{test_c}
```

## Faz

- Editar só o escopo da feature/run
- Atualizar requirements/use-cases/acceptance se o comportamento mudou
- Rodar testes mapeados no `acceptance.md` (AC-T*)

## Não faz

- Commit/push sem `ask`
- Redesign sem Architect + ADR
- Expandir escopo para “desbloquear”

## Checklist

- [ ] SPEC lida
- [ ] Implementação
- [ ] `{test_c}` no escopo
- [ ] Handoff Tester/Reviewer
""",
    )

    write(
        harness / "Agents/tester.md",
        f"""# Agent — Tester ({repo.name})

## Missão

Provar os AC-T* do `acceptance.md` com os testes do repositório.

## Comando padrão

```bash
{test_c}
```

## Faz

- Mapear AC → arquivo de teste
- Rodar só o escopo da feature
- Registrar resultado na tabela de evidências do acceptance
- Se AC-G* (lacuna): criar stub/teste mínimo e regenerar acceptance

## Checklist

- [ ] AC-T* executados
- [ ] Falhas no LOG da run
- [ ] Handoff Reviewer
""",
    )

    write(
        harness / "Workflows/feature.md",
        f"""# Workflow — Feature ({repo.name})

1. Run (`Runtime/RUN.md`) — workflow=`feature`
2. Spec em `Specification/features/<id>/` (criar a partir de templates se nova)
3. Architect se mudar boundaries → ADR
4. Developer implementa em `{code_root}`
5. Tester: `{test_c}` conforme acceptance
6. Reviewer: Governance + Knowledge
7. DONE; commit só com `ask`

## DoR

- [ ] requirements + use-cases + acceptance
- [ ] Knowledge lido

## DoD

- [ ] AC-T* verdes (ou AC-G* justificado + stub criado)
- [ ] STATUS=DONE
""",
    )

    write(
        harness / "Workflows/bug.md",
        f"""# Workflow — Bug ({repo.name})

1. Reproduzir (teste falhando preferencialmente)
2. Fix mínimo no código (`{code_root}`)
3. Tester: regressão `{test_c}`
4. Reviewer: sem refactor de carona
5. DONE

## DoD

- [ ] Teste de regressão existe (criar se AC-G*)
- [ ] Fix no escopo
""",
    )


# ── Stubs de teste para lacunas ─────────────────────────────────────────────


def ensure_test_stubs(repo: Path, stack: dict, features: list[tuple[str, str, str]], test_map: dict) -> int:
    """Cria stubs mínimos para features sem testes. Retorna qtd criada."""
    created = 0
    for fid, code, desc in features:
        if test_map.get(fid):
            continue
        if fid in ("core",) and not stack.get("flutter") and not stack.get("dotnet"):
            # docs-only: não criar stubs de código
            continue

        if stack.get("flutter"):
            stub = repo / "test" / "features" / fid / f"{fid}_harness_gap_test.dart"
            if stub.exists():
                continue
            write(
                stub,
                f"""// Stub gerado pelo enrich-harness — substitua por testes reais.
import 'package:flutter_test/flutter_test.dart';

void main() {{
  test('HARNESS_GAP: feature `{fid}` precisa de cobertura unitária', () {{
    // TODO: espelhar Specification/features/{fid}/requirements.md
    // Código: {code}
    expect(true, isTrue, reason: 'Remova este stub após adicionar testes reais');
  }});
}}
""",
            )
            created += 1

        elif stack.get("dotnet"):
            # Prefer existing *Tests project
            tests_dirs = [p for p in repo.rglob("*Tests") if p.is_dir() and "obj" not in p.parts and "bin" not in p.parts]
            target = None
            for d in tests_dirs:
                if "Domain" in d.name or "Unit" in d.name or d.name.endswith("Tests"):
                    target = d
                    break
            if not target and tests_dirs:
                target = tests_dirs[0]
            if not target:
                continue
            safe = re.sub(r"[^A-Za-z0-9_]", "", fid.title().replace("-", "_")) or "Feature"
            stub = target / f"{safe}HarnessGapTests.cs"
            if stub.exists():
                continue
            ns = target.name.replace("-", "_")
            write(
                stub,
                f"""// Stub gerado pelo enrich-harness — substitua por testes reais.
using Xunit;

namespace {ns};

public class {safe}HarnessGapTests
{{
    [Fact(Skip = "HARNESS_GAP: feature `{fid}` — implementar cobertura. Código: {code}")]
    public void Feature_{safe}_NeedsUnitCoverage()
    {{
        Assert.True(true);
    }}
}}
""",
            )
            created += 1

    return created


# ── Requirements refresh from code symbols ──────────────────────────────────


def enrich_requirements(dest: Path, fid: str, code: str, desc: str, symbols: list[str]) -> None:
    path = dest / "requirements.md"
    base = read(path)
    if "### Tipos / símbolos do código" in base:
        return
    extra = "\n".join(f"- `{s}`" for s in symbols[:15]) if symbols else "- (nenhum tipo Domain mapeado nesta pasta)"
    write(
        path,
        (base or f"# Requirements — {fid}\n\n## Intenção\n\n{desc}\n")
        + f"""

### Tipos / símbolos do código

Código: `{code}`

{extra}

> Atualizado por enrich-harness em {date.today().isoformat()}.
""",
    )


# ── Orquestração ────────────────────────────────────────────────────────────


def enrich_repo(repo: Path) -> dict:
    harness = repo / ".ai-harness"
    if not harness.is_dir():
        return {"ok": False}

    # Reaproveita descoberta do deep-fill
    readme = fill.read_readme(repo)
    stack = fill.detect_stack(repo)
    table = deep.parse_feature_tables(readme)
    features = deep.discover_features_deep(repo, stack, table)
    all_tests = deep.discover_unit_tests(repo)
    test_map = deep.map_tests_to_features(repo, features, all_tests)

    arch_style = "ver Knowledge/Architecture.md"
    if stack.get("flutter"):
        arch_style = "Feature-first (Flutter) + BLoC/Cubit"
    elif stack.get("dotnet"):
        low = f"{repo.name} {repo}".lower()
        arch_style = (
            "Clean Architecture / CQRS (.NET)"
            if ("flow" in low or "mediator" in low or "fato" in low)
            else ".NET modular"
        )
    elif stack.get("docs_only"):
        arch_style = "Documentação / framework versionado"

    integrations = detect_integrations(repo, stack, readme)

    # Domain glossary
    write(harness / "Knowledge/Domain.md", build_glossary(repo, stack, features))

    # ADR
    write_adr(repo, harness, stack, readme, arch_style)

    # Governance
    write_governance(repo, harness, stack, integrations, readme)

    # Agents / Workflows
    write_agents_workflows(repo, harness, stack)

    # Per-feature use-cases + requirements symbols
    domain_types = extract_csharp_domain(repo) if stack.get("dotnet") else extract_dart_domain(repo) if stack.get("flutter") else []
    for fid, code, desc in features:
        dest = harness / "Specification" / "features" / fid
        dest.mkdir(parents=True, exist_ok=True)
        rewrite_use_cases(dest, fid, test_map.get(fid, []), desc)
        syms = [n for n, _, p in domain_types if code.split("/")[-1].lower() in p.lower() or fid.replace("-", "") in p.lower().replace(".", "").replace("-", "")]
        enrich_requirements(dest, fid, code, desc, syms or [n for n, _, _ in domain_types[:5]])

    stubs = ensure_test_stubs(repo, stack, features, test_map)

    # Regenera acceptance após stubs (para incluir novos testes)
    if stubs:
        all_tests = deep.discover_unit_tests(repo)
        test_map = deep.map_tests_to_features(repo, features, all_tests)
        for fid, code, desc in features:
            dest = harness / "Specification" / "features" / fid
            write(
                dest / "acceptance.md",
                deep.build_acceptance_md(repo, stack, fid, code, test_map.get(fid, []), []),
            )

    write(
        harness / "Knowledge/README.md",
        f"""# Knowledge — {repo.name}

Atualizado por `enrich-harness.py` em {date.today().isoformat()}.

| Documento | Conteúdo |
|-----------|----------|
| [Architecture.md](./Architecture.md) | Estilo e pastas |
| [Domain.md](./Domain.md) | Glossário completo (código + features) |
| [Standards.md](./Standards.md) | Build/test/git |
| [ADR/](./ADR/) | Decisões (ADR-0001 baseline) |
""",
    )

    return {
        "ok": True,
        "features": len(features),
        "tests": len(all_tests),
        "stubs": stubs,
        "integrations": len(integrations),
    }


def main() -> int:
    base = Path("/home/desenvolvedor/Projects/Refatora")
    if len(sys.argv) > 1:
        repos = [Path(p).resolve() for p in sys.argv[1:]]
    else:
        repos = sorted(p.parent for p in base.rglob(".ai-harness") if p.is_dir())

    ok = stubs_total = 0
    for repo in repos:
        if repo.name == "harness-engineering" and (repo / "template").is_dir():
            continue
        r = enrich_repo(repo)
        if not r.get("ok"):
            print(f"[SKIP] {repo.name}")
            continue
        print(
            f"[OK] {repo.name} — features={r['features']} tests={r['tests']} stubs={r['stubs']} integrations={r['integrations']}"
        )
        ok += 1
        stubs_total += r["stubs"]

    print(f"\nRepos: {ok} | Stubs de teste criados: {stubs_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
