# Workflow — Refactoring

Improve structure **without** changing observable behavior (unless explicitly accepted).

## Steps

1. Run + CONTEXT (motivation, area, success metric).
2. Architect: refactoring boundaries; ADR if the style/pattern changes.
3. Capture the test baseline (Tester) **before**.
4. Developer: internal changes; do not change feature acceptance. Preserve class/property attributes; do not change logic; do not remove code in a way that breaks functionality.
5. Tester: same suite green; no new behaviors.
6. Reviewer: confirm "behavior-preserving".

## DoR

- [ ] Clear motivation and boundaries
- [ ] Safety-net suite (tests) identified

## DoD

- [ ] External behavior unchanged
- [ ] Relevant tests passing
- [ ] Attributes preserved; docs updated
- [ ] Final validation of all rules in the LOG
- [ ] Unit tests for every new/changed behavior; coverage ≥ 80% line on every testable artifact
- [ ] Security baseline S1–S12 verified (`Governance/security.md`) — evidence in the log
- [ ] Logging verification L1–L8 (`Knowledge/standards.md#logging`) — evidence in the log
- [ ] STATUS = DONE
