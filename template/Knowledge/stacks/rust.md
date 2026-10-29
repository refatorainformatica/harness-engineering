# Stack pack — Rust

Complements [standards.md](../standards.md). Frameworks: Axum, Actix Web, Tokio, Tonic.

## Code docs (rustdoc)

- `///` in English on every item (public and private): first line = summary; following paragraph = remarks (rule and exception in the baseline); `# Errors` / `# Panics` sections when applicable.
- `//!` module docs for every module; trait and implementation docs identical.
- Module path = folder (`src/features/<feature>/`).

## Tests

- Unit tests in `#[cfg(test)] mod tests` inside the module; integration tests in `tests/features/<feature>/`.
- `mockall` for traits at the edges (repositories, HTTP, clock); `tokio::test` for async; no `thread::sleep` — use `tokio::time::pause`.
- Test `method_name_should_expected_behavior_when_condition`.
- Command: `cargo test features::<feature>`.

## Coverage

- `cargo llvm-cov --cobertura --output-path coverage.xml` (or `cargo tarpaulin --out Xml`); ≥ 80% per crate.

## Logging

- `tracing` with fields and spans: `info!(order_id = %id, "processing order")`; `#[instrument]` on orchestrators.
- Never `format!` inside the message; errors as a field (`error = %err`).

## Attributes to preserve

- `#[derive(...)]`, `#[serde(...)]`, `#[cfg(...)]`, `#[instrument]`, `#[async_trait]`, `#[validate(...)]`, `#[must_use]`.

## Structure

- Feature: `src/features/<feature>/` (`handler.rs`, `service.rs`, `domain.rs`, `repository.rs`, `mod.rs`) — mirror the existing feature; `main.rs` only wires.
- No `unsafe` without an ADR; no `unwrap()`/`expect()` on runtime paths.
