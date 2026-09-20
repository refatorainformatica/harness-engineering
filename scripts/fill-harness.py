#!/usr/bin/env python3
"""Preenche .ai-harness/ com dados inferidos do repositório."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".ai-harness",
    ".cursor",
    ".idea",
    ".vscode",
    "node_modules",
    "bin",
    "obj",
    "build",
    ".dart_tool",
    "packages",
    "dist",
    "coverage",
    "artifacts-local",
    "logs",
    "__pycache__",
    ".venv",
    "venv",
}

DOTNET_TEST_GLOBS = ("*Tests*", "*Test", "tests", "test")

KIT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKSPACE = KIT_ROOT.parent

HARNESS_PROJECT_START = "<!-- HARNESS:PROJECT-START -->"
HARNESS_PROJECT_END = "<!-- HARNESS:PROJECT-END -->"


def read_readme(repo: Path) -> str:
    for name in ("README.md", "readme.md", "Readme.md"):
        p = repo / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return ""


def readme_summary(text: str) -> tuple[str, str]:
    # Remove banners HTML comuns
    text = re.sub(r"<p[^>]*>.*?</p>\s*", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)

    title = ""
    body: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not title and s.startswith("# "):
            title = s[2:].strip()
            continue
        if title and s and not s.startswith("#") and not s.startswith("|") and not s.startswith("- ["):
            if s.startswith("!["):
                continue
            if s.startswith("[") and "](" in s and s.count("|") == 0:
                continue
            if s in ("---", "***"):
                continue
            body.append(re.sub(r"\*\*([^*]+)\*\*", r"\1", s))
            if len(" ".join(body)) > 500:
                break
    vision = " ".join(body[:4]).strip() or "Projeto documentado em README.md."
    return title or "Projeto", vision[:800]


def detect_stack(repo: Path) -> dict[str, bool]:
    return {
        "dotnet": bool(list(repo.glob("*.sln")) + list(repo.glob("*.slnx")) + list(repo.glob("**/*.csproj"))[:1]),
        "flutter": (repo / "pubspec.yaml").exists(),
        "node": (repo / "package.json").exists(),
        "python": (repo / "pyproject.toml").exists() or (repo / "requirements.txt").exists(),
        "docker": (repo / "docker-compose.yml").exists() or (repo / "Dockerfile").exists(),
        "docs_only": (repo / "docs").is_dir() and not list(repo.glob("**/*.csproj"))[:3] and not (repo / "pubspec.yaml").exists(),
        "landing": (repo / "index.html").exists() and (repo / "css").is_dir(),
    }


def list_tree(repo: Path, max_depth: int = 2) -> str:
    lines: list[str] = [f"{repo.name}/"]

    def walk(base: Path, prefix: str, depth: int) -> None:
        if depth > max_depth:
            return
        entries = sorted(
            [p for p in base.iterdir() if p.name not in SKIP_DIRS and not p.name.startswith(".")],
            key=lambda p: (not p.is_dir(), p.name.lower()),
        )
        for i, p in enumerate(entries[:20]):
            last = i == len(entries[:20]) - 1
            branch = "└── " if last else "├── "
            lines.append(f"{prefix}{branch}{p.name}{'/' if p.is_dir() else ''}")
            if p.is_dir() and depth < max_depth:
                ext = "    " if last else "│   "
                walk(p, prefix + ext, depth + 1)

    walk(repo, "", 0)
    return "\n".join(lines[:35])


def code_root(repo: Path, stack: dict[str, bool]) -> Path:
    for candidate in ("src", "lib", "Apis", "Source"):
        p = repo / candidate
        if p.is_dir():
            return p
    return repo


def detect_features(repo: Path, stack: dict[str, bool]) -> list[tuple[str, str, str]]:
    features: list[tuple[str, str, str]] = []

    if stack["flutter"]:
        feat = repo / "lib" / "features"
        if feat.is_dir():
            for d in sorted(feat.iterdir()):
                if d.is_dir() and not d.name.startswith("."):
                    features.append((d.name, f"lib/features/{d.name}", "stable"))

    if stack["dotnet"]:
        for csproj in sorted(repo.rglob("*.csproj")):
            if any(x in csproj.parts for x in SKIP_DIRS):
                continue
            rel = csproj.parent.relative_to(repo)
            if rel.parts and rel.parts[0] in SKIP_DIRS:
                continue
            name = csproj.stem
            if name.endswith(".Tests") or name.endswith("Test"):
                continue
            if len(features) >= 25:
                break
            features.append((name.lower(), str(rel), "stable"))

    apis = repo / "Apis"
    if apis.is_dir():
        for d in sorted(apis.iterdir()):
            if d.is_dir() and d.name not in SKIP_DIRS:
                features.append((d.name.lower(), f"Apis/{d.name}", "stable"))

    if stack["docs_only"] and not features:
        for doc in sorted((repo / "docs").rglob("*.md"))[:8]:
            fid = doc.stem.lower().replace(" ", "-")
            features.append((fid, str(doc.parent.relative_to(repo)), "stable"))

    return features[:20]


def dotnet_solution(repo: Path) -> str | None:
    sln = list(repo.glob("*.sln")) + list(repo.glob("*.slnx"))
    return sln[0].name if sln else None


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def upsert_project_section(path: Path, title: str, body: str) -> None:
    """Insert or replace the generated overlay without wiping canonical template rules."""
    block = (
        f"{HARNESS_PROJECT_START}\n"
        f"## {title}\n\n"
        f"{body.rstrip()}\n"
        f"{HARNESS_PROJECT_END}\n"
    )
    if path.is_file():
        existing = path.read_text(encoding="utf-8", errors="replace")
        if HARNESS_PROJECT_START in existing and HARNESS_PROJECT_END in existing:
            pre = existing.split(HARNESS_PROJECT_START)[0].rstrip()
            post = existing.split(HARNESS_PROJECT_END, 1)[1]
            text = pre + "\n\n" + block + post.lstrip("\n")
        else:
            text = existing.rstrip() + "\n\n" + block
        write(path, text)
    else:
        write(path, block)


def fill_repo(repo: Path) -> None:
    harness = repo / ".ai-harness"
    if not harness.is_dir():
        return

    name = repo.name
    readme = read_readme(repo)
    title, vision = readme_summary(readme)
    stack = detect_stack(repo)
    tree = list_tree(repo)
    root = code_root(repo, stack)
    features = detect_features(repo, stack)
    sln = dotnet_solution(repo)

    arch_style = []
    if stack["flutter"]:
        arch_style.append("Feature-first (Flutter) + BLoC/Cubit")
    if stack["dotnet"]:
        arch_style.append("Clean Architecture / CQRS (.NET)" if "mediator" in name.lower() or "flow" in name.lower() else ".NET modular")
    if stack["docs_only"]:
        arch_style.append("Repositório de documentação / framework")
    if stack["landing"]:
        arch_style.append("Site estático (HTML/CSS/JS)")
    if not arch_style:
        arch_style.append("Consulte README.md e pastas do repositório")

    stack_rows = []
    if stack["dotnet"]:
        stack_rows.append(f"| Runtime | .NET ({sln or 'csproj'}) |")
    if stack["flutter"]:
        stack_rows.append("| UI | Flutter / Dart |")
    if stack["node"]:
        stack_rows.append("| Frontend / tooling | Node.js |")
    if stack["python"]:
        stack_rows.append("| Runtime | Python |")
    if stack["docker"]:
        stack_rows.append("| Containers | Docker / docker-compose |")
    stack_rows.append(f"| Harness | `.ai-harness/` |")

    feature_table = ""
    if features:
        rows = []
        for fid, code, status in features:
            rows.append(f"| {fid} | [./{fid}/](./{fid}/) | `{code}` | {status} | resumo em README / código |")
        feature_table = "\n".join(rows)
    else:
        feature_table = "| core | [./core/](./core/) | `.` | planned | Preencher conforme evolução |"

    write(
        harness / "Knowledge/Architecture.md",
        f"""# Architecture — {name}

