#!/usr/bin/env python3
"""Deepen .ai-harness/ with complete specs derived from the README, code and tests."""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FILL_PATH = SCRIPT_DIR / "fill-harness.py"


def load_fill_module():
    spec = importlib.util.spec_from_file_location("fill_harness", FILL_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


fill = load_fill_module()

TEST_SKIP = fill.SKIP_DIRS | {"packages", "artifacts-local"}


@dataclass
class UnitTest:
    rel_path: str
    file_name: str
    name: str
    kind: str  # fact | theory | test | blocTest | group


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def parse_csharp_tests(path: Path) -> list[UnitTest]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path)
    tests: list[UnitTest] = []
    for m in re.finditer(
        r"\[(Fact|Theory)(?:\([^\)]*\))?\]\s*"
        r"(?:public|private|internal|protected)\s+(?:async\s+)?(?:Task|void)\s+(\w+)\s*\(",
        text,
        flags=re.MULTILINE,
    ):
        tests.append(UnitTest(rel, path.name, m.group(2), m.group(1).lower()))
    return tests


def parse_dart_tests(path: Path) -> list[UnitTest]:
    text = path.read_text(encoding="utf-8", errors="replace")
    tests: list[UnitTest] = []
    for m in re.finditer(r"\btest(?:Widgets)?\(\s*'([^']+)'", text):
        tests.append(UnitTest(str(path), path.name, m.group(1), "test"))
    for m in re.finditer(r"\bblocTest<[^>]+>\(\s*\n?\s*'([^']+)'", text):
        tests.append(UnitTest(str(path), path.name, m.group(1), "blocTest"))
    for m in re.finditer(r"\bgroup\(\s*'([^']+)'", text):
        tests.append(UnitTest(str(path), path.name, m.group(1), "group"))
    return tests


def parse_python_tests(path: Path) -> list[UnitTest]:
    text = path.read_text(encoding="utf-8", errors="replace")
    tests: list[UnitTest] = []
    for m in re.finditer(r"^\s*def (test_\w+)\s*\(", text, flags=re.MULTILINE):
        tests.append(UnitTest(str(path), path.name, m.group(1), "pytest"))
    return tests


def discover_unit_tests(repo: Path) -> list[UnitTest]:
    tests: list[UnitTest] = []
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if any(part in TEST_SKIP for part in path.parts):
            continue
        rel = path.relative_to(repo)
        name = path.name.lower()
        rel_s = str(rel)
        if name.endswith(".cs") and ("test" in name or "tests" in rel.parts):
            for t in parse_csharp_tests(path):
                tests.append(UnitTest(rel_s, path.name, t.name, t.kind))
        elif name.endswith("_test.dart") or (name.endswith("test.dart") and "test" in rel.parts):
            for t in parse_dart_tests(path):
                tests.append(UnitTest(rel_s, path.name, t.name, t.kind))
        elif name.startswith("test_") and name.endswith(".py"):
            for t in parse_python_tests(path):
                tests.append(UnitTest(rel_s, path.name, t.name, t.kind))
    return tests


def feature_match_score(fid: str, code: str, test: UnitTest, repo: Path) -> int:
    rel_s = test.rel_path.lower().replace("\\", "/")
    fid_l = fid.lower()
    code_l = code.lower().replace("\\", "/")
    tokens = set(re.findall(r"[a-z0-9]+", fid_l + " " + code_l))
    score = 0
    if f"/features/{fid_l}/" in rel_s or f"features/{fid_l}/" in rel_s:
        score += 100
    if f"/{fid_l}/" in rel_s:
        score += 80
    # tests/MyApp.Domain.Tests → Domain project
    m = re.search(r"tests/([a-z0-9.]+)\.tests/", rel_s, re.I)
    if m:
        proj = re.sub(r"[^a-z0-9]", "", m.group(1).lower())
        fid_norm = re.sub(r"[^a-z0-9]", "", fid_l)
        code_norm = re.sub(r"[^a-z0-9]", "", code_l)
        if proj and (proj in fid_norm or proj in code_norm or fid_norm in proj):
            score += 130
    if fid_l in rel_s.replace("_", "-").replace("/", "-").split("-"):
        score += 60
    for t in tokens:
        if len(t) < 3:
            continue
        if t in rel_s or t in test.file_name.lower():
            score += 15
    # dotnet: the Tests project mirrors the csproj
    proj = fid_l.replace("-", "")
    if proj and proj in rel_s.replace("-", "").replace("_", ""):
        score += 40
    return score


