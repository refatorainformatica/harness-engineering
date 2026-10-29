#!/usr/bin/env python3
"""Fill .ai-harness/ with data inferred from the repository (the target project, not this kit)."""

from __future__ import annotations

import json
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
DEFAULT_WORKSPACE = Path.cwd()


def is_harness_kit(repo: Path) -> bool:
    """True if the path is this template kit (not a consuming project)."""
    return (repo / "template" / "agents.md").is_file() and (repo / "scripts" / "init-harness.sh").is_file()

HARNESS_PROJECT_START = "<!-- HARNESS:PROJECT-START -->"
HARNESS_PROJECT_END = "<!-- HARNESS:PROJECT-END -->"

# Generated section titles (English) -> titles written by the legacy Portuguese kit.
# Used so that re-running fill/enrich on an old project replaces the old section instead of duplicating it.
LEGACY_SECTION_TITLES: dict[str, tuple[str, ...]] = {
    "Stack and commands (generated)": ("Stack e comandos (gerado)",),
    "Project (detected)": ("Projeto (detectado)",),
}

# Heading that marks the canonical standards.md (new English heading + legacy Portuguese one).
STANDARDS_FEATURE_HEADINGS = ("Feature-first organization", "Organização por feature")


def read_readme(repo: Path) -> str:
    for name in ("README.md", "readme.md", "Readme.md"):
        p = repo / name
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return ""


def readme_summary(text: str) -> tuple[str, str]:
    # Strip common HTML banners
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
    vision = " ".join(body[:4]).strip() or "Project documented in README.md."
    return title or "Project", vision[:800]


def _first(repo: Path, pattern: str) -> Path | None:
    for path in repo.glob(pattern):
        if not SKIP_DIRS & set(path.relative_to(repo).parts):
            return path
    return None


def _package_deps(repo: Path) -> set[str]:
    deps: set[str] = set()
    for pkg in [repo / "package.json", *repo.glob("*/package.json"), *repo.glob("*/*/package.json")]:
        if not pkg.is_file() or SKIP_DIRS & set(pkg.relative_to(repo).parts):
            continue
        try:
            data = json.loads(pkg.read_text(encoding="utf-8", errors="replace"))
        except ValueError:
            continue
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            deps.update((data.get(key) or {}).keys())
    return deps


def _text_of(repo: Path, patterns: list[str], limit: int = 200) -> str:
    chunks: list[str] = []
    for pattern in patterns:
        for path in repo.glob(pattern):
            if SKIP_DIRS & set(path.relative_to(repo).parts) or not path.is_file():
                continue
            chunks.append(path.read_text(encoding="utf-8", errors="replace"))
            if len(chunks) >= limit:
                return "\n".join(chunks)
    return "\n".join(chunks)


def detect_cloud(repo: Path, deps: set[str], csproj_text: str) -> dict[str, bool]:
    """DevOps + cloud providers (AWS / Azure / GCP) from IaC, pipelines and SDKs."""
    tf = _text_of(repo, ["**/*.tf"])
    manifests = _text_of(repo, ["requirements*.txt", "pyproject.toml", "pom.xml", "build.gradle*", "**/build.gradle*"], 50)
    all_deps = " ".join(deps) + " " + csproj_text + " " + manifests
    has = lambda *patterns: any(_first(repo, p) for p in patterns)  # noqa: E731
    aws = (
        'provider "aws"' in tf
        or has("cdk.json", "serverless.yml", "samconfig.toml", "buildspec.yml", "**/buildspec.yml")
        or any(k in all_deps for k in ("@aws-sdk/", "aws-cdk", "AWSSDK.", "boto3", "software.amazon.awssdk", "com.amazonaws"))
    )
    azure = (
        'provider "azurerm"' in tf
        or 'provider "azapi"' in tf
        or has("**/*.bicep", "azure-pipelines.yml", "azure.yaml", "**/azure-pipelines*.yml")
        or any(k in all_deps for k in ("@azure/", "Azure.", "Microsoft.Azure.", "azure-", "com.azure"))
    )
    gcp = (
        'provider "google"' in tf
        or has("cloudbuild.yaml", "cloudbuild.yml", "app.yaml", "**/cloudbuild.yaml")
        or any(k in all_deps for k in ("@google-cloud/", "Google.Cloud.", "google-cloud-", "com.google.cloud", "firebase-admin"))
    )
    devops = (
        aws or azure or gcp or bool(tf)
        or has("Dockerfile", "**/Dockerfile", "docker-compose.yml", "compose.yaml", "**/Chart.yaml",
               "kustomization.yaml", "**/kustomization.yaml", ".github/workflows/*.yml", ".gitlab-ci.yml", "Jenkinsfile")
    )
    oci = (
        'provider "oci"' in tf
        or any(k in all_deps for k in ("oci-sdk", "oci-common", "com.oracle.oci.sdk", "OCI.DotNetSDK", "\noci\n", "oci=="))
    )
    devops = devops or oci
    return {"devops": devops, "aws": aws, "azure": azure, "gcp": gcp, "oci": oci}


