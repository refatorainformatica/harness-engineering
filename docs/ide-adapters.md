# Tool adapters

The harness (`.ai-harness/`) is the source of truth and does not depend on any tool. Adapters are optional, short pointers installed **in the project that adopts the template**, under the exact file name each tool looks for.

| ID | Tool | Destination in the project |
|----|------|----------------------------|
| `agents-md` (default) | Any agent that reads the open `AGENTS.md` convention | `AGENTS.md` |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` |
| `claude` | Claude Code | `CLAUDE.md` |
| `cursor` | Cursor | `.cursor/rules/harness-sdd.mdc` |
| `windsurf` | Windsurf | `.windsurfrules` |
| `continue` | Continue | `.continue/rules/harness-sdd.md` |
| `aider` | Aider | `CONVENTIONS.md` |
| `jetbrains` | JetBrains AI | `.aiassistant/rules/harness.md` |
| `all` / `none` | all / none | — |

```bash
./scripts/init-harness.sh ~/proj/api AcmeApi                          # AGENTS.md only
./scripts/init-harness.sh ~/proj/api AcmeApi --adapters=copilot,claude
./scripts/init-harness.sh ~/proj/demo Demo --adapters=all
./scripts/init-harness.sh ~/proj/lib Lib --adapters=none              # harness only
```

- Every adapter has the same body, generated from [adapters/source/harness.md](../adapters/source/harness.md) by `scripts/build-adapters.py`. Edit the source, never the generated files (`build-adapters.py --check` runs in `tests/run.sh`).
- An existing project file that is not a harness file (e.g. your own `AGENTS.md`) is **never overwritten**; the script prints a warning so you can add the pointer by hand.
- Adding a new tool: add an entry to `ADAPTERS` in `scripts/build-adapters.py` and a case in `install_adapter` in `scripts/init-harness.sh`.
