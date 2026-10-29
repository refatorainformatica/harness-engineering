# E01 — New feature

**Prompt:** "Add the ability to cancel an order with a reason. Cancelled orders cannot be shipped."

## Expected

- [ ] A run was created and the `feature` workflow followed (run `log.md` exists).
- [ ] Spec created/updated in `Specification/features/<id>/` and registered in `index.md`.
- [ ] Code placed in the feature folder, mirroring the closest existing feature's layout.
- [ ] Rule lives in the domain (`order.Cancel(reason)`-style method with an invariant), not in the handler/controller.
- [ ] Unit tests added in the feature test folder, named per convention, covering success, validation failure, exception and edge case.
- [ ] Coverage ≥ 80% on the touched artifacts (report attached to the log).
- [ ] New/changed orchestrators log start, decision, outcome and failure with identifiers (L1–L8 recorded).
- [ ] Code docs (English) on new/changed members; affected `docs/` page updated.
- [ ] Security baseline S1–S12 recorded (authorization on the new operation, input validation).
- [ ] `check-harness.py --diff` reports no errors.
- [ ] No commit/push without being asked.
