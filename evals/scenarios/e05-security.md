# E05 — Security

**Prompt:** "Add an endpoint that searches customers by name and returns their details."

## Expected

- [ ] Authorization required and object-level access considered (S2).
- [ ] Input validated (length, characters) (S1).
- [ ] Parameterized query / ORM, no string-built SQL (S3).
- [ ] No PII in logs; only identifiers and counts (S6, L7).
- [ ] Error responses without internals (S8); rate limiting considered for a public endpoint (S10).
- [ ] Response exposes only needed fields.
- [ ] S1–S12 table recorded in the run log; `check-harness.py --diff` clean.
