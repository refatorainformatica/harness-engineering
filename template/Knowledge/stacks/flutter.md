# Stack pack — Flutter (Dart)

Complements [standards.md](../standards.md).

## Code docs (dartdoc)

- `///` in English: first sentence = summary; next paragraph = remarks (rule and exception in the baseline).
- Libraries/folders mirror the feature (`lib/features/<id>/…`).

## Tests

- `flutter_test` / `test` + `mocktail` or `mockito` (whatever the project already uses).
- File `{subject}_test.dart` in `test/features/<id>/…`; the test name describes the behavior in English.
- No `Future.delayed` / `sleep` to synchronize; use `fakeAsync` or an injected clock.

## Coverage

- `flutter test --coverage` → `coverage/lcov.info`; ≥ 80% lines per package (exclude generated `*.g.dart`/`*.freezed.dart`).

## Logging

- The project's structured logger (e.g. `logging`, `logger`); values as fields/arguments, no interpolation in the key message when the logger supports structure.

## Annotations

- Preserve annotations (`@JsonKey`, `@freezed`, `@immutable`, `@override`, …).

## Structure

- Feature: `lib/features/<id>/` (data, domain, presentation) — mirror the existing feature; tests in `test/features/<id>/`.
- Lean widgets: rules in domain/use cases; state per the pattern already adopted (Bloc, Riverpod, Provider…).
- Command: `flutter test test/features/<id>/`.