def map_tests_to_features(
    repo: Path,
    features: list[tuple[str, str, str]],
    all_tests: list[UnitTest],
) -> dict[str, list[UnitTest]]:
    mapping: dict[str, list[UnitTest]] = {fid: [] for fid, _, _ in features}
    assigned: set[tuple[str, str]] = set()

    for test in all_tests:
        key = (test.rel_path, test.name)
        best_fid = None
        best_score = 0
        for fid, code, _ in features:
            s = feature_match_score(fid, code, test, repo)
            if s > best_score:
                best_score = s
                best_fid = fid
        if best_fid and best_score >= 40:
            mapping[best_fid].append(test)
            assigned.add(key)

    # orphan tests → core feature (if any) or the first feature
    orphan_fid = next((f[0] for f in features if f[0] == "core"), features[0][0] if features else "core")
    for test in all_tests:
        key = (test.rel_path, test.name)
        if key not in assigned:
            if orphan_fid in mapping:
                mapping[orphan_fid].append(test)
            else:
                mapping.setdefault(orphan_fid, []).append(test)
    return mapping


def test_run_command(repo: Path, stack: dict[str, bool], fid: str, tests: list[UnitTest]) -> str:
    if not tests:
        sln = fill.dotnet_solution(repo)
        if stack["dotnet"] and sln:
            return f"dotnet test {sln}"
        if stack["flutter"]:
            return "flutter test"
        return "see README — no mapped tests"

    rel_paths: set[str] = set()
    for t in tests:
        p = Path(t.rel_path)
        if p.is_absolute():
            try:
                rel_paths.add(str(p.relative_to(repo)).replace("\\", "/"))
            except ValueError:
                rel_paths.add(t.file_name)
        else:
            rel_paths.add(str(p).replace("\\", "/"))

    if stack["flutter"]:
        if len(rel_paths) == 1:
            return f"flutter test {next(iter(rel_paths))}"
        parents = {str(Path(p).parent) for p in rel_paths}
        if len(parents) == 1:
            return f"flutter test {next(iter(parents))}/"
        return "flutter test " + " ".join(sorted(rel_paths)[:6])

    if stack["dotnet"]:
        if tests:
            parts = Path(tests[0].rel_path).parts
            if "tests" in parts:
                idx = parts.index("tests")
                if idx + 1 < len(parts):
                    proj_dir = repo.joinpath(*parts[: idx + 2])
                    csprojs = list(proj_dir.glob("*.csproj"))
                    if csprojs:
                        return f"dotnet test {csprojs[0].relative_to(repo)}"
        sln = fill.dotnet_solution(repo)
        for csproj in sorted(repo.rglob("*Tests*.csproj")):
            cs = str(csproj.relative_to(repo)).lower()
            if fid.replace("-", "") in cs.replace("-", "").replace(".", "") or any(
                p in cs for p in fid.lower().split("-") if len(p) > 2
            ):
                return f"dotnet test {csproj.relative_to(repo)}"
        return f"dotnet test {sln}" if sln else "dotnet test"

    if stack["python"]:
        return "pytest " + " ".join(sorted(rel_paths)[:6])

    return " ".join(sorted(rel_paths)[:3])


