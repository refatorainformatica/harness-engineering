#!/usr/bin/env python3
"""
Second enrichment script for .ai-harness/

Completes what fill/deep-fill left shallow:
- ADR from real decisions (stack, style, integrations)
- Domain glossary from the code (entities, enums, features)
- Use cases derived from tests + public types in the code
- Project-specific Governance security/cost for the detected project
- Custom Agents/Workflows: only `Agents/project.md` (roles come from the template)
- Test stubs for features with a coverage gap (AC-G*)

Usage:
  python3 enrich-harness.py [/path/to/repo ...]
  (no args: every .ai-harness under the current directory)
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


# ── Code → glossary / types ─────────────────────────────────────────────────


def extract_csharp_domain(repo: Path) -> list[tuple[str, str, str]]:
    """(term, kind, path)"""
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
        # prioritize Domain / Entities / ValueObjects / Features
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
        ("Harness", "`.ai-harness/` structure of this repository", "—"),
        ("Feature", "Unit in `Specification/features/<id>/`", "—"),
        ("Run", "Agent execution in `Runtime/state/runs/`", "—"),
        ("Acceptance", "Criteria derived from unit tests (AC-T*)", "—"),
    ]
    seen = {r[0].lower() for r in rows}

    for fid, code, desc in features:
        if fid.lower() in seen:
            continue
        seen.add(fid.lower())
        rows.append((fid, desc[:120] or f"Module `{code}`", code))

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
        rows.append((name, f"{kind} in `{path}`", path))
        if len(rows) >= 60:
            break

    table = "\n".join(f"| {t} | {m} | `{p}` |" for t, m, p in rows)
    return f"""# Domain — {repo.name}

> Glossary enriched on {date.today().isoformat()} from features + code.

## Glossary (ubiquitous language)

| Term | Meaning | Source |
|------|---------|--------|
{table}

## How to maintain

1. New domain concept → a row in this glossary **in the same PR**.
2. Same identifier in the SPEC, code and tests.
3. ADR if the term implies an architectural trade-off.
"""


# ── Use cases from tests / code ────────────────────────────────────────────


def humanize_test_name(name: str) -> tuple[str, str, str]:
    """Convert a test name into an approximate Given/When/Then."""
    raw = name
    # snake/camel → spaces
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    s = s.replace("_", " ").strip()
    s = re.sub(r"\s+", " ", s)

    given = "the system is in the initial state of the test"
    when = f"the scenario `{raw}` runs"
    then = f"the behavior `{s}` holds"

    low = s.lower()
    if "should" in low:
        parts = re.split(r"\bshould\b", s, flags=re.I)
        when = parts[0].strip() or when
        then = ("should " + parts[1].strip()) if len(parts) > 1 else then
    if "emits" in low:
        then = s
        when = "the scenario event/action is triggered"
    # Test-name keywords: English and Portuguese (test names in target projects may use either).
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

- **Actor:** system under test
- **Source:** `{rel}` ({t.kind})
- **Given** {g}
- **When** {w}
- **Then** {th}
"""
            )
    else:
        ucs.append(
            f"""## UC-01 — Main behavior of `{fid}`

- **Actor:** user / API consumer
- **Given** the module `{fid}` is available
- **When** the main operation described in requirements is executed
- **Then** {description[:180] or "the result expected in the SPEC is obtained"}

## UC-02 — Test gap

- **Actor:** engineering
- **Given** no unit tests are mapped to `{fid}`
- **When** the feature evolves
- **Then** an automated test is added and the acceptance file is regenerated
"""
        )
    write(dest / "use-cases.md", f"# Use Cases — {fid}\n\n> Derived from tests/code on {date.today().isoformat()}.\n\n" + "\n".join(ucs))


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
        ("MediatR-style / Mediator", ["imediator", "mediatr"]),
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
    adr_path = adr_dir / "adr-0001-baseline-architecture.md"

    alts = []
    if stack.get("dotnet"):
        alts = ["Anemic monolith without layers", "Premature microservices", "In-process mediator vs gRPC"]
    elif stack.get("flutter"):
        alts = ["Online-only with a REST API", "Single global state management", "No E2E encryption"]
    elif stack.get("docs_only"):
        alts = ["Unversioned wiki", "Single PDF without gates"]
    else:
        alts = ["Proprietary cloud-first stack", "No folder standardization"]

    write(
        adr_path,
        f"""# ADR-0001: Baseline architecture — {repo.name}

| Field | Value |
|-------|-------|
| Status | accepted |
| Date | {date.today().isoformat()} |
| Deciders | engineering (inferred from the repository) |

## Context

The `{repo.name}` repository needs an explicit architectural baseline for agents and humans.
Decisions were inferred from the code, README and dependencies on {date.today().isoformat()}.

## Decision

- **Style:** {arch_style}
- **Adopted integrations:** {', '.join(integrations) if integrations else 'see README'}
- **Harness:** `.ai-harness/` folder as the operational contract (Specs + Agents + Governance)
- **Acceptance:** acceptance criteria tied to existing unit tests (`AC-T*`)

## Alternatives considered

{chr(10).join(f'{i}. {a}' for i, a in enumerate(alts, 1))}

## Consequences

### Positive
- Agents have a clear anchor (Knowledge + ADR)
- Structural changes require a new ADR
- Tests become the acceptance contract

### Negative / risks
- An inferred ADR may need human review
- Listed integrations reflect the current state of the code, not the roadmap

## Links

- `Knowledge/architecture.md`
- `Knowledge/domain.md`
- README.md
""",
    )

    write(
        adr_dir / "readme.md",
        f"""# ADR — Architecture Decision Records

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| ADR-0001 | [Baseline architecture](./adr-0001-baseline-architecture.md) | accepted | {date.today().isoformat()} |

## When to create

- New significant dependency
- Change of architectural style
- External integration / vendor
- Performance, security or cost trade-off with systemic impact

## How

1. Copy [template.md](./template.md) → `adr-xxxx-short-title.md`
2. Fill in Context / Decision / Consequences
3. Update this index
""",
    )


