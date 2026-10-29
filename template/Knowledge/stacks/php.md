# Stack pack — PHP (Laravel / Symfony)

Complements [standards.md](../standards.md).

## Code docs (PHPDoc)

- `/** ... */` in English on every class, property, constant and method (public and private): summary + remarks (rule and exception in the baseline); `@param`, `@return`, `@throws` when the native types do not say it all.
- Interface and implementation docs identical.
- Namespace = folder (PSR-4: `App\Features\<Feature>`).

## Tests

- PHPUnit or Pest (whatever the project uses) + Mockery/PHPUnit mocks; Laravel: `Http::fake()`, `Queue::fake()`, `Storage::fake()`; Symfony: `KernelTestCase` only for integration.
- Class `{ClassName}Test`; method `test_method_name_should_expected_behavior_when_condition` (or `#[Test]` + camelCase with the same pattern).
- Unit tests without a real database; `Carbon::setTestNow()` / `ClockInterface` for time; no `sleep()`.
- Location: `tests/Unit/Features/<Feature>/`.

## Coverage

- `phpunit --coverage-cobertura=coverage.xml` (Xdebug or PCOV) / `pest --coverage --min=80`; ≥ 80% per package/module.

## Logging

- PSR-3 logger (Monolog) with context arrays: `$logger->info('Processing order {orderId}', ['orderId' => $id])`.
- Never interpolate (`"... $id"`) or concatenate in the message; exception in the context (`['exception' => $e]`).

## Attributes / annotations to preserve

- PHP attributes and annotations: `#[Route]`, `#[ORM\Column]`, `#[Assert\NotBlank]`, `#[AsCommand]`, Laravel `$fillable`/`$casts`/`$hidden`.

## Structure

- Feature: `app/Features/<Feature>/` (Http/Controllers, Actions/UseCases, Domain, Repositories, Services, `<Feature>ServiceProvider`) — mirror the existing feature.
- Controllers and jobs only orchestrate; rules in domain entities/value objects, not in Eloquent models' controllers or Blade views.
