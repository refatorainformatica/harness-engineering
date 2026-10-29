# Stack pack — Angular

Layer on top of [typescript.md](./typescript.md) (read both).

## Code docs

- TSDoc on components, services, pipes and directives; every `input()`/`@Input`, `output()`/`@Output`, public signal and public method with summary + remarks.

## Tests

- The project's runner (Jasmine/Karma, Jest or Vitest) + `TestBed`; `{name}.spec.ts` next to the file, inside the feature.
- HTTP with `provideHttpClientTesting` / `HttpTestingController`; injected services mocked; `fakeAsync`/`tick` instead of real waits.

## Coverage

- `ng test --code-coverage` (Karma/Jest/Vitest) with `lcov`; ≥ 80% lines per app/library (`angular.json` / `karma.conf` thresholds).

## Logging

- The application's logging service with structured context — no `console.log` in production code; no template literal in the message.

## Decorators

- Preserve `@Component`, `@Injectable`, `@Directive`, `@Pipe`, `@NgModule`, `@Input`, `@Output`, `@HostListener`, `@ViewChild` and their metadata (`selector`, `standalone`, `providers`, …).

## Structure

- Feature: `src/app/features/<id>/` (components, services, models, routes) with lazy loading — mirror the existing feature.
- Lean components: logic and HTTP calls in feature services; state per the pattern already adopted (signals, NgRx…).
