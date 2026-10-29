# Stack pack — Python

Frameworks: Django, FastAPI, Flask.

Complements [standards.md](../standards.md).

## Code docs (docstrings)

- Docstrings in English in the style already adopted (Google / NumPy / reST): summary on the first line + remarks section (rule and exception in the baseline).
- Packages/modules mirror the feature (`<pkg>/features/<id>/…`).

## Tests

- `pytest` + `unittest.mock` / `pytest-mock`.
- File `test_{subject}.py` under `tests/features/<id>/`; function `test_<method>_should_<behavior>_when_<condition>`.
- No `time.sleep`; injected clock or `freezegun`.

## Coverage

- `pytest --cov=<pkg> --cov-report=xml --cov-fail-under=80` → `coverage.xml` (Cobertura); ≥ 80% per package.

## Logging

- `logger.info("Processing order %s", order_id)` or `extra={...}` — never an f-string in the message.

## Decorators

- Preserve decorators (`@dataclass`, `@property`, `@field_validator`, framework routes, …).

## Structure

- Feature: `<pkg>/features/<id>/` (Django: one app per feature) — mirror the existing feature; views/routers only orchestrate, rules in the feature's domain/services.
- Command: `pytest tests/features/<id>/`.