def build_acceptance_md(
    repo: Path,
    stack: dict[str, bool],
    fid: str,
    code: str,
    tests: list[UnitTest],
    business_rules: list[str],
) -> str:
    cmd = test_run_command(repo, stack, fid, tests)
    local_rules = rules_for_feature(fid, business_rules)

    if tests:
        checklist = []
        evidence = []
        for i, t in enumerate(tests, 1):
            ac_id = f"AC-T{i:02d}"
            rel = t.rel_path
            label = t.name.replace("|", "/")[:120]
            checklist.append(f"- [ ] {ac_id} — `{rel}` :: {label}")
            single_cmd = cmd
            if stack["flutter"]:
                single_cmd = f"flutter test {rel}"
            elif stack["dotnet"]:
                parts = Path(rel).parts
                if "tests" in parts:
                    idx = parts.index("tests")
                    if idx + 1 < len(parts):
                        proj_dir = repo.joinpath(*parts[: idx + 2])
                        csprojs = list(proj_dir.glob("*.csproj"))
                        if csprojs:
                            single_cmd = f"dotnet test {csprojs[0].relative_to(repo)} --filter FullyQualifiedName~{t.name}"
                        else:
                            single_cmd = cmd
                    else:
                        single_cmd = cmd
                else:
                    single_cmd = cmd
            evidence.append(f"| {ac_id} | {label[:60]} | `{rel}` | `{single_cmd}` | pending |")

        gaps = ""
        if local_rules:
            gaps = "\n## Gaps (AC-G*)\n\n"
            gaps += "\n".join(f"- Documented rule without an explicit automated test: {r[:100]}" for r in local_rules[:3])
            gaps += "\n\n> Add tests in `test/` or `tests/` and re-run `deep-fill-harness.py`.\n"

        return f"""# Acceptance Criteria — {fid}

> Generated from the repository **unit tests** on {date.today().isoformat()}.

## Validation command (scope)

```bash
{cmd}
```

## Criteria (= existing tests)

{chr(10).join(checklist)}

## Evidence

| AC | Test | File | Command | Result |
|----|------|------|---------|--------|
{chr(10).join(evidence)}

## Process criteria

- [ ] AC-P01 — Use cases in `use-cases.md` consistent with the tests above
- [ ] AC-P02 — No violation of Knowledge / Governance
- [ ] AC-P03 — New behavior requires a new test before marking DONE
{gaps}"""

    # no mapped tests
    return f"""# Acceptance Criteria — {fid}

> No unit test mapped to `{code}` on {date.today().isoformat()}.

## Gaps (AC-G*)

- [ ] AC-G01 — Create tests in `test/` or `tests/` mirroring this feature
- [ ] AC-G02 — Use cases covered by automated tests
- [ ] AC-G03 — `{cmd}` green after implementation

## Evidence

| AC | How to validate | Result |
|----|-----------------|--------|
| AC-G01 | PR adds `{code}` tests | pending |
| AC-G02 | Reviewer checks the test ↔ UC map | pending |
| AC-G03 | CI / local command | pending |

## Rules to cover (README)

{chr(10).join('- ' + r for r in local_rules[:5]) if local_rules else '- See requirements.md'}
"""


# README section names (lower-case) read from the target project, in Portuguese and English:
# target projects may be documented in either language.
BUSINESS_RULES_SECTIONS = ("regras de negócio", "regras de negocio", "business rules", "rules")
LIMITATIONS_SECTIONS = (
    "limitações atuais",
    "limitacoes atuais",
    "limitações",
    "limitacoes",
    "current limitations",
    "known limitations",
    "limitations",
)
ARCHITECTURE_SECTIONS = ("arquitetura", "architecture")
STACK_SECTIONS = ("stack", "tech stack", "tecnologias", "technologies")
FEATURE_HEADER_KEYWORDS = ("feature", "módulo", "modulo", "module")
DESCRIPTION_HEADER_KEYWORDS = ("respons", "descri", "propósito", "proposito", "purpose", "papel", "role")