def detect_extra(repo: Path, deps: set[str]) -> dict[str, bool]:
    """Stacks beyond the original set: Go, Rust, PHP, Ruby, Vue, React Native, Android, iOS, database, data/ML."""
    has = lambda *patterns: any(_first(repo, p) for p in patterns)  # noqa: E731
    gradle = _text_of(repo, ["build.gradle*", "*/build.gradle*", "settings.gradle*"], 30)
    py_manifests = _text_of(repo, ["requirements*.txt", "pyproject.toml", "setup.py"], 20).lower()
    return {
        "go": has("go.mod", "*/go.mod"),
        "rust": has("Cargo.toml", "*/Cargo.toml"),
        "php": has("composer.json", "*/composer.json"),
        "ruby": has("Gemfile", "*/Gemfile"),
        "vue": bool({"vue", "nuxt"} & deps),
        "react_native": bool({"react-native", "expo"} & deps),
        "android": has("**/AndroidManifest.xml") or "com.android.application" in gradle or "com.android.library" in gradle,
        "ios": has("*.xcodeproj", "*/*.xcodeproj", "*.xcworkspace", "Package.swift", "Podfile", "*/Podfile"),
        "database": has(
            "flyway.conf", "**/db/migration/*.sql", "**/changelog/*.xml", "**/db.changelog-master.*", "**/Migrations/*.cs",
            "alembic.ini", "**/migrations/*.py", "**/prisma/schema.prisma", "db/migrate/*.rb", "knexfile.*",
            "**/migrations/*.sql", "**/migrations/*.up.sql",
        ),
        "data": has("dbt_project.yml", "*/dbt_project.yml", "**/*.ipynb", "**/dags/*.py")
        or any(k in py_manifests for k in ("pyspark", "apache-airflow", "dagster", "prefect", "dbt-core", "scikit-learn", "torch", "mlflow")),
    }


# Per-stack facts for the stacks added by detect_extra (and OCI): stack row, test tool, validation tool, code root.
EXTRA_STACKS = [
    ("go", "| Backend | Go |", ("go.test", "go test ./..."), ("go.vet", "go vet ./..."), "internal/features/<feature>/"),
    ("rust", "| Backend | Rust |", ("rust.test", "cargo test"), ("rust.clippy", "cargo clippy -- -D warnings"), "src/features/<feature>/"),
    ("php", "| Backend | PHP (Laravel / Symfony) |", ("php.test", "vendor/bin/phpunit"), ("php.stan", "vendor/bin/phpstan analyse"), "app/Features/<Feature>/"),
    ("ruby", "| Backend | Ruby / Rails |", ("ruby.test", "bundle exec rspec"), ("ruby.lint", "bundle exec rubocop"), "app/features/<feature>/"),
    ("vue", "| Frontend | Vue / Nuxt |", None, None, "src/features/<id>/"),
    ("react_native", "| Mobile | React Native |", None, None, "src/features/<id>/"),
    ("android", "| Mobile | Android (Kotlin) |", ("android.test", "./gradlew testDebugUnitTest"), ("android.lint", "./gradlew lint"), "feature/<feature>/"),
    ("ios", "| Mobile | iOS (Swift) |", ("ios.test", "xcodebuild test -scheme <Scheme> -destination '<simulator>' -enableCodeCoverage YES"), ("ios.lint", "swiftlint"), "<App>/Features/<Feature>/"),
    ("database", "| Data | Schema migrations |", None, ("db.migrate.validate", "<migration tool> validate  # e.g. flyway validate, alembic check"), None),
    ("data", "| Data | dbt / Spark / notebooks / ML |", ("data.test", "dbt test --target dev && pytest"), ("data.build", "dbt build --select state:modified+ --target dev"), None),
    ("oci", "| Cloud | Oracle Cloud (OCI) |", None, None, None),
]


