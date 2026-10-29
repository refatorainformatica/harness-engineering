# Tools

Catalog of actions the agent may trigger. Effective level: [Governance/permissions.md](../Governance/permissions.md).

| Area | File |
|------|------|
| Build | [build.md](./build.md) |
| Test | [test.md](./test.md) |
| Git | [git.md](./git.md) |
| Validation | [validation.md](./validation.md) |
| Infra / DevOps | [infra.md](./infra.md) |

## Conventions

- Stable **ID** — use it in the run LOG.
- Outside this catalog = **deny** or **ask** until explicit authorization.
- Remove unused stacks; add the project's real stack.

## Harness scripts

`bin/check-harness.py` — automatic rule check (`harness.check`). Only Python 3 + git; runs in any terminal, git hook or CI.

## AI tools

The harness does not depend on any tool. Optional adapters (installed by the kit) only point the agent to `agents.md` — they are not tools.
