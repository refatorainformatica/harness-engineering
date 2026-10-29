# Adoption guide — AI Engineering Harness

This repository is the **template**. Any other repository adopts the harness by installing `.ai-harness/` from here.

## 1. Install in the target project

From a clone of this kit:

```bash
./scripts/init-harness.sh /path/to/project MyApp                       # AGENTS.md adapter (default)
./scripts/init-harness.sh /path/to/project MyApp --adapters=copilot,claude
./scripts/init-harness.sh /path/to/project MyApp --adapters=none       # harness only
./scripts/init-harness.sh /path/to/project MyApp --enrich              # install + infer Knowledge/specs
```

- Creates the project folder if needed and copies `template/` → `<project>/.ai-harness/`.
- Installs the selected adapters under the file names each tool expects, never overwriting a project file that is not a harness file.
- Writes `.ai-harness/.kit-version` and the `.gitignore` entries for ephemeral runs.
- Does **not** copy this kit into the app.

## 2. Update from the template

When this kit evolves, in projects that already have the harness:

```bash
./scripts/init-harness.sh /path/to/project --update
```

| Updates | Preserves |
|---------|-----------|
| `agents.md`, Agents (roles), Workflows, Governance, Tools (incl. `bin/check-harness.py`), Runtime, Specification templates | Knowledge `architecture` / `domain` / `standards` |
| Stack packs the project kept (all packs if it has none) | `Specification/features/` |
| Adapters, when `--adapters=` is passed | `Agents/project.md` |

The update also **migrates legacy upper-case file names** (kit < 1.1) to lower-case, including runs in progress; conflicting copies are kept as `<name>.legacy` for review. See [changelog.md](../changelog.md) for each version's migration notes.

Re-apply the stack overlay after an update:

```bash
python3 scripts/enrich-harness.py /path/to/project
```

## 3. Fill in Knowledge

By hand or:

```bash
python3 scripts/fill-harness.py /path/to/project
python3 scripts/deep-fill-harness.py /path/to/project
python3 scripts/enrich-harness.py /path/to/project
```

Without arguments the scripts work on `.ai-harness/` **in the current directory** (not in this kit).

| Script | Does |
|--------|------|
| `fill-harness.py` | Knowledge/Tools/index + stack overlay + active stack packs (never deletes canonical rules) |
| `deep-fill-harness.py` | Specs + **acceptance = unit tests** |
| `enrich-harness.py` | ADR, glossary, use cases, Governance overlay, `Agents/project.md`, AC-G* stubs in the feature folder |

| File | Content |
|------|---------|
| `Knowledge/architecture.md` | Style and real folders |
| `Knowledge/domain.md` | Glossary, contexts, criticality |
| `Knowledge/standards.md` | Code, tests, logging, docs, git, dependencies |
| `Knowledge/stacks/` | Stack packs — delete the ones the project does not use |
| `Knowledge/ADR/` | Lasting decisions (cloud provider, managed services, style) |

Canonical rules: [rules-baseline.md](./rules-baseline.md).

## 4. Governance, Tools and checks

- `Governance/*` — security (S1–S12), quality (unit tests, ≥ 80% coverage), architecture, cost, permissions.
- `Tools/*` — the real commands of your stack and infra (remove what you do not use).
- Turn on the automated checks in whatever runs your pipeline:

```bash
python3 .ai-harness/Tools/bin/check-harness.py --diff origin/main
python3 .ai-harness/Tools/bin/check-harness.py --coverage "<coverage report glob>"
python3 .ai-harness/Tools/bin/check-harness.py --install-hook      # optional git pre-commit
```

## 5. First features

1. Copy `Specification/templates/` → `features/<id>/`
2. Register it in `features/index.md`
3. Remove `features/example`
4. Follow `Workflows/feature.md`

## 6. Validate with any agent

> Read `.ai-harness/agents.md`. Which workflow and role would you use for feature X?

Expected: it cites Runtime, Specification, Agents, the active stack packs and permissions. For a measurable check, run the scenarios in [evals/](../evals/readme.md).

## Operations

| Event | Path |
|-------|------|
| New feature | `Workflows/feature.md` |
| Bug | `Workflows/bug.md` |
| Refactoring | `Workflows/refactoring.md` |
| Migration | `Workflows/migration.md` |
| Infrastructure / pipeline / cloud | `Workflows/infra.md` |
| Architectural decision | `Knowledge/ADR/` + Architect |
| Update the kit rules | `init-harness.sh <project> --update` |

## Anti-patterns

- Copying this whole repository into the product (use the script)
- Empty harness (Knowledge never filled in)
- Tools for a stack the project does not use; every stack pack left active
- Implementing without acceptance or without unit tests
- A "do-everything" agent that never declares its role
- Changing a business rule without confirmation
- Commit/push without `ask`; infra changed outside IaC
