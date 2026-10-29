# Run state

- `runs/` is **gitignored** (ephemeral).
- `templates/` are versioned.
- Optional: `CURRENT` file with the active run-id (one line).

```text
Runtime/state/
├── readme.md
├── CURRENT
├── templates/
└── runs/<run-id>/
```