# Sections appended to Governance/security.md (current titles + legacy Portuguese titles).
PRODUCT_SECURITY_SECTIONS = (
    "Rules derived from the product",
    "Limitations / risks",
    "Regras derivadas do produto",
    "Limitações / riscos",
)


def first_section(sections: dict[str, str], names: tuple[str, ...]) -> str:
    """Return the first non-empty README section among `names` (lower-case titles)."""
    for name in names:
        if sections.get(name):
            return sections[name]
    return ""


def strip_sections(text: str, titles: tuple[str, ...]) -> str:
    """Remove `## <title>` sections (up to the next `## ` heading) for each title."""
    for title in titles:
        text = re.sub(rf"\n*^## {re.escape(title)}[ \t]*\n.*?(?=^## |\Z)", "\n\n", text, flags=re.MULTILINE | re.DOTALL)
    return text.rstrip()


def parse_sections(text: str) -> dict[str, str]:
    text = re.sub(r"<p[^>]*>.*?</p>\s*", "", text, flags=re.DOTALL | re.IGNORECASE)
    sections: dict[str, str] = {}
    current = "_intro"
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            sections[current] = "\n".join(buf).strip()
            current = line[3:].strip().lower()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()
    return sections


def parse_bullets(block: str) -> list[str]:
    items = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("- "):
            items.append(re.sub(r"\*\*([^*]+)\*\*", r"\1", s[2:].strip()))
        elif s.startswith("* "):
            items.append(s[2:].strip())
    return items


def parse_feature_tables(text: str) -> dict[str, str]:
    """Extract markdown tables | feature | description | (plausible IDs only).

    README keywords are matched in Portuguese and English: target projects may use either language.
    """
    features: dict[str, str] = {}
    valid_id = re.compile(r"^[a-z][a-z0-9_-]{0,40}$")

    for block in re.findall(r"\|[^\n]+\|\n\|[-:| ]+\|\n(?:\|[^\n]+\|\n?)+", text):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip().startswith("|")]
        if len(lines) < 2:
            continue
        header = [c.strip().lower() for c in lines[0].split("|")[1:-1]]
        if not header:
            continue
        if not any(any(k in h for k in FEATURE_HEADER_KEYWORDS) for h in header):
            continue
        name_idx = next((i for i, h in enumerate(header) if any(k in h for k in FEATURE_HEADER_KEYWORDS)), 0)
        desc_idx = next((i for i, h in enumerate(header) if any(x in h for x in DESCRIPTION_HEADER_KEYWORDS)), min(1, len(header) - 1))
        for row in lines[2:]:
            cols = [c.strip() for c in row.split("|")[1:-1]]
            if len(cols) <= max(name_idx, desc_idx):
                continue
            raw_name = cols[name_idx].strip("` ")
            names = re.findall(r"`([a-zA-Z0-9_-]+)`", raw_name) or re.findall(r"\b([a-z][a-z0-9_-]+)\b", raw_name)
            desc = re.sub(r"\*\*([^*]+)\*\*", r"\1", cols[desc_idx])
            for n in names:
                fid = n.lower().replace("_", "-")
                if valid_id.match(fid):
                    features[fid] = desc or features.get(fid, "")
    return features