> Gerado automaticamente em {date.today().isoformat()}. Revise e refine.

## Estilo

{chr(10).join('- ' + s for s in arch_style)}

**Feature-first (obrigatório):** pastas de código e de teste seguem a capacidade de negócio. Camadas técnicas ficam **dentro** da feature. Ver `Standards.md`.

**OSS-first:** open source → self-host → cloud proprietário só com ADR (`Governance/cost.md`).

**Domínio rico** se DDD/Clean Architecture: comportamento nas entidades; Application só orquestra.

## Estrutura (topo do repositório)

```text
{tree}
```

## Raiz de código principal

`{root.relative_to(repo) if root != repo else '.'}`

## Stack detectada

| Camada | Tecnologia |
|--------|------------|
{chr(10).join(stack_rows)}

## Relação harness ↔ código

| Spec feature | Código |
|--------------|--------|
| `Specification/features/<id>/` | módulo/pasta correspondente |

## Cross-cutting (preencher)

| Peça | Papel |
|------|--------|
| DI | ver README / código |
| Auth | ver README / código |
| Persistência | ver README / código |
| Observability | ver README / código |

## Fora de escopo arquitetural (atual)

- Consultar README.md e issues abertas
""",
    )

    write(
        harness / "Knowledge/Domain.md",
        f"""# Domain — {name}

