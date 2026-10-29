# E04 — Handler helpers

**Setup:** a handler with several private helper methods and 300+ lines.

**Prompt:** "Clean up this handler."

## Expected

- [ ] Private helpers moved to a service (interface + implementation) inside the same feature, registered in the feature module and injected.
- [ ] The handler only orchestrates; business rules moved to the domain where applicable.
- [ ] Each extracted service has its own unit tests; coverage ≥ 80%.
- [ ] Behavior unchanged (existing tests green); attributes preserved.
- [ ] Logging kept/added per L1–L8.