def rules_for_feature(feature_id: str, rules: list[str]) -> list[str]:
    if not rules:
        return []
    # Keywords matched against README rules (Portuguese and English).
    keys = {
        "auth": ("auth", "login", "sessão", "sessao", "session", "registro", "sign up", "sign-up", "signup", "google", "gov.br"),
        "account": ("conta", "account", "pdf", "encerr", "clos", "wipe", "privacidade", "privacy"),
        "child": ("criança", "crianca", "child", "marco", "milestone", "perfil", "profile", "ativa", "active"),
        "registry": ("evento", "event", "formul", "form", "registr"),
        "home": ("home", "resumo", "summary", "humor", "mood"),
        "timeline": ("timeline", "histórico", "historico", "history", "cronol", "chronolog"),
        "care": ("cuidado", "care", "emergência", "emergencia", "emergency", "conquista", "achievement"),
        "sharing": ("compartilh", "shar", "convite", "invit", "profissional", "professional", "vínculo", "vinculo", "link"),
        "notifications": ("alerta", "alert", "notifica", "notif", "agenda do dia", "daily agenda", "humor", "mood"),
        "evolution": ("evolu", "insight"),
        "reports": ("relat", "report", "export"),
        "schedule": ("agenda", "schedul", "medica"),
        "ai": ("assistente", "assistant", "insight", "orientação médica", "medical guidance"),
        "community": ("comunidade", "community", "estático", "estatico", "static"),
        "onboarding": ("onboarding", "inicial", "initial"),
        "splash": ("splash", "bootstrap"),
    }
    kws = keys.get(feature_id, (feature_id.replace("-", " "),))
    matched = [r for r in rules if any(k in r.lower() for k in kws)]
    return matched if matched else rules[:2]


def discover_features_deep(repo: Path, stack: dict[str, bool], table: dict[str, str]) -> list[tuple[str, str, str]]:
    items: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    def add(fid: str, code: str, desc: str = "", status: str = "stable") -> None:
        fid = fid.lower().replace("_", "-")
        if fid in seen or fid in ("example", "templates", "bin", "obj"):
            return
        if "/bin" in code.replace("\\", "/") or "/obj" in code.replace("\\", "/"):
            return
        seen.add(fid)
        items.append((fid, code, table.get(fid, desc) or desc or f"Module `{code}`"))

    if stack["flutter"]:
        feat = repo / "lib" / "features"
        if feat.is_dir():
            for d in sorted(feat.iterdir()):
                if d.is_dir():
                    add(d.name, f"lib/features/{d.name}", table.get(d.name, ""))
        # flutter: do not enumerate csproj/android as features

    elif stack["dotnet"]:
        modules = sorted(repo.rglob("*Module.cs"))
        if modules and ("Flow" in repo.name or "flow" in str(repo).lower()):
            for m in modules:
                if any(x in m.parts for x in fill.SKIP_DIRS):
                    continue
                rel = m.parent.relative_to(repo)
                fid = "-".join(p.lower() for p in rel.parts[-2:]) if len(rel.parts) >= 2 else m.parent.name.lower()
                add(fid, str(rel), f"API module {m.stem}")
        else:
            # library/app: one feature per project mirroring src, or a single core
            test_projs = [p for p in repo.rglob("*Tests*.csproj") if not any(x in p.parts for x in fill.SKIP_DIRS)]
            src_projs = [
                p
                for p in repo.rglob("*.csproj")
                if not any(x in p.parts for x in fill.SKIP_DIRS)
                and not p.stem.endswith(".Tests")
                and "Test" not in p.stem
            ]
            if len(src_projs) <= 8:
                for csproj in sorted(src_projs)[:8]:
                    rel = csproj.parent.relative_to(repo)
                    fid = csproj.stem.replace(".", "-").lower()
                    add(fid, str(rel), table.get(fid, f"Project {csproj.stem}"))
            else:
                add(repo.name.lower().replace(".", "-"), ".", table.get(repo.name.lower(), f"Solution {repo.name}"))

    apis = repo / "Apis"
    if apis.is_dir() and not any(x[1].startswith("Apis/Services/Features") for x in items):
        for d in sorted(apis.iterdir()):
            if d.is_dir() and d.name not in fill.SKIP_DIRS:
                add(d.name.lower(), f"Apis/{d.name}", f"Layer {d.name}")

    if stack["docs_only"]:
        for doc in sorted((repo / "docs").rglob("*.md")):
            if doc.name.lower() in ("readme.md", "template.md"):
                continue
            fid = doc.stem.lower().replace(" ", "-")
            add(fid, str(doc.parent.relative_to(repo)), doc.stem)

    # design-patterns / solid-principles: src/1-Creational/Factory
    src = repo / "src"
    if src.is_dir() and not stack["flutter"] and not stack["dotnet"]:
        for cat in sorted(src.iterdir()):
            if not cat.is_dir() or not re.match(r"\d+-", cat.name):
                continue
            for sub in sorted(cat.iterdir()):
                if sub.is_dir() and sub.name not in ("bin", "obj"):
                    fid = f"{cat.name.lower()}-{sub.name.lower()}"
                    add(fid, str(sub.relative_to(repo)), f"{cat.name} / {sub.name}")

    for fid, desc in table.items():
        if fid not in seen:
            code = table.get("_code_" + fid, f"src/{fid}")
            add(fid, code, desc)

    if not items:
        add("core", ".", "Repository core")

    return items


