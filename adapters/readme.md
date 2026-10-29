# Adapters

The harness in `.ai-harness/` is **tool-agnostic**. Each adapter only points a specific tool at `.ai-harness/agents.md`. Install them with `scripts/init-harness.sh` in the **target project**, not in this kit.

- Single source: [source/harness.md](./source/harness.md). Generated files: `python3 scripts/build-adapters.py` (never edit them by hand).
- Destination names per tool: [../docs/ide-adapters.md](../docs/ide-adapters.md).
