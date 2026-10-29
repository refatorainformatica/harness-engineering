# Stack pack — .NET (C#)

Complements [standards.md](../standards.md). Layers: [blazor.md](./blazor.md).

## Code docs (XML documentation)

- `<summary>` + `<remarks>` on every public and private member (fields, properties, constructors, methods, enum values) — rule and exception in the baseline.
- Interface ↔ implementation: identical `<summary>`, `<remarks>`, `<param>`, `<returns>` and `<response>` (`<inheritdoc/>` only if the project already uses it).
- Namespace = physical folder relative to the project (`.csproj`).

## Tests

- xUnit + Moq + FluentAssertions (unless a pattern is already adopted: NUnit, MSTest, NSubstitute).
- Class `{ClassName}Tests`; method `MethodName_ShouldExpectedBehavior_WhenCondition`.
- Mock `DbContext`, repositories, `HttpClient`/handlers, brokers, filesystem, `TimeProvider`.
- `Thread.Sleep` / `Task.Delay` to synchronize tests is forbidden.
- Command: `dotnet test <sln> --filter FullyQualifiedName~Features.<Name>`.

## Coverage

- coverlet (`coverlet.collector`): `dotnet test --collect:"XPlat Code Coverage"` → `**/coverage.cobertura.xml`; ≥ 80% line per assembly.
- Exclude only generated code, `Program.cs`/DI bootstrap and migrations (`[ExcludeFromCodeCoverage]` or runsettings), never logic.

## Logging

- `ILogger<T>` with message templates: `logger.LogInformation("Processing {OrderId}", orderId)`.
- Never `$"..."` nor concatenation in the message; exception as the first argument: `LogError(ex, "...", ...)`.
- Levels: `Information` · `Warning` · `Error` · `Debug`.

## Attributes

- Preserve class and property attributes (`[JsonPropertyName]`, `[Required]`, `[Table]`, `[ApiController]`, `[Authorize]`, …).

## Structure

- Feature: `src/**/Features/<Name>/` (Models, UseCases/Commands/Queries, Repositories, Services, `<Name>Module.cs`) — mirror the existing feature.
- Private helpers of handlers (e.g. MediatR) → feature Service (interface + implementation) registered in the feature's DI module.