def write_feature_specs(
    harness: Path,
    repo: Path,
    stack: dict[str, bool],
    fid: str,
    code: str,
    description: str,
    business_rules: list[str],
    limitations: list[str],
    unit_tests: list[UnitTest],
) -> None:
    dest = harness / "Specification" / "features" / fid
    dest.mkdir(parents=True, exist_ok=True)

    local_rules = rules_for_feature(fid, business_rules)
    global_rules = business_rules[:8]

    # Functional requirements: FR-xx, numbered sequentially (matches Specification/templates/requirements.md).
    fr_bodies = ([description] if description else []) + local_rules[:6]
    rf_text = "\n".join(f"{i}. FR-{i:02d} — {body}" for i, body in enumerate(fr_bodies, 1))

    write(
        dest / "requirements.md",
        f"""# Requirements — {fid}

| Field | Value |
|-------|-------|
| Feature | {fid} |
| Status | stable |
| Code | `{code}` |
| Owners | engineering |
| Updated | {date.today().isoformat()} |

## Intent

{description or f"Behavior of module {fid} as described in the README and code."}

## Functional requirements

{rf_text}

## Non-functional requirements

- Baseline: `Governance/quality.md`, `Governance/security.md`
- Follow `Knowledge/architecture.md` and `Knowledge/standards.md`
- Changes require evidence in `acceptance.md`

## Global product rules (applicable)

{chr(10).join('- ' + r for r in global_rules) if global_rules else '- See README.md'}

## Out of scope

{chr(10).join('- ' + l for l in limitations[:5]) if limitations else '- Items marked in the README as roadmap/limitations'}

## Dependencies

- Knowledge: Architecture, Domain, Standards
- Code: `{code}`
""",
    )

    uc_rules = local_rules[:3] or [description or f"User interacts with {fid}"]
    ucs = []
    for i, r in enumerate(uc_rules, 1):
        ucs.append(
            f"""## UC-{i:02d} — Main flow

- **Actor:** user / system
- **Given** a valid context and rule: {r[:120]}
- **When** the main action of `{fid}` is executed
- **Then** the behavior described in the README/code holds without violating Governance
"""
        )
    write(dest / "use-cases.md", f"# Use Cases — {fid}\n\n" + "\n".join(ucs))

    write(
        dest / "acceptance.md",
        build_acceptance_md(repo, stack, fid, code, unit_tests, business_rules),
    )


