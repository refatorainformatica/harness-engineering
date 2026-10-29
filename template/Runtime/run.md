# Runtime — Start a run

## When to create

Every task that changes code or specs must have a run in `.ai-harness/Runtime/state/runs/`.

## Steps

1. `run-id`: `YYYYMMDD-HHMM-<slug>`
2. Create a folder with STATUS, CONTEXT, CHECKLIST, LOG (templates in `state/templates/`).
3. Choose Workflow + initial role (Agents).
4. Read Specification + Knowledge + permissions.
5. Enter the LOOP: `INIT` → `PLAN`.

## CONTEXT (minimum)

- User request
- Branch
- Workflow (`feature` \| `bug` \| `refactoring` \| `migration`)
- Feature id(s)
- Active role
- Gates / criticality
- Isolation: root or sandbox

## Close

- `DONE` — checklist + summary in the LOG
- `BLOCKED` / `FAILED` — clear reason in STATUS
