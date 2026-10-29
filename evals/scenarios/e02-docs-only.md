# E02 — Documentation pass

**Setup:** a class with partial docs, Portuguese log messages and serialization attributes (e.g. `[JsonPropertyName]`, `@JsonProperty`).

**Prompt:** "Document this file."

## Expected

- [ ] The **whole** file documented (fields, properties, constructors, methods, enum values), old docs replaced.
- [ ] Summary + remarks on every member (simple-property exception applied conservatively).
- [ ] Docs in English, concise, no invented constraints.
- [ ] Log messages translated to English.
- [ ] Interface and implementation docs identical.
- [ ] No attribute/annotation removed; no logic changed (`check-harness.py --diff` clean).
- [ ] Namespace/package matches the folder (or the mismatch is reported).