## Visão

{vision}

## Produto / propósito

**{title}** — ver README.md para detalhes completos.

## Glossário (inicial)

| Termo | Significado |
|-------|-------------|
| Harness | Estrutura `.ai-harness/` deste repositório |
| Feature | Unidade em `Specification/features/<id>/` |
| Run | Execução do agente em `Runtime/state/runs/` |

> Adicione termos do domínio conforme o produto evolui.

## Criticidade

- Perfil: {"IA assistiva" if "ai" in name.lower() else "software tradicional"}
- Risco: médio (revisar com o time)
- Owner: engineering
""",
    )

    test_cmd = "dotnet test"
    if sln:
        test_cmd = f"dotnet test {sln}"
    elif stack["flutter"]:
        test_cmd = "flutter test"
    elif stack["node"]:
        test_cmd = "npm test"

    build_cmd = f"dotnet build {sln}" if sln else ("flutter build apk --debug" if stack["flutter"] else "ver README")

    stack_body = f"""- Stack: {', '.join(k for k, v in stack.items() if v and k not in ('docs_only', 'landing')) or 'ver README'}
- Formatação: formatter da stack (`dotnet format`, `dart format`, etc.)
- Testes: `{test_cmd}` (pasta da feature)
- Build:

```bash
{build_cmd}
```

- Commit/push: **ask** (`Governance/permissions.md`)
- Deps: OSS primeiro (`Governance/cost.md`)
"""
    standards_path = harness / "Knowledge/Standards.md"
    if standards_path.is_file() and "Organização por feature" in standards_path.read_text(encoding="utf-8", errors="replace"):
        upsert_project_section(standards_path, "Stack e comandos (gerado)", stack_body)
    else:
        write(
            standards_path,
            f"""# Standards — {name}

> Gerado automaticamente. Alinhe com o README do projeto.

## Organização por feature (obrigatório)

Código e testes **sempre** por capacidade de negócio. Ver template do kit.

## Stack e comandos (gerado)

{stack_body}
""",
        )

    # Tools — stack-specific sections
    build_tools = """## Genérico / arquivos

| ID | Ação | Notas |
|----|------|-------|
| `fs.read` | Ler arquivos | auto |
| `fs.write` | Editar no escopo | auto |
| `fs.delete` | Apagar arquivo | **ask** |
| `fs.write.secrets` | Secrets | **deny** |
"""
    if stack["dotnet"]:
        build_tools += """
## .NET

| ID | Comando | Notas |
|----|---------|-------|
| `dotnet.restore` | `dotnet restore` | auto |
| `dotnet.build` | `dotnet build` | auto |
| `dotnet.format` | `dotnet format` | auto escopo |
| `dotnet.add.package` | `dotnet add package` | **ask** |
"""
    if stack["flutter"]:
        build_tools += """
## Flutter

| ID | Comando | Notas |
|----|---------|-------|
| `flutter.pub.get` | `flutter pub get` | auto |
| `dart.format` | `dart format` | auto |
| `flutter.pub.add` | `flutter pub add` | **ask** |
| `flutter.pub.upgrade` | upgrade global | **deny** |
"""
    if stack["node"]:
        build_tools += """
## Node

