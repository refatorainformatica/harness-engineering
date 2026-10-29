# Tools — Validation

| ID | Action | Notes |
|----|--------|-------|
| `lint` | linter / analyze on touched files | auto |
| `typecheck` | typecheck / compile dry | auto |
| `security.scan` | project SAST / dependency scan | **ask** if heavy or publishing a report |
| `harness.check` | `python3 .ai-harness/Tools/bin/check-harness.py [--diff <base>]` | auto — harness structure + rules on the diff |
| `harness.coverage` | `python3 .ai-harness/Tools/bin/check-harness.py --coverage "<report glob>"` | auto — ≥ 80% line per testable artifact |
| `harness.check.hook` | `python3 .ai-harness/Tools/bin/check-harness.py --install-hook` | **ask** — installs git pre-commit |
| `harness.spec.read` | Read `.ai-harness/**` | auto |
| `harness.spec.write` | Update Specification/Knowledge | auto if behavior/decision changed |
| `harness.state.write` | Write Runtime/state | auto |

Add company gates (policy-as-code, contract tests, etc.) with stable IDs.