# ── Governance ──────────────────────────────────────────────────────────────


def write_governance(repo: Path, harness: Path, stack: dict, integrations: list[str], _readme: str) -> None:
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

    extra: list[str] = []
    if has_secrets or "firebase" in " ".join(integrations).lower():
        extra.append("Local config files (`dart_defines`, `appsettings`, service accounts) stay gitignored.")
    if has_ai:
        extra.append("AI feature detected — no production data in prompts; OSS/local models first.")
    if stack.get("dotnet"):
        extra.append(".NET stack: apply the rich domain model (`Governance/architecture.md`).")

    sec_body = (
        f"Generated on {date.today().isoformat()} for `{repo.name}`.\n\n"
        f"**Detected integrations:** {', '.join(integrations) if integrations else 'see Knowledge/architecture.md'}\n\n"
        + (("**Notes:**\n" + "\n".join(f"- {r}" for r in extra) + "\n") if extra else "")
        + "The canonical baseline (secrets, PII, OSS, AI) remains in the sections above — this overlay does not replace it.\n"
    )
    fill.upsert_project_section(harness / "Governance/security.md", "Project (detected)", sec_body)

    cost_bits = [
        f"Generated on {date.today().isoformat()} for `{repo.name}`.",
        "The baseline OSS preference remains mandatory.",
    ]
    if has_cloud:
        cost_bits.append("Cloud detected: free tier / self-host; SKU upgrade = **ask**.")
    if has_ai:
        cost_bits.append("AI detected: Ollama/local first; paid API only with authorization.")
    if stack.get("dotnet") or stack.get("flutter"):
        cost_bits.append("CI: run the feature-scope tests, not the whole suite on every iteration.")
    if "docker" in " ".join(integrations).lower():
        cost_bits.append("Do not start the full compose stack just for unit tests.")
    fill.upsert_project_section(
        harness / "Governance/cost.md",
        "Project (detected)",
        "\n".join(f"- {b}" for b in cost_bits) + "\n",
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
        code_root = "src/**/Features/<Name>/"
    elif stack.get("java"):
        maven = (repo / "pom.xml").exists()
        build_c = "./mvnw -q verify -DskipTests" if maven else "./gradlew build -x test"
        test_c = "./mvnw test" if maven else "./gradlew test"
        code_root = "src/main/java/**/features/<feature>/"
    elif stack.get("angular"):
        build_c = "npm run build"
        test_c = "npm test"
        code_root = "src/app/features/<id>/"
    elif stack.get("node"):
        build_c = "npm run build"
        test_c = "npm test"
        code_root = "src/features/<id>/"
    elif stack.get("python"):
        build_c = "python -m compileall -q ."
        test_c = "pytest tests/features/<id>/"
        code_root = "<pkg>/features/<id>/"
    else:
        extra = next(
            (e for e in fill.EXTRA_STACKS if stack.get(e[0]) and (e[2] or e[4])),
            None,
        )
        build_c = extra[3][1] if extra and extra[3] else "see README"
        test_c = extra[2][1] if extra and extra[2] else "see README"
        code_root = extra[4] if extra and extra[4] else "."

    write(
        harness / "Agents/project.md",
        f"""# Project context — {repo.name}

> Generated by enrich-harness on {date.today().isoformat()}. The roles in `developer.md` / `tester.md` are **not** replaced.

## Paths

- Code: `{code_root}`
- Specs: `Specification/features/<id>/`
- Tests: feature folder (`Knowledge/standards.md`)

## Active stack packs

Read **only** these (`Knowledge/stacks/readme.md`):

{fill.packs_markdown(stack)}

## Commands (`auto`)

```bash
{build_c}
{test_c}
```

## Notes

- Acceptance: AC-T* green or AC-G* + stub in the feature folder
- OSS / cloud: `Governance/cost.md`
""",
    )


# ── Test stubs for gaps ────────────────────────────────────────────────────


def ensure_test_stubs(repo: Path, stack: dict, features: list[tuple[str, str, str]], test_map: dict) -> int:
    """Create minimal stubs for features without tests. Returns how many were created."""
    created = 0
    for fid, code, desc in features:
        if test_map.get(fid):
            continue
        if fid in ("core",) and not stack.get("flutter") and not stack.get("dotnet"):
            # docs-only: do not create code stubs
            continue

        if stack.get("flutter"):
            stub = repo / "test" / "features" / fid / f"{fid}_harness_gap_test.dart"
            if stub.exists():
                continue
            write(
                stub,
                f"""// Stub generated by enrich-harness — replace with real tests.
import 'package:flutter_test/flutter_test.dart';

void main() {{
  test('HARNESS_GAP: feature `{fid}` needs unit coverage', () {{
    // TODO: mirror Specification/features/{fid}/requirements.md
    // Code: {code}
    expect(true, isTrue, reason: 'Remove this stub after adding real tests');
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
            ns = target.name.replace("-", "_")
            stub = target / "Features" / safe / f"{safe}HarnessGapTests.cs"
            if stub.exists():
                continue
            write(
                stub,
                f"""// Stub generated by enrich-harness — replace with real tests.
using Xunit;

namespace {ns};

public class {safe}HarnessGapTests
{{
    [Fact(Skip = "HARNESS_GAP: feature `{fid}` — implement coverage. Code: {code}")]
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


# Current heading first; the legacy Portuguese one is still recognized so old projects are not duplicated.
SYMBOLS_HEADINGS = ("### Code types / symbols", "### Tipos / símbolos do código")


def enrich_requirements(dest: Path, fid: str, code: str, desc: str, symbols: list[str]) -> None:
    path = dest / "requirements.md"
    base = read(path)
    if any(h in base for h in SYMBOLS_HEADINGS):
        return
    extra = "\n".join(f"- `{s}`" for s in symbols[:15]) if symbols else "- (no Domain type mapped in this folder)"
    write(
        path,
        (base or f"# Requirements — {fid}\n\n## Intent\n\n{desc}\n")
        + f"""

{SYMBOLS_HEADINGS[0]}

Code: `{code}`

{extra}

> Updated by enrich-harness on {date.today().isoformat()}.
""",
    )


# ── Orchestration ───────────────────────────────────────────────────────────


def enrich_repo(repo: Path) -> dict:
    harness = repo / ".ai-harness"
    if not harness.is_dir():
        return {"ok": False}

    # Reuse the deep-fill discovery
    readme = fill.read_readme(repo)
    stack = fill.detect_stack(repo)
    table = deep.parse_feature_tables(readme)
    features = deep.discover_features_deep(repo, stack, table)
    all_tests = deep.discover_unit_tests(repo)
    test_map = deep.map_tests_to_features(repo, features, all_tests)

    arch_style = "see Knowledge/architecture.md"
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
        arch_style = "Versioned documentation / framework"

    integrations = detect_integrations(repo, stack, readme)

    # Domain glossary
    write(harness / "Knowledge/domain.md", build_glossary(repo, stack, features))

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

    # Regenerate acceptance after the stubs (to include the new tests)
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
        harness / "Knowledge/readme.md",
        f"""# Knowledge — {repo.name}

Updated by `enrich-harness.py` on {date.today().isoformat()}.

| Document | Content |
|----------|---------|
| [architecture.md](./architecture.md) | Style and folders |
| [domain.md](./domain.md) | Full glossary (code + features) |
| [standards.md](./standards.md) | Build/test/git |
| [ADR/](./ADR/) | Decisions (ADR-0001 baseline) |
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
    base = fill.DEFAULT_WORKSPACE
    if len(sys.argv) > 1:
        repos = [Path(p).resolve() for p in sys.argv[1:]]
    else:
        repos = sorted(p.parent for p in base.rglob(".ai-harness") if p.is_dir())

    ok = stubs_total = 0
    for repo in repos:
        if fill.is_harness_kit(repo):
            print(f"[SKIP] {repo.name} — kit-template")
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

    print(f"\nRepos: {ok} | Test stubs created: {stubs_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
