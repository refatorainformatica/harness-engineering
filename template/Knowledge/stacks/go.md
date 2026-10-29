# Stack pack — Go

Complements [standards.md](../standards.md). Frameworks: standard library `net/http`, Gin, Echo, Fiber, gRPC.

## Code docs (godoc)

- Doc comment in English right above every exported **and** unexported declaration: first sentence starts with the identifier name (summary); following paragraph = remarks (rule and exception in the baseline).
- Package comment in `doc.go` for every package; interface and implementation carry the same doc text.
- Package path = folder (`internal/features/<feature>`).

## Tests

- `testing` + `testify` (`assert`/`require`/`mock`) or `gomock` — whatever the project already uses; table-driven tests.
- File `<subject>_test.go` next to the code in the feature package; test `TestMethodName_ShouldExpectedBehavior_WhenCondition` (or subtests `t.Run("should <behavior> when <condition>")`).
- Interfaces at the consumer for repositories, HTTP clients, brokers and clock; `httptest` for handlers; no `time.Sleep` — inject a clock and use channels/contexts.
- Command: `go test ./internal/features/<feature>/...`.

## Coverage

- `go test ./... -coverprofile=coverage.out`; convert for the gate with `gocover-cobertura < coverage.out > coverage.xml`; ≥ 80% per module/package.

## Logging

- `log/slog` (or zap/zerolog) with key-value fields: `logger.Info("processing order", "order_id", id)`; pass `context.Context` for trace ids.
- Never `fmt.Sprintf` inside the message; errors as a field (`"err", err`) and wrapped with `%w`.

## Tags and directives to preserve

- Struct tags (`json:"id"`, `db:"id"`, `validate:"required"`), `//go:build`, `//go:generate`, `//go:embed` directives.

## Structure

- Feature: `internal/features/<feature>/` (handler, service, domain, repository) — mirror the existing feature; `cmd/<app>/main.go` only wires.
- Handlers only orchestrate; business rules in domain types with methods.
