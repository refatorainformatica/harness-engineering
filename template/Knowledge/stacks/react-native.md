# Stack pack — React Native (incl. Expo)

Layer on top of [react.md](./react.md) and [typescript.md](./typescript.md) (read all three).

## Tests

- Jest + React Native Testing Library; native modules mocked (`jest.mock`), HTTP with MSW, fake timers.
- `{Component}.test.tsx` in the feature folder; E2E (Detox/Maestro) only in the E2E suite.

## Coverage

- `jest --coverage` with `lcov` + `cobertura`; `coverageThreshold.global.lines: 80`, excluding only native bridges and generated code.

## Logging

- Application logger/crash reporting with structured context; no `console.log` in release builds; never log tokens, device ids tied to people, or PII.

## Security

- Secrets never in the JS bundle (it ships to devices); tokens in the Keychain/Keystore (`expo-secure-store`, `react-native-keychain`); certificate validation on; deep links validated.

## Structure

- Feature: `src/features/<id>/` (screens, components, hooks, api) — navigation only composes features; platform code (`*.ios.tsx`/`*.android.tsx`) stays in the same feature.