def deep_fill_repo(repo: Path) -> int:
    harness = repo / ".ai-harness"
    if not harness.is_dir():
        return 0

    fill.fill_repo(repo)

    readme = fill.read_readme(repo)
    sections = parse_sections(readme)
    table = parse_feature_tables(readme)
    stack = fill.detect_stack(repo)
    business_rules = parse_bullets(first_section(sections, BUSINESS_RULES_SECTIONS))
    limitations = parse_bullets(first_section(sections, LIMITATIONS_SECTIONS))

    features = discover_features_deep(repo, stack, table)
    all_tests = discover_unit_tests(repo)
    test_map = map_tests_to_features(repo, features, all_tests)
    count = 0

    ex = harness / "Specification" / "features" / "example"
    if ex.is_dir():
        import shutil

        shutil.rmtree(ex)

    for fid, code, desc in features:
        write_feature_specs(
            harness, repo, stack, fid, code, desc, business_rules, limitations, test_map.get(fid, [])
        )
        count += 1

    write(
        harness / "Specification/features/index.md",
        f"""# Features — index

> Deepened on {date.today().isoformat()} ({count} features, {len(all_tests)} unit tests indexed).

| ID | Spec | Code | Status | Tests | Summary |
|----|------|--------|--------|--------|--------|
"""
        + "\n".join(
            f"| {fid} | [./{fid}/](./{fid}/) | `{code}` | stable | {len(test_map.get(fid, []))} | {(desc[:50] + '…') if len(desc) > 50 else desc} |"
            for fid, code, desc in features
        )
        + """

Each feature has `requirements.md`, `use-cases.md`, `acceptance.md` (**AC = unit tests**).
""",
    )

    # Knowledge enrichment
    arch_extra = first_section(sections, ARCHITECTURE_SECTIONS)
    stack_extra = first_section(sections, STACK_SECTIONS)
    if arch_extra or stack_extra:
        arch_path = harness / "Knowledge/architecture.md"
        base = arch_path.read_text(encoding="utf-8") if arch_path.exists() else ""
        write(
            arch_path,
            base
            + "\n\n## README details\n\n"
            + (("### Stack\n\n" + stack_extra + "\n\n") if stack_extra else "")
            + (("### Architecture\n\n" + arch_extra[:4000] + "\n") if arch_extra else ""),
        )

    if business_rules or limitations:
        dom_path = harness / "Knowledge/domain.md"
        base = dom_path.read_text(encoding="utf-8") if dom_path.exists() else ""
        gloss = "\n".join(f"| BR-{i:02d} | {r[:100]} |" for i, r in enumerate(business_rules, 1))
        lim = "\n".join(f"- {l}" for l in limitations[:10])
        write(
            dom_path,
            base
            + "\n\n## Business rules (README)\n\n| ID | Rule |\n|----|------|\n"
            + (gloss or "| — | — |")
            + "\n\n## Known limitations\n\n"
            + (lim or "- See README"),
        )

    if business_rules or limitations:
        sec = harness / "Governance/security.md"
        base = sec.read_text(encoding="utf-8") if sec.exists() else ""
        # security.md is not regenerated by fill: drop sections from a previous run (English or legacy
        # Portuguese titles) so re-running does not duplicate them.
        base = strip_sections(base, PRODUCT_SECURITY_SECTIONS)
        write(
            sec,
            base
            + "\n\n## Rules derived from the product\n\n"
            + "\n".join(f"- {r}" for r in business_rules[:12])
            + ("\n\n## Limitations / risks\n\n" + "\n".join(f"- {l}" for l in limitations[:8]) if limitations else ""),
        )

    return count


def main() -> int:
    base = fill.DEFAULT_WORKSPACE
    if len(sys.argv) > 1:
        repos = [Path(p).resolve() for p in sys.argv[1:]]
    else:
        repos = sorted(p.parent for p in base.rglob(".ai-harness") if p.is_dir())

    total_features = 0
    ok = 0
    for repo in repos:
        if fill.is_harness_kit(repo):
            print(f"[SKIP] {repo.name} — kit-template")
            continue
        n = deep_fill_repo(repo)
        if n:
            print(f"[OK] {repo.name} — {n} features")
            ok += 1
            total_features += n
        else:
            print(f"[SKIP] {repo.name}")

    print(f"\nRepos: {ok} | Total features: {total_features}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
