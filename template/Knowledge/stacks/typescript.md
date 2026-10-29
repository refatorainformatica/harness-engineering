# Stack pack — TypeScript / JavaScript

Base for [node.md](./node.md), [angular.md](./angular.md) and [react.md](./react.md). Complements [standards.md](../standards.md).

## Code docs (TSDoc / JSDoc)

- `/** ... */` in English: summary + `@remarks` (rule and exception in the baseline); `@param`, `@returns`, `@throws`.
- Interface/type ↔ implementation with the same member docs.

## Tests

- The runner already adopted (Vitest / Jest / node:test); the runner's mocks.
- File `{subject}.test.ts` / `{subject}.spec.ts` under the feature folder; `describe('<Subject>')` + `it('should <behavior> when <condition>')`.
- Fake timers (`vi.useFakeTimers` / `jest.useFakeTimers`) instead of real waits; mocked HTTP (MSW, `HttpTestingController`, nock).

## Coverage

- Vitest (`--coverage`, v8/istanbul) or Jest (`--coverage`) with `lcov` + `cobertura` reporters; `coverageThreshold`/`thresholds` ≥ 80% lines per package.

## Logging

- Structured logger: `logger.info({ orderId }, 'Processing order')` — no template literal nor concatenation in the message.

## Decorators

- Preserve class and property decorators (framework, ORM, validation, DI).

## Structure

- Feature: `src/features/<id>/` (or the framework equivalent) — mirror the existing feature; no generic `utils/` with feature rules.
- The `tsconfig` `strict` setting is not loosened to "make it pass".