def detect_stack(repo: Path) -> dict[str, bool]:
    deps = _package_deps(repo)
    csproj = [p for p in repo.glob("**/*.csproj") if not SKIP_DIRS & set(p.relative_to(repo).parts)][:20]
    csproj_text = " ".join(p.read_text(encoding="utf-8", errors="replace") for p in csproj)
    has_package_json = bool(_first(repo, "package.json") or _first(repo, "*/package.json") or _first(repo, "*/*/package.json"))
    return {
        "dotnet": bool(list(repo.glob("*.sln")) + list(repo.glob("*.slnx")) + csproj[:1]),
        "blazor": bool(_first(repo, "**/*.razor")) or "Microsoft.AspNetCore.Components" in csproj_text,
        "java": bool(_first(repo, "pom.xml") or _first(repo, "build.gradle") or _first(repo, "build.gradle.kts")
                     or _first(repo, "*/pom.xml") or _first(repo, "*/build.gradle*")),
        "flutter": (repo / "pubspec.yaml").exists(),
        "node": has_package_json,
        "typescript": has_package_json or bool(_first(repo, "tsconfig.json")),
        "angular": bool(_first(repo, "angular.json") or _first(repo, "*/angular.json")) or "@angular/core" in deps,
        "react": "react" in deps,
        "node_backend": bool({"express", "fastify", "@nestjs/core", "koa", "@hapi/hapi"} & deps),
        "python": (repo / "pyproject.toml").exists() or (repo / "requirements.txt").exists() or (repo / "setup.py").exists(),
        **detect_cloud(repo, deps, csproj_text),
        **detect_extra(repo, deps),
        "docker": (repo / "docker-compose.yml").exists() or (repo / "Dockerfile").exists(),
        "docs_only": (repo / "docs").is_dir() and not list(repo.glob("**/*.csproj"))[:3] and not (repo / "pubspec.yaml").exists(),
        "landing": (repo / "index.html").exists() and (repo / "css").is_dir(),
    }


STACK_PACKS = [
    ("dotnet", "dotnet.md"),
    ("blazor", "blazor.md"),
    ("java", "java.md"),
    ("typescript", "typescript.md"),
    ("node_backend", "node.md"),
    ("angular", "angular.md"),
    ("react", "react.md"),
    ("flutter", "flutter.md"),
    ("python", "python.md"),
    ("go", "go.md"),
    ("rust", "rust.md"),
    ("php", "php.md"),
    ("ruby", "ruby.md"),
    ("vue", "vue.md"),
    ("react_native", "react-native.md"),
    ("android", "android.md"),
    ("ios", "ios.md"),
    ("database", "database.md"),
    ("data", "data.md"),
    ("devops", "devops.md"),
    ("aws", "aws.md"),
    ("azure", "azure.md"),
    ("gcp", "gcp.md"),
    ("oci", "oci.md"),
]


def stack_packs(stack: dict[str, bool]) -> list[str]:
    """Packs from `Knowledge/stacks/` that apply to the detected stack (base + layers)."""
    return [pack for key, pack in STACK_PACKS if stack.get(key)]


def packs_markdown(stack: dict[str, bool]) -> str:
    packs = stack_packs(stack)
    if not packs:
        return "- No pack detected — copy one from `Knowledge/stacks/` as a model (see `stacks/readme.md`)."
    return "\n".join(f"- `Knowledge/stacks/{p}`" for p in packs)


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