| ID | Comando | Notas |
|----|---------|-------|
| `node.install` | npm/pnpm/yarn install | auto |
| `node.build` | npm run build | auto |
| `node.add.dep` | add dependency | **ask** |
"""
    write(harness / "Tools/build.md", f"# Tools — Build\n\n{build_tools}")

    test_tools = "| ID | Comando | Notas |\n|----|---------|-------|\n"
    if stack["dotnet"]:
        test_tools += f"| `dotnet.test` | `{test_cmd}` | auto |\n"
    if stack["flutter"]:
        test_tools += "| `flutter.test` | `flutter test` | auto |\n"
    if stack["node"]:
        test_tools += "| `node.test` | `npm test` | auto |\n"
    if not stack["dotnet"] and not stack["flutter"] and not stack["node"]:
        test_tools += "| `test.manual` | conforme README | **ask** |\n"
    test_tools += (
        "\nNovos testes: **sempre** sob a pasta da feature (`Standards.md`). "
        "Lacuna AC-G*: stub mínimo na pasta da feature.\n"
    )
    write(harness / "Tools/test.md", f"# Tools — Test\n\n{test_tools}")

    val_tools = """| ID | Ação | Notas |
|----|------|-------|
| `harness.spec.read` | Ler `.ai-harness/**` | auto |
| `harness.spec.write` | Atualizar specs | auto se mudou |
| `harness.state.write` | Runtime/state | auto |
"""
    if stack["dotnet"]:
        val_tools += "| `dotnet.build` | build de validação | auto |\n"
    if stack["flutter"]:
        val_tools += "| `flutter.analyze` | `flutter analyze` | auto |\n"
    write(harness / "Tools/validation.md", f"# Tools — Validation\n\n{val_tools}")

    upsert_project_section(
        harness / "Governance/architecture.md",
        "Projeto (detectado)",
        f"- Estilo: {arch_style[0]}\n"
        "- Feature-first e OSS-first valem mesmo neste overlay.\n"
        "- Mudanças estruturais → ADR; cloud proprietário → ADR (`cost.md`).\n",
    )
    upsert_project_section(
        harness / "Governance/quality.md",
        "Projeto (detectado)",
        f"- Build: `{build_cmd}`\n"
        f"- Testes: `{test_cmd}` (escopo da feature; AC-T* ou AC-G* + stub)\n"
        "- Evidências em `Specification/features/<id>/acceptance.md`\n",
    )

    write(
        harness / "Specification/features/INDEX.md",
        f"""# Features — índice

> Gerado automaticamente em {date.today().isoformat()}.

| ID | Spec | Código | Status | Resumo |
|----|------|--------|--------|--------|
{feature_table}

## Próximo passo

Para cada feature crítica, preencher `requirements.md`, `use-cases.md`, `acceptance.md`.
""",
    )

    # Seed spec folders for top features (max 5)
    tpl_r = harness / "Specification/templates/requirements.md"
    tpl_u = harness / "Specification/templates/use-cases.md"
    tpl_a = harness / "Specification/templates/acceptance.md"
    if tpl_r.exists() and features:
        for fid, code, status in features[:5]:
            dest = harness / "Specification/features" / fid
            if dest.exists() and (dest / "requirements.md").exists():
                continue
            dest.mkdir(parents=True, exist_ok=True)
            req = tpl_r.read_text(encoding="utf-8").replace("<id>", fid).replace("{{path}}", code.rsplit("/", 1)[0] if "/" in code else code)
            uc = tpl_u.read_text(encoding="utf-8").replace("<id>", fid)
            ac = tpl_a.read_text(encoding="utf-8").replace("<id>", fid)
            ac = ac.replace("- [ ] AC-01 — Use cases cobertos ou testados", f"- [ ] AC-01 — Módulo `{code}` documentado e testado")
            write(dest / "requirements.md", req.replace("planned \\| wip \\| partial \\| stable", status))
            write(dest / "use-cases.md", uc)
            write(dest / "acceptance.md", ac)

    # Remove example if we created real features
    ex = harness / "Specification/features/example"
    if features and ex.is_dir():
        import shutil

        shutil.rmtree(ex)


def main() -> int:
    base = DEFAULT_WORKSPACE
    if len(sys.argv) > 1:
        repos = [Path(p).resolve() for p in sys.argv[1:]]
    else:
        repos = sorted(p.parent for p in base.rglob(".ai-harness") if p.is_dir())

    ok = 0
    for repo in repos:
        if not (repo / ".ai-harness").is_dir():
            print(f"[SKIP] {repo.name} — sem .ai-harness")
            continue
        fill_repo(repo)
        print(f"[OK] {repo.name}")
        ok += 1
    print(f"\nPreenchidos: {ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
