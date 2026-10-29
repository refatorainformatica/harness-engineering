# AI Engineering Harness

Layer installed from the **template** (kit repository). Entrypoint: [agents.md](./agents.md).

```text
.ai-harness/
├── Knowledge/        # Stable system truth
├── Specification/    # What to deliver (per feature)
├── Agents/           # Roles (Architect, Developer, Reviewer, Tester)
├── Workflows/        # Feature, Bug, Refactoring, Migration
├── Tools/            # Build, Test, Git, Validation
├── Governance/       # Security, Quality, Architecture, Cost, Permissions
└── Runtime/          # Loop, runs, sandbox
```

## Entrypoint

Every agent starts at [agents.md](./agents.md).

## Capability checklist

| Pillar | Where |
|--------|-------|
| Knowledge | [Knowledge/](./Knowledge/) |
| Specification | [Specification/](./Specification/) |
| Agents | [Agents/](./Agents/) |
| Workflows | [Workflows/](./Workflows/) |
| Tools | [Tools/](./Tools/) |
| Governance | [Governance/](./Governance/) |
| Runtime | [Runtime/](./Runtime/) |

## Principles

- Spec before code — no clear acceptance → `BLOCKED`.
- AI produces; a human approves what the matrix marks as `ask`.
- Knowledge and Governance prevail over the agent's preference.
- The workflow chooses the role; the role does not invent the process.