def _section_pattern(title: str) -> re.Pattern[str]:
    """Match an unmarked `## <title>` section up to the next `## ` heading (or end of file)."""
    return re.compile(rf"^## {re.escape(title)}[ \t]*\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)


def upsert_project_section(path: Path, title: str, body: str) -> None:
    """Insert or replace the generated overlay without wiping canonical template rules.

    Replacement order: the `HARNESS:PROJECT-*` marker block; otherwise an unmarked section with the
    same title or its legacy Portuguese title (projects installed with the old kit); otherwise append.
    """
    block = (
        f"{HARNESS_PROJECT_START}\n"
        f"## {title}\n\n"
        f"{body.rstrip()}\n"
        f"{HARNESS_PROJECT_END}\n"
    )
    if not path.is_file():
        write(path, block)
        return
    existing = path.read_text(encoding="utf-8", errors="replace")
    if HARNESS_PROJECT_START in existing and HARNESS_PROJECT_END in existing:
        pre = existing.split(HARNESS_PROJECT_START)[0].rstrip()
        post = existing.split(HARNESS_PROJECT_END, 1)[1]
        text = pre + "\n\n" + block + post.lstrip("\n")
    else:
        text = None
        for candidate in (title, *LEGACY_SECTION_TITLES.get(title, ())):
            match = _section_pattern(candidate).search(existing)
            if match:
                pre = existing[: match.start()].rstrip()
                post = existing[match.end():].lstrip("\n")
                text = pre + "\n\n" + block + ("\n" + post if post else "")
                break
        if text is None:
            text = existing.rstrip() + "\n\n" + block
    write(path, text)


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
        arch_style.append("Documentation / framework repository")
    if stack["landing"]:
        arch_style.append("Static site (HTML/CSS/JS)")
    if not arch_style:
        arch_style.append("See README.md and the repository folders")

    stack_rows = []
    if stack["dotnet"]:
        stack_rows.append(f"| Runtime | .NET ({sln or 'csproj'}) |")
    if stack["flutter"]:
        stack_rows.append("| UI | Flutter / Dart |")
    if stack["blazor"]:
        stack_rows.append("| UI | Blazor |")
    if stack["java"]:
        stack_rows.append("| Backend | Java / Kotlin (JVM) |")
    if stack["angular"]:
        stack_rows.append("| Frontend | Angular |")
    if stack["react"]:
        stack_rows.append("| Frontend | React |")
    if stack["node_backend"]:
        stack_rows.append("| Backend | Node.js |")
    elif stack["node"] and not (stack["angular"] or stack["react"]):
        stack_rows.append("| Frontend / tooling | Node.js |")
    if stack["python"]:
        stack_rows.append("| Runtime | Python |")
    if stack["docker"]:
        stack_rows.append("| Containers | Docker / docker-compose |")
    for key, row, _test, _lint, _root in EXTRA_STACKS:
        if stack.get(key):
            stack_rows.append(row)
    stack_rows.append(f"| Harness | `.ai-harness/` |")

    feature_table = ""
    if features:
        rows = []
        for fid, code, status in features:
            rows.append(f"| {fid} | [./{fid}/](./{fid}/) | `{code}` | {status} | summary in README / code |")
        feature_table = "\n".join(rows)
    else:
        feature_table = "| core | [./core/](./core/) | `.` | planned | Fill in as the project evolves |"

    write(
        harness / "Knowledge/architecture.md",
        f"""# Architecture — {name}

> Generated automatically on {date.today().isoformat()}. Review and refine.

## Style

{chr(10).join('- ' + s for s in arch_style)}

**Feature-first (mandatory):** code and test folders follow the business capability. Technical layers live **inside** the feature. See `standards.md`.

**OSS-first:** open source → self-host → proprietary cloud only with an ADR (`Governance/cost.md`).

**Rich domain** if DDD/Clean Architecture: behavior lives in the entities; Application only orchestrates.

## Structure (repository top level)

```text
{tree}
```

## Main code root

`{root.relative_to(repo) if root != repo else '.'}`

## Detected stack

| Layer | Technology |
|-------|------------|
{chr(10).join(stack_rows)}

## Harness ↔ code mapping

| Spec feature | Code |
|--------------|------|
| `Specification/features/<id>/` | matching module/folder |

## Cross-cutting (fill in)

| Piece | Role |
|-------|------|
| DI | see README / code |
| Auth | see README / code |
| Persistence | see README / code |
| Observability | see README / code |

## Out of architectural scope (current)

- See README.md and open issues
""",
    )

    write(
        harness / "Knowledge/domain.md",
        f"""# Domain — {name}

## Product vision (summary)

{vision}

## Product / purpose

**{title}** — see README.md for full details.

## Glossary (ubiquitous language)

| Term | Meaning |
|------|---------|
| Harness | `.ai-harness/` structure of this repository |
| Feature | Unit in `Specification/features/<id>/` |
| Run | Agent execution in `Runtime/state/runs/` |

> Add domain terms as the product evolves.

## Criticality

- Profile: {"assistive AI" if "ai" in name.lower() else "traditional software"}
- Risk: medium (review with the team)
- Owner: engineering
""",
    )

    extra_tests = [t for key, _r, t, _l, _c in EXTRA_STACKS if t and stack.get(key)]
    test_cmd = "dotnet test" if stack["dotnet"] else (extra_tests[0][1] if extra_tests else "see README")
    if sln:
        test_cmd = f"dotnet test {sln}"
    elif stack["flutter"]:
        test_cmd = "flutter test"
    elif stack["node"]:
        test_cmd = "npm test"
    elif stack["java"]:
        test_cmd = "./mvnw test" if (repo / "pom.xml").exists() else "./gradlew test"
    elif stack["python"]:
        test_cmd = "pytest"

    build_cmd = f"dotnet build {sln}" if sln else ("flutter build apk --debug" if stack["flutter"] else "see README")

    stack_body = f"""- Stack: {', '.join(k for k, v in stack.items() if v and k not in ('docs_only', 'landing', 'node_backend')) or 'see README'}
- Active stack packs (read only these):
{packs_markdown(stack)}
- Formatting: the stack formatter (`dotnet format`, `dart format`, etc.)
- Tests: `{test_cmd}` (feature folder)
- Build:

```bash
{build_cmd}
```

- Commit/push: **ask** (`Governance/permissions.md`)
- Deps: OSS first (`Governance/cost.md`)
"""
    standards_path = harness / "Knowledge/standards.md"
    standards_text = standards_path.read_text(encoding="utf-8", errors="replace") if standards_path.is_file() else ""
    if any(h in standards_text for h in STANDARDS_FEATURE_HEADINGS):
        upsert_project_section(standards_path, "Stack and commands (generated)", stack_body)
    else:
        write(
            standards_path,
            f"""# Standards — {name}

> Generated automatically. Align with the project README.

## Feature-first organization (mandatory)

Code and tests **always** organized by business capability. See the kit template.

## Stack and commands (generated)

{stack_body}
""",
        )

    # Tools — stack-specific sections
    build_tools = """## Generic / files

| ID | Action | Notes |
|----|------|-------|
| `fs.read` | Read files | auto |
| `fs.write` | Edit within scope | auto |
| `fs.delete` | Delete file | **ask** |
| `fs.write.secrets` | Secrets | **deny** |
"""
    if stack["dotnet"]:
        build_tools += """
## .NET

| ID | Command | Notes |
|----|---------|-------|
| `dotnet.restore` | `dotnet restore` | auto |
| `dotnet.build` | `dotnet build` | auto |
| `dotnet.format` | `dotnet format` | auto (scope) |
| `dotnet.add.package` | `dotnet add package` | **ask** |
"""
    if stack["flutter"]:
        build_tools += """
## Flutter

| ID | Command | Notes |
|----|---------|-------|
| `flutter.pub.get` | `flutter pub get` | auto |
| `dart.format` | `dart format` | auto |
| `flutter.pub.add` | `flutter pub add` | **ask** |
| `flutter.pub.upgrade` | global upgrade | **deny** |
"""
    if stack["node"]:
        build_tools += """
## Node

| ID | Command | Notes |
|----|---------|-------|
| `node.install` | npm/pnpm/yarn install | auto |
| `node.build` | npm run build | auto |
| `node.add.dep` | add dependency | **ask** |
"""
    write(harness / "Tools/build.md", f"# Tools — Build\n\n{build_tools}")

    test_tools = "| ID | Command | Notes |\n|----|---------|-------|\n"
    if stack["dotnet"]:
        test_tools += f"| `dotnet.test` | `{test_cmd}` | auto |\n"
    if stack["flutter"]:
        test_tools += "| `flutter.test` | `flutter test` | auto |\n"
    if stack["node"]:
        test_tools += "| `node.test` | `npm test` | auto |\n"
    if stack["java"]:
        jvm = "./mvnw test" if (repo / "pom.xml").exists() else "./gradlew test"
        test_tools += f"| `jvm.test` | `{jvm}` | auto |\n"
    if stack["python"]:
        test_tools += "| `python.test` | `pytest` | auto |\n"
    for tool_id, cmd in extra_tests:
        test_tools += f"| `{tool_id}` | `{cmd}` | auto |\n"
    if not any(stack[k] for k in ("dotnet", "flutter", "node", "java", "python")) and not extra_tests:
        test_tools += "| `test.manual` | as per README | **ask** |\n"
    test_tools += (
        "\nNew tests: **always** under the feature folder (`standards.md`). "
        "AC-G* gap: minimal stub in the feature folder.\n"
    )
    write(harness / "Tools/test.md", f"# Tools — Test\n\n{test_tools}")

    val_tools = """| ID | Action | Notes |
|----|------|-------|
| `harness.check` | `python3 .ai-harness/Tools/bin/check-harness.py [--diff <base>]` | auto — structure + rules on the diff |
| `harness.coverage` | `python3 .ai-harness/Tools/bin/check-harness.py --coverage "<report glob>"` | auto — ≥ 80% line per testable artifact |
| `harness.check.hook` | `python3 .ai-harness/Tools/bin/check-harness.py --install-hook` | **ask** — installs the git pre-commit hook |
| `harness.spec.read` | Read `.ai-harness/**` | auto |
| `harness.spec.write` | Update specs | auto if changed |
| `harness.state.write` | Runtime/state | auto |
"""
    if stack["dotnet"]:
        val_tools += "| `dotnet.build` | validation build | auto |\n"
    if stack["flutter"]:
        val_tools += "| `flutter.analyze` | `flutter analyze` | auto |\n"
    if stack["typescript"]:
        val_tools += "| `node.lint` | `npm run lint` (if present) | auto |\n"
    if stack["java"]:
        jvm_build = "./mvnw -q verify -DskipTests" if (repo / "pom.xml").exists() else "./gradlew build -x test"
        val_tools += f"| `jvm.build` | `{jvm_build}` | auto |\n"
    if stack["python"]:
        val_tools += "| `python.lint` | `ruff check` (if adopted) | auto |\n"
    for key, _r, _t, lint, _c in EXTRA_STACKS:
        if lint and stack.get(key):
            val_tools += f"| `{lint[0]}` | `{lint[1]}` | auto |\n"
    write(harness / "Tools/validation.md", f"# Tools — Validation\n\n{val_tools}")

    upsert_project_section(
        harness / "Governance/architecture.md",
        "Project (detected)",
        f"- Style: {arch_style[0]}\n"
        "- Feature-first and OSS-first apply in this overlay too.\n"
        "- Structural changes → ADR; proprietary cloud → ADR (`cost.md`).\n",
    )
    upsert_project_section(
        harness / "Governance/quality.md",
        "Project (detected)",
        f"- Build: `{build_cmd}`\n"
        f"- Tests: `{test_cmd}` (feature scope; AC-T* or AC-G* + stub)\n"
        "- Evidence in `Specification/features/<id>/acceptance.md`\n",
    )

    write(
        harness / "Specification/features/index.md",
        f"""# Features — index

> Generated automatically on {date.today().isoformat()}.

| ID | Spec | Code | Status | Summary |
|----|------|--------|--------|--------|
{feature_table}

## Next step

For each critical feature, fill in `requirements.md`, `use-cases.md`, `acceptance.md`.
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
            for seed in ("- [ ] AC-01 — Use cases covered or tested", "- [ ] AC-01 — Use cases cobertos ou testados"):
                ac = ac.replace(seed, f"- [ ] AC-01 — Module `{code}` documented and tested")
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
        if is_harness_kit(repo):
            print(f"[SKIP] {repo.name} — kit-template")
            continue
        if not (repo / ".ai-harness").is_dir():
            print(f"[SKIP] {repo.name} — no .ai-harness")
            continue
        fill_repo(repo)
        print(f"[OK] {repo.name}")
        ok += 1
    print(f"\nFilled: {ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
