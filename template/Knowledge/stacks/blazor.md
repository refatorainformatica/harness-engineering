# Stack pack — Blazor

Layer on top of [dotnet.md](./dotnet.md) (read both). Complements [standards.md](../standards.md).

## Code docs

- Components: XML doc in the code-behind (`.razor.cs`) or in the `@code` block; every `[Parameter]`, `[CascadingParameter]`, `EventCallback` and lifecycle method with summary + remarks.

## Tests

- bUnit + xUnit (+ Moq/FluentAssertions): `{Component}Tests` in `tests/**/Features/<Name>/`.
- Rendering and interaction via `TestContext`; injected services mocked; no `Task.Delay` — use `WaitForState`/`WaitForAssertion`.

## Coverage

- Same as `dotnet.md` (coverlet); components count as testable artifacts.

## Logging

- Injected `ILogger<T>` (`@inject ILogger<MyComponent> Logger`) with message templates — never interpolation.

## Attributes / directives

- Preserve `[Parameter]`, `[CascadingParameter]`, `[Inject]`, `[SupplyParameterFromQuery]`, `@page`, `@attribute [Authorize]`, `@rendermode`, `@inject`.

## Structure

- The feature's components, pages and services in `Features/<Name>/` (or `Components/Features/<Name>/`); lean components — logic in feature services, not in `@code`.
