# Runtime — Loop

## States

| State | Meaning |
|-------|---------|
| `INIT` | Run created |
| `PLAN` | Plan recorded in state |
| `ACT` | Implementing (Developer) / deciding (Architect) |
| `VERIFY` | Tester / validation |
| `REVIEW` | Reviewer |
| `UPDATE_SPEC` | Specification/ADR aligned |
| `DONE` | Acceptance OK |
| `BLOCKED` | Needs the user |
| `FAILED` | Gate failed with no safe fix within scope |

## Loop

```
while state not in {DONE, BLOCKED, FAILED}:
  1. Read status.md
  2. Next CHECKLIST item
  3. One unit of work (allowed tool / active role)
  4. Record in the LOG (tool ID + role)
  5. Check whether code changed
  6. Update CHECKLIST + STATUS
  7. Acceptance OK → DONE; ask → BLOCKED; error with no fix → FAILED
```

## DONE

1. `harness.check` with no errors + final validation of all applicable rules (Standards + Governance) recorded in the LOG  
2. Security baseline S1–S12 and logging verification L1–L8 recorded in the log
3. Unit tests for every new/changed behavior; coverage ≥ 80% line on every testable artifact
4. Scope fulfilled  
5. Acceptance checked or justified  
6. Requested gates passed  
7. No deny action  
8. STATUS = DONE  

## BLOCKED

- ask without authorization  
- Existing business rule would change without confirmation  
- Ambiguous spec / conflict with Knowledge  
- Mixed WIP without sandbox  

## Anti-loop

- Max. ~12 iterations → BLOCKED with summary  
- Same failing command > 2 times → change approach  
- Do not expand scope to get unblocked  

## Execution bias (within the matrix)

- In `auto` steps: analysis that finds a problem within scope is followed **immediately** by editing — do not deliver only analysis/plan when the change is possible and allowed.
- Do not ask which files to process when the scope is already defined; do not generate repo inventories unless asked.
- Process in batches (up to ~10 files per iteration), applying the changes in each batch, until done or until an unrecoverable compilation error.
- Idempotency: keep a record of the files processed in the run (CHECKLIST/LOG) and do not touch them again without a new problem; explicitly skip what is already compliant.
- **Never** overrides `ask` / `deny` from `Governance/permissions.md` or the iteration limit.

## Relationship with the tool

Continue `auto` steps without asking "may I proceed"; stop only on ask/ambiguity. Report the `run-id` and state.
