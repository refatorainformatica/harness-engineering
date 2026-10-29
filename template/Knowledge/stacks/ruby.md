# Stack pack — Ruby (Rails)

Complements [standards.md](../standards.md).

## Code docs (YARD)

- YARD comments in English on every class, module and method (public and private): summary + remarks (`@note`) (rule and exception in the baseline); `@param`, `@return`, `@raise`.
- Module namespace = folder (`app/features/<feature>/` → `Features::<Feature>`).

## Tests

- RSpec (or Minitest, if adopted) + `instance_double`/`webmock`/`travel_to`; `describe '#method'` + `it 'should <behavior> when <condition>'`.
- Unit specs without a real database where possible (`build_stubbed`); no `sleep`.
- Location: `spec/features/<feature>/` mirroring the code (system specs stay in `spec/system/`).

## Coverage

- SimpleCov with `simplecov-cobertura` formatter → `coverage/coverage.xml`; `minimum_coverage 80` per group.

## Logging

- `Rails.logger` with structured payloads (lograge / semantic_logger): `logger.info(message: 'processing order', order_id: id)`.
- Never interpolate (`"... #{id}"`) in the message; exceptions logged with class, message and backtrace fields.

## Declarations to preserve

- Validations, callbacks, associations, `attribute`, `enum`, `before_action`, `rescue_from`, strong-parameter permits, serializer `attributes`.

## Structure

- Feature: `app/features/<feature>/` (or `app/{controllers,services,models}/<feature>/`) — mirror the existing feature.
- Controllers and jobs only orchestrate; business rules in domain objects (POROs/value objects), not in callbacks or views.
